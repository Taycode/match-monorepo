#!/usr/bin/env python3
"""
Google API Setup Script for HayaNG

This script helps you set up Google API credentials for Forms and Sheets integration.
Follow the instructions to create a service account and download the credentials.
"""

import os
import json
from pathlib import Path

def create_google_credentials_template():
    """Create a template for Google API credentials"""
    
    print("🔧 Google API Setup for HayaNG")
    print("=" * 50)
    
    print("\n📋 STEP 1: Create Google Cloud Project")
    print("   1. Go to https://console.cloud.google.com/")
    print("   2. Create a new project or select an existing one")
    print("   3. Note your project ID")
    
    print("\n🔑 STEP 2: Enable APIs")
    print("   1. Go to 'APIs & Services' > 'Library'")
    print("   2. Enable the following APIs:")
    print("      - Google Forms API")
    print("      - Google Sheets API")
    print("      - Google Drive API")
    
    print("\n🎯 STEP 3: Create Service Account")
    print("   1. Go to 'APIs & Services' > 'Credentials'")
    print("   2. Click 'Create Credentials' > 'Service Account'")
    print("   3. Fill in the details:")
    print("      - Name: HayaNG Service Account")
    print("      - Description: Service account for HayaNG job posting automation")
    print("   4. Grant the service account these roles:")
    print("      - Editor (for creating forms and sheets)")
    print("   5. Click 'Done'")
    
    print("\n📥 STEP 4: Download Service Account Key")
    print("   1. Click on the service account you just created")
    print("   2. Go to 'Keys' tab")
    print("   3. Click 'Add Key' > 'Create New Key'")
    print("   4. Choose 'JSON' format")
    print("   5. Save the file as 'google-credentials.json'")
    
    print("\n🔐 STEP 5: Configure Environment Variables")
    print("   Option A: Use Service Account (Recommended)")
    print("   Add this to your .env file:")
    print("   GOOGLE_CREDENTIALS_FILE=/path/to/your/google-credentials.json")
    
    print("\n   Option B: Use OAuth2 (Alternative)")
    print("   1. Go to 'APIs & Services' > 'Credentials'")
    print("   2. Click 'Create Credentials' > 'OAuth client ID'")
    print("   3. Choose 'Web application'")
    print("   4. Add these to your .env file:")
    print("   GOOGLE_CLIENT_ID=your_client_id")
    print("   GOOGLE_CLIENT_SECRET=your_client_secret")
    print("   GOOGLE_REFRESH_TOKEN=your_refresh_token")
    
    print("\n✅ STEP 6: Test Your Setup")
    print("   Run: python manage.py test_google_api")
    
    print("\n⚠️  IMPORTANT SECURITY NOTES:")
    print("   - Never commit your credentials file to version control")
    print("   - Add google-credentials.json to your .gitignore")
    print("   - Keep your credentials secure")
    
    # Create a sample .env template
    env_template = """
# Google API Configuration
# Option A: Service Account (Recommended)
GOOGLE_CREDENTIALS_FILE=./google-credentials.json

# Option B: OAuth2 (Alternative)
# GOOGLE_CLIENT_ID=your_client_id_here
# GOOGLE_CLIENT_SECRET=your_client_secret_here
# GOOGLE_REFRESH_TOKEN=your_refresh_token_here

# Other existing environment variables...
"""
    
    with open('.env.google.template', 'w') as f:
        f.write(env_template)
    
    print(f"\n📄 Created .env.google.template with sample configuration")
    print("   Copy the relevant lines to your .env file")
    
    # Create gitignore entries
    gitignore_entries = """
# Google API Credentials
google-credentials.json
.env.google.template
"""
    
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        if 'google-credentials.json' not in content:
            with open(gitignore_path, 'a') as f:
                f.write(gitignore_entries)
            print("   Added Google credentials to .gitignore")
    else:
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_entries)
        print("   Created .gitignore with Google credentials")


def validate_credentials():
    """Validate Google API credentials"""
    
    print("\n🔍 Validating Google API Credentials...")
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
    
    if credentials_file and os.path.exists(credentials_file):
        print("   ✅ Service account credentials file found")
        
        try:
            with open(credentials_file, 'r') as f:
                creds = json.load(f)
            
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if field not in creds]
            
            if missing_fields:
                print(f"   ❌ Missing fields in credentials file: {', '.join(missing_fields)}")
                return False
            
            if creds.get('type') != 'service_account':
                print("   ❌ Credentials file is not a service account")
                return False
            
            print(f"   ✅ Service account: {creds.get('client_email')}")
            print(f"   ✅ Project ID: {creds.get('project_id')}")
            
        except json.JSONDecodeError:
            print("   ❌ Invalid JSON in credentials file")
            return False
        except Exception as e:
            print(f"   ❌ Error reading credentials file: {str(e)}")
            return False
    
    elif client_id and client_secret and refresh_token:
        print("   ✅ OAuth2 credentials found")
        print(f"   ✅ Client ID: {client_id[:20]}...")
        
    else:
        print("   ❌ No valid Google API credentials found")
        print("   Please configure either:")
        print("   - GOOGLE_CREDENTIALS_FILE (service account)")
        print("   - GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN (OAuth2)")
        return False
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        validate_credentials()
    else:
        create_google_credentials_template() 