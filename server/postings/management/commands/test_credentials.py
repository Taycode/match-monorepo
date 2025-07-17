import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Test API credentials configuration'

    def handle(self, *args, **options):
        self.stdout.write("🔐 Testing API Credentials Configuration\n")
        
        # Test Google API credentials
        self.stdout.write("📋 Google APIs:")
        google_configured = False
        
        if settings.GOOGLE_CREDS:
            try:
                import json
                json.loads(settings.GOOGLE_CREDS)
                self.stdout.write("   ✅ GOOGLE_CREDS (JSON string) configured")
                google_configured = True
            except:
                self.stdout.write("   ❌ GOOGLE_CREDS contains invalid JSON")
        elif settings.GOOGLE_CREDENTIALS_FILE and os.path.exists(settings.GOOGLE_CREDENTIALS_FILE):
            self.stdout.write("   ✅ Service Account file found")
            google_configured = True
        elif settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET and settings.GOOGLE_REFRESH_TOKEN:
            self.stdout.write("   ✅ OAuth2 credentials configured")
            google_configured = True
        else:
            self.stdout.write("   ❌ Google credentials not configured")
            self.stdout.write("      Need: GOOGLE_CREDS (JSON string) OR GOOGLE_CREDENTIALS_FILE OR (GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET + GOOGLE_REFRESH_TOKEN)")
        
        # Test Twitter API credentials
        self.stdout.write("\n🐦 Twitter API:")
        twitter_configured = True
        twitter_vars = [
            'TWITTER_BEARER_TOKEN',
            'TWITTER_ACCESS_TOKEN', 
            'TWITTER_ACCESS_TOKEN_SECRET',
            'TWITTER_API_KEY',
            'TWITTER_API_KEY_SECRET'
        ]
        
        for var in twitter_vars:
            value = getattr(settings, var, None)
            if value:
                self.stdout.write(f"   ✅ {var} configured")
            else:
                self.stdout.write(f"   ❌ {var} missing")
                twitter_configured = False
        
        # Test OpenAI (should be working)
        self.stdout.write("\n🤖 OpenAI API:")
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            self.stdout.write("   ✅ OPENAI_API_KEY configured")
        elif hasattr(settings, 'OPENAPI_API_KEY') and settings.OPENAPI_API_KEY:
            self.stdout.write("   ✅ OPENAPI_API_KEY configured")
        else:
            self.stdout.write("   ❌ OpenAI API key missing")
        
        # Test Pinecone (should be working)  
        self.stdout.write("\n🌲 Pinecone API:")
        if settings.PINECONE_API_KEY:
            self.stdout.write("   ✅ PINECONE_API_KEY configured")
        else:
            self.stdout.write("   ❌ PINECONE_API_KEY missing")
        
        # Summary
        self.stdout.write("\n" + "="*50)
        if google_configured and twitter_configured:
            self.stdout.write("🎉 All automations should work!")
        else:
            self.stdout.write("⚠️  Some automations will use mock data:")
            if not google_configured:
                self.stdout.write("   - Google Forms/Sheets → Mock URLs")
            if not twitter_configured:
                self.stdout.write("   - Twitter posting → Skipped") 