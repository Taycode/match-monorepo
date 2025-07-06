from django.core.management.base import BaseCommand
from postings.models import Job
from postings.job_services import sync_form_responses
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync form responses from Google Sheets for a specific job or all jobs'

    def add_arguments(self, parser):
        parser.add_argument(
            'job_id',
            nargs='?',
            type=str,
            help='Specific job ID to sync responses for',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Sync responses for all jobs',
        )

    def handle(self, *args, **options):
        job_id = options['job_id']
        sync_all = options['all']
        
        if job_id:
            self.sync_job_responses(job_id)
        elif sync_all:
            self.sync_all_responses()
        else:
            self.stdout.write(
                self.style.WARNING("Please specify a job ID or use --all flag")
            )
            self.stdout.write("Usage:")
            self.stdout.write("  python manage.py sync_form_responses <job_id>")
            self.stdout.write("  python manage.py sync_form_responses --all")

    def sync_job_responses(self, job_id):
        """Sync responses for a specific job"""
        self.stdout.write(f"🔄 Syncing form responses for job: {job_id}")
        
        try:
            job = Job.objects.get(id=job_id)
            
            if not job.google_sheet_id:
                self.stdout.write(
                    self.style.WARNING(f"   ⚠️  Job {job_id} has no Google Sheet ID")
                )
                return
            
            self.stdout.write(f"   📋 Job: {job.title}")
            self.stdout.write(f"   📊 Sheet: {job.google_sheet_url}")
            
            new_responses = sync_form_responses(job_id)
            
            if new_responses > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"   ✅ Synced {new_responses} new responses")
                )
            else:
                self.stdout.write("   ℹ️  No new responses found")
                
        except Job.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Job {job_id} not found")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Error syncing responses: {str(e)}")
            )
            logger.error(f"Error syncing responses for job {job_id}: {str(e)}", exc_info=True)

    def sync_all_responses(self):
        """Sync responses for all jobs"""
        self.stdout.write("🔄 Syncing form responses for all jobs...")
        
        jobs = Job.objects.filter(google_sheet_id__isnull=False)
        total_jobs = jobs.count()
        
        if total_jobs == 0:
            self.stdout.write(
                self.style.WARNING("   ⚠️  No jobs with Google Sheets found")
            )
            return
        
        self.stdout.write(f"   📊 Found {total_jobs} jobs with Google Sheets")
        
        total_new_responses = 0
        successful_syncs = 0
        
        for job in jobs:
            self.stdout.write(f"\n   🔄 Processing job: {job.title} ({job.id})")
            
            try:
                new_responses = sync_form_responses(str(job.id))
                total_new_responses += new_responses
                successful_syncs += 1
                
                if new_responses > 0:
                    self.stdout.write(f"      ✅ {new_responses} new responses")
                else:
                    self.stdout.write("      ℹ️  No new responses")
                    
            except Exception as e:
                self.stdout.write(f"      ❌ Error: {str(e)}")
                logger.error(f"Error syncing responses for job {job.id}: {str(e)}", exc_info=True)
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Sync completed!")
        )
        self.stdout.write(f"   📊 Jobs processed: {successful_syncs}/{total_jobs}")
        self.stdout.write(f"   📥 Total new responses: {total_new_responses}")
        
        if successful_syncs < total_jobs:
            self.stdout.write(
                self.style.WARNING(f"   ⚠️  {total_jobs - successful_syncs} jobs had errors")
            ) 