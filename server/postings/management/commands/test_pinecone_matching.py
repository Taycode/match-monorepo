from django.core.management.base import BaseCommand
from postings.models import Job, FormResponse
from postings.job_services import match_candidates_for_job
from vector.service import VectorManager
from talents.models import Talent
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test Pinecone-based candidate matching system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--job-id',
            type=str,
            help='Test matching for specific job ID',
        )
        parser.add_argument(
            '--test-pinecone',
            action='store_true',
            help='Test Pinecone connection and basic functionality',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Testing Pinecone-based Candidate Matching')
        )
        
        if options['test_pinecone']:
            self.test_pinecone_connection()
            
        if options['job_id']:
            self.test_job_matching(options['job_id'])
        else:
            self.test_system_overview()

    def test_pinecone_connection(self):
        """Test basic Pinecone connection and functionality"""
        self.stdout.write("\n🔌 Testing Pinecone Connection...")
        
        try:
            # Test talent pool index
            self.stdout.write("  📊 Testing talent pool index...")
            talent_manager = VectorManager('haya-talents', create_index=False)
            
            # Try a simple search
            test_results = talent_manager.search("Python developer", top_k=5)
            self.stdout.write(f"    ✅ Found {len(test_results.matches)} talent matches")
            
            # Test job-specific index (create a small test one)
            self.stdout.write("  📋 Testing job-specific index creation...")
            test_job_manager = VectorManager('test-job-responses', create_index=True)
            
            # Add a test vector
            test_job_manager.add_text_to_index(
                unique_id="test-123",
                text="Python developer with 5 years experience",
                metadata={"name": "Test Candidate", "experience": "5 years"}
            )
            
            # Search for it
            search_results = test_job_manager.search("Python developer", top_k=5)
            self.stdout.write(f"    ✅ Test index working: {len(search_results.matches)} matches")
            
            for match in search_results.matches[:3]:
                self.stdout.write(f"      - Score: {match.score:.3f}, ID: {match.id}")
            
        except Exception as e:
            self.stdout.write(f"    ❌ Pinecone connection failed: {str(e)}")
            logger.error(f"Pinecone connection test failed: {str(e)}", exc_info=True)

    def test_job_matching(self, job_id: str):
        """Test matching for a specific job"""
        self.stdout.write(f"\n🎯 Testing Job Matching for Job ID: {job_id}")
        
        try:
            # Get job details
            job = Job.objects.get(id=job_id)
            self.stdout.write(f"  📋 Job: {job.title}")
            self.stdout.write(f"  📝 Description: {job.description[:100]}...")
            
            # Test the matching system
            self.stdout.write("\n  🔍 Running candidate matching...")
            matches = match_candidates_for_job(job_id)
            
            self.stdout.write(f"  ✅ Found {len(matches)} total matches")
            
            # Breakdown by type
            talent_matches = [m for m in matches if m['candidate_type'] == 'talent']
            form_matches = [m for m in matches if m['candidate_type'] == 'form_response']
            
            self.stdout.write(f"    👥 Talent Pool: {len(talent_matches)} matches")
            self.stdout.write(f"    📝 Form Responses: {len(form_matches)} matches")
            
            # Show top matches
            if matches:
                self.stdout.write("\n  🏆 Top 5 Matches:")
                for i, match in enumerate(matches[:5], 1):
                    candidate_data = match['candidate_data']
                    score = match['similarity_score']
                    match_type = match['candidate_type']
                    
                    # Color code based on score
                    if score > 0.8:
                        color = self.style.SUCCESS
                    elif score > 0.6:
                        color = self.style.WARNING
                    else:
                        color = self.style.ERROR
                    
                    name = candidate_data.get('name', 'Unknown')
                    message = f"{i}. {name} ({match_type}): {score:.3f}"
                    self.stdout.write(f"    {color(message)}")
                    
                    # Show additional details
                    if match_type == 'talent':
                        skills = candidate_data.get('skills', [])
                        if skills:
                            skills_str = ', '.join(skills[:3]) if isinstance(skills, list) else str(skills)[:50]
                            self.stdout.write(f"       Skills: {skills_str}")
                    else:
                        years_exp = candidate_data.get('years_of_experience', '')
                        if years_exp:
                            self.stdout.write(f"       Experience: {years_exp}")
            
        except Job.DoesNotExist:
            self.stdout.write(f"    ❌ Job with ID {job_id} not found")
        except Exception as e:
            self.stdout.write(f"    ❌ Error testing job matching: {str(e)}")
            logger.error(f"Error testing job matching: {str(e)}", exc_info=True)

    def test_system_overview(self):
        """Test overall system health and data availability"""
        self.stdout.write("\n📊 System Overview...")
        
        try:
            # Check data availability
            total_jobs = Job.objects.count()
            total_talents = Talent.objects.count()
            total_form_responses = FormResponse.objects.count()
            
            self.stdout.write(f"  📋 Total Jobs: {total_jobs}")
            self.stdout.write(f"  👥 Total Talents: {total_talents}")
            self.stdout.write(f"  📝 Total Form Responses: {total_form_responses}")
            
            # Check Pinecone data
            if total_talents > 0:
                self.stdout.write("\n  🔍 Checking Pinecone talent data...")
                try:
                    talent_manager = VectorManager('haya-talents', create_index=False)
                    test_search = talent_manager.search("developer", top_k=5)
                    self.stdout.write(f"    ✅ Pinecone talent index responsive: {len(test_search.matches)} results")
                except Exception as e:
                    self.stdout.write(f"    ❌ Pinecone talent index issue: {str(e)}")
            
            # Suggest next steps
            self.stdout.write("\n  💡 Suggestions:")
            if total_jobs == 0:
                self.stdout.write("    - Create a test job using: python manage.py test_google_api --create-test-job")
            elif total_talents == 0:
                self.stdout.write("    - Add talents to the pool via the admin interface or API")
            else:
                recent_job = Job.objects.order_by('-created_at').first()
                self.stdout.write(f"    - Test matching with recent job: python manage.py test_pinecone_matching --job-id {recent_job.id}")
            
        except Exception as e:
            self.stdout.write(f"    ❌ Error checking system overview: {str(e)}")
            logger.error(f"Error checking system overview: {str(e)}", exc_info=True) 