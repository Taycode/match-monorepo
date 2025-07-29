from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
import structlog
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from django.db import models

from .models import Posting, Job, Match
from .pagination import PostingCursorPagination
from .serializers import (
    PostingSerializer, InitiatePostingSerializer,
    JobSerializer, CreateJobSerializer, MatchSerializer
)
from .services import generate_tweet_content_for_posting, trigger_post_on_twitter
from .job_services import create_job_with_automations, match_candidates_for_job, sync_form_responses

logger = structlog.get_logger(__name__)


# Existing Posting Views (Social Media)
class CreatePostingView(generics.CreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    parser_classes = [CamelCaseJSONParser]

    def create(self, request, *args, **kwargs):
        """
        We override `create` to add custom error handling/logging.
        Note that `super().create(...)` returns a `Response`, not the instance.
        """
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            # Re-raise validation errors to return the usual 400 response
            raise e from e
        except Exception:
            # Log any unexpected error and return a generic 500
            logger.exception(
                "Error creating Posting or posting tweet on Twitter")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        """
        This is where the actual instance is created.
        We call `serializer.save()` to create the object,
        then run `trigger_post_on_twitter(...)` with the newly created instance.
        """
        instance = serializer.save()
        trigger_post_on_twitter(instance)


class RetrievePostingView(generics.RetrieveAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer


class ListPostingView(generics.ListAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    pagination_class = PostingCursorPagination


class InitiatePostingView(APIView):
    serializer_class = InitiatePostingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        responses = generate_tweet_content_for_posting(
            validated_data,
            2
        )
        return Response({
            'responses': responses
        }, status.HTTP_200_OK)


# MVP Job Posting Views
class CreateJobView(APIView):
    """
    Create a new job posting with all automations
    """

    def post(self, request):
        serializer = CreateJobSerializer(data=request.data)
        if serializer.is_valid():
            try:
                title = serializer.validated_data['title']
                description = serializer.validated_data['description']

                # Create job with all automations
                job, matches = create_job_with_automations(title, description)

                # Return job details with matches
                job_serializer = JobSerializer(job)
                return Response({
                    'job': job_serializer.data,
                    'matches_count': len(matches),
                    'message': 'Job created successfully with all automations'
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error creating job: {str(e)}")
                return Response({
                    'error': 'Failed to create job with automations',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListJobsView(generics.ListAPIView):
    """
    List all job postings
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        # Add search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class JobDetailView(generics.RetrieveAPIView):
    """
    Get specific job details
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobMatchesView(generics.ListAPIView):
    """
    Get all matches for a specific job
    """
    serializer_class = MatchSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Match.objects.filter(job_id=job_id)

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            matches = Match.objects.filter(
                job=job).order_by('-similarity_score')

            # Separate matches by type
            talent_matches = matches.filter(candidate_type='talent')
            form_matches = matches.filter(candidate_type='form_response')

            talent_serializer = MatchSerializer(talent_matches, many=True)
            form_serializer = MatchSerializer(form_matches, many=True)

            return Response({
                'job_id': job_id,
                'job_title': job.title,
                'total_matches': matches.count(),
                'talent_pool_matches': {
                    'count': talent_matches.count(),
                    'candidates': talent_serializer.data
                },
                'form_response_matches': {
                    'count': form_matches.count(),
                    'candidates': form_serializer.data
                }
            })

        except Job.DoesNotExist:
            return Response({
                'error': 'Job not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error getting matches for job {job_id}: {str(e)}")
            return Response({
                'error': 'Failed to get job matches'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShortlistCandidateView(APIView):
    """
    Shortlist or un-shortlist a candidate
    """

    def post(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id)
            # 'shortlist' or 'remove'
            action = request.data.get('action', 'shortlist')

            if action == 'shortlist':
                match.is_shortlisted = True
                message = 'Candidate shortlisted successfully'
            elif action == 'remove':
                match.is_shortlisted = False
                message = 'Candidate removed from shortlist'
            else:
                return Response({
                    'error': 'Invalid action. Use "shortlist" or "remove"'
                }, status=status.HTTP_400_BAD_REQUEST)

            match.save()

            serializer = MatchSerializer(match)
            return Response({
                'match': serializer.data,
                'message': message
            })

        except Match.DoesNotExist:
            return Response({
                'error': 'Match not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Error updating shortlist for match {match_id}: {str(e)}")
            return Response({
                'error': 'Failed to update shortlist'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshMatchesView(APIView):
    """
    Re-run matching algorithm for a job
    """

    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)

            # Clear existing matches
            Match.objects.filter(job=job).delete()

            # Run matching again
            matches = match_candidates_for_job(job_id)

            return Response({
                'job_id': job_id,
                'matches_found': len(matches),
                'message': 'Matches refreshed successfully'
            })

        except Job.DoesNotExist:
            return Response({
                'error': 'Job not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Error refreshing matches for job {job_id}: {str(e)}")
            return Response({
                'error': 'Failed to refresh matches'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobStatsView(APIView):
    """
    Get statistics for a job
    """

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            matches = Match.objects.filter(job=job)

            stats = {
                'job_title': job.title,
                'created_at': job.created_at,
                'total_matches': matches.count(),
                'talent_pool_matches': matches.filter(candidate_type='talent').count(),
                'form_response_matches': matches.filter(candidate_type='form_response').count(),
                'shortlisted_candidates': matches.filter(is_shortlisted=True).count(),
                'google_form_url': job.google_form_url,
                'google_sheet_url': job.google_sheet_url,
                'twitter_posted': bool(job.twitter_post_id),
                'avg_similarity_score': matches.aggregate(
                    avg_score=models.Avg('similarity_score')
                )['avg_score'] or 0
            }

            return Response(stats)

        except Job.DoesNotExist:
            return Response({
                'error': 'Job not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error getting stats for job {job_id}: {str(e)}")
            return Response({
                'error': 'Failed to get job stats'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SyncFormResponsesView(APIView):
    """
    Sync form responses from Google Sheets for a specific job
    """

    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            from .google_services import get_a_google_form

            if not job.google_sheet_id:

                form = get_a_google_form(job.google_form_id)

                linked_sheet_id = form.get('linkedSheetId') if form else None
                if linked_sheet_id:
                    job.google_sheet_id = form.get('linkedSheetId')
                    job.google_sheet_url = f"https://docs.google.com/spreadsheets/d/{linked_sheet_id}"
                    job.save()
                else:
                    logger.error(
                        f"Job {job_id} has no Google Sheet configured")
                    return Response({
                        'error': 'Job has no Google Sheet configured'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Sync responses from Google Sheets
            new_responses = sync_form_responses(job_id)

            # Re-run matching if new responses were found
            if new_responses > 0:
                matches = match_candidates_for_job(job_id)

                return Response({
                    'job_id': job_id,
                    'new_responses': new_responses,
                    'matches_updated': len(matches),
                    'message': f'Synced {new_responses} new responses and updated matches'
                })
            else:
                return Response({
                    'job_id': job_id,
                    'new_responses': 0,
                    'message': 'No new responses found'
                })

        except Job.DoesNotExist:
            return Response({
                'error': 'Job not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Error syncing form responses for job {job_id}: {str(e)}")
            return Response({
                'error': 'Failed to sync form responses',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
