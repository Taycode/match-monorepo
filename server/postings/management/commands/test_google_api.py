from django.core.management.base import BaseCommand
from django.utils import timezone
from postings.models import Job
from postings.google_services import (
    get_google_credentials,
    create_google_form,
    create_google_sheet,
    get_form_responses,
    get_sheet_responses
)
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test Google API integration for Forms and Sheets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-test-job',
            action='store_true',
            help='Create a test job with Google Form and Sheet',
        )
        parser.add_argument(
            '--test-credentials',
            action='store_true',
            help='Test Google API credentials',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Testing Google API Integration')
        )
        
        if options['test_credentials']:
            self.test_credentials()
        
        if options['create_test_job']:
            self.create_test_job()
        
        if not options['test_credentials'] and not options['create_test_job']:
            self.test_credentials()
            self.create_test_job()

    def test_credentials(self):
        """Test Google API credentials"""
        self.stdout.write("\n🔑 Testing Google API Credentials...")
        
        try:
            credentials = get_google_credentials()
            self.stdout.write(
                self.style.SUCCESS("   ✅ Successfully authenticated with Google API")
            )
            
            if hasattr(credentials, 'service_account_email'):
                self.stdout.write(f"   📧 Service Account: {credentials.service_account_email}")
            
            if hasattr(credentials, 'project_id'):
                self.stdout.write(f"   🏗️  Project ID: {credentials.project_id}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Error authenticating: {str(e)}")
            )
            self.stdout.write(
                self.style.WARNING("   💡 Run 'python setup_google_api.py' for setup instructions")
            )
            return False
        
        return True

    def create_test_job(self):
        """Create a test job with Google Form and Sheet"""
        self.stdout.write("\n🚀 Creating Test Job...")
        
        # Test job data
        test_title = "Test Software Engineer Position"
        test_description = """
We are looking for a talented Software Engineer to join our team.

Requirements:
- 3+ years of experience in software development
- Proficiency in Python, JavaScript, or similar languages
- Experience with web frameworks (Django, React, etc.)
- Strong problem-solving skills
- Good communication skills

Responsibilities:
- Develop and maintain web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews
- Contribute to technical documentation

Benefits:
- Competitive salary
- Health insurance
- Flexible working hours
- Professional development opportunities
- Remote work options

This is a test job posting created by the Google API integration test.
        """.strip()
        
        try:
            # Create test job in database
            job = Job.objects.create(
                title=test_title,
                description=test_description
            )
            
            self.stdout.write(f"   ✅ Created test job: {job.id}")
            
            # Test Google Form creation
            self.stdout.write("   📋 Creating Google Form...")
            form_id, form_url = create_google_form(test_title, test_description)
            
            job.google_form_id = form_id
            job.google_form_url = form_url
            
            self.stdout.write(f"   ✅ Form created: {form_url}")
            
            # Test Google Sheet creation
            self.stdout.write("   📊 Creating Google Sheet...")
            sheet_id, sheet_url = create_google_sheet(test_title, form_id)
            
            job.google_sheet_id = sheet_id
            job.google_sheet_url = sheet_url
            job.save()
            
            self.stdout.write(f"   ✅ Sheet created: {sheet_url}")
            
            # Test reading responses (should be empty)
            self.stdout.write("   📥 Testing response retrieval...")
            
            form_responses = get_form_responses(form_id)
            sheet_responses = get_sheet_responses(sheet_id)
            
            self.stdout.write(f"   📊 Form responses: {len(form_responses)}")
            self.stdout.write(f"   📊 Sheet responses: {len(sheet_responses)}")
            
            # Success summary
            self.stdout.write(
                self.style.SUCCESS("\n🎉 Test completed successfully!")
            )
            self.stdout.write(f"   🆔 Job ID: {job.id}")
            self.stdout.write(f"   📋 Form: {form_url}")
            self.stdout.write(f"   📊 Sheet: {sheet_url}")
            
            self.stdout.write(
                self.style.WARNING("\n💡 To test the full workflow:")
            )
            self.stdout.write(f"   1. Fill out the form: {form_url}")
            self.stdout.write(f"   2. Check the sheet: {sheet_url}")
            self.stdout.write(f"   3. Run: python manage.py sync_form_responses {job.id}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Error creating test job: {str(e)}")
            )
            logger.error(f"Error in test_google_api: {str(e)}", exc_info=True)
            
            # Clean up if job was created
            try:
                if 'job' in locals():
                    job.delete()
                    self.stdout.write("   🧹 Cleaned up test job")
            except:
                pass 