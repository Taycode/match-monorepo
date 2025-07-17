# Google API Integration Setup Guide

## Overview

This guide will help you set up Google Forms and Google Sheets API integration for HayaNG's job posting automation system.

## 🚀 What's Implemented

### ✅ Features Added
- **Real Google Forms API Integration**: Automatically creates job application forms
- **Real Google Sheets API Integration**: Automatically creates and links response sheets
- **Form Response Syncing**: Pulls responses from Google Sheets into the database
- **Comprehensive Error Handling**: Graceful fallbacks and detailed logging
- **Management Commands**: CLI tools for testing and syncing
- **API Endpoints**: REST endpoints for manual syncing
- **Setup Scripts**: Automated credential configuration

### 🔧 Components Added

#### 1. **Google API Service Module** (`postings/google_services.py`)
- Authentication with Google APIs
- Form creation with custom questions
- Sheet creation with proper formatting
- Response retrieval and parsing

#### 2. **Updated Job Services** (`postings/job_services.py`)
- Replaced mock implementations with real API calls
- Added graceful fallbacks for development
- Enhanced error handling and logging

#### 3. **Management Commands**
- `python manage.py test_google_api` - Test the integration
- `python manage.py sync_form_responses <job_id>` - Sync responses for a job
- `python manage.py sync_form_responses --all` - Sync all jobs

#### 4. **API Endpoints**
- `POST /posting/jobs/<job_id>/sync-responses/` - Manual sync trigger

#### 5. **Setup Scripts**
- `python setup_google_api.py` - Interactive setup guide
- `python setup_google_api.py validate` - Validate credentials

## 🛠️ Installation Steps

### Step 1: Install Dependencies

```bash
cd server
poetry install
```

The following Google API libraries have been added:
- `google-api-python-client`
- `google-auth-httplib2`
- `google-auth-oauthlib`
- `google-auth`

### Step 2: Google Cloud Setup

Run the interactive setup guide:

```bash
python setup_google_api.py
```

This will guide you through:
1. Creating a Google Cloud Project
2. Enabling required APIs
3. Setting up service account credentials
4. Configuring environment variables

### Step 3: Configure Credentials

#### Option A: Service Account (Recommended)
1. Download your service account JSON file
2. Place it in your project directory
3. Add to `.env`:
   ```
   GOOGLE_CREDENTIALS_FILE=./google-credentials.json
   ```

#### Option B: OAuth2 Credentials
1. Set up OAuth2 credentials in Google Cloud Console
2. Add to `.env`:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REFRESH_TOKEN=your_refresh_token
   ```

### Step 4: Test the Integration

```bash
# Test credentials and create a test job
python manage.py test_google_api

# Test specific parts
python manage.py test_google_api --test-credentials
python manage.py test_google_api --create-test-job
```

## 🔄 How It Works

### Job Creation Flow
1. **User creates job** via frontend or API
2. **Google Form is created** with standardized questions
3. **Google Sheet is created** and linked to the form
4. **Twitter post is published** (existing feature)
5. **Candidates are matched** from talent pool and form responses

### Form Response Syncing
- **Automatic**: Planned for future implementation with webhooks
- **Manual**: Use management commands or API endpoints
- **Scheduled**: Can be set up with cron jobs

## 📋 Form Structure

Each job creates a Google Form with these questions:
1. **Full Name** (required)
2. **Email Address** (required)
3. **Phone Number** (optional)
4. **Resume/CV URL** (required)
5. **Cover Letter** (optional)
6. **Years of Experience** (required dropdown)

## 🔧 API Usage

### Creating a Job (Automatic Integration)
```bash
curl -X POST http://localhost:8000/posting/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Developer",
    "description": "We are looking for a senior developer..."
  }'
```

### Manual Response Sync
```bash
curl -X POST http://localhost:8000/posting/jobs/<job_id>/sync-responses/
```

### Get Job Stats
```bash
curl -X GET http://localhost:8000/posting/jobs/<job_id>/stats/
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Errors
```
Error: Google credentials not configured
```
**Solution**: Run `python setup_google_api.py validate` to check credentials

#### 2. API Not Enabled
```
Error: Google Forms API has not been used
```
**Solution**: Enable APIs in Google Cloud Console

#### 3. Permission Errors
```
Error: The caller does not have permission
```
**Solution**: Ensure service account has Editor role

#### 4. Form Creation Fails
```
Error: Failed to create Google Form
```
**Solution**: Check API quotas and credentials

### Debug Commands

```bash
# Validate credentials
python setup_google_api.py validate

# Test with verbose logging
python manage.py test_google_api --verbosity=2

# Check specific job
python manage.py sync_form_responses <job_id>
```

## 🔒 Security Notes

### Important
- Never commit `google-credentials.json` to version control
- Use environment variables for all sensitive data
- Regularly rotate service account keys
- Monitor API usage and quotas

### .gitignore Entries
```
google-credentials.json
.env.google.template
```

## 🎯 Testing the Full Workflow

1. **Create a test job**:
   ```bash
   python manage.py test_google_api --create-test-job
   ```

2. **Fill out the form** using the provided URL

3. **Sync responses**:
   ```bash
   python manage.py sync_form_responses <job_id>
   ```

4. **Check matches**:
   ```bash
   curl -X GET http://localhost:8000/posting/jobs/<job_id>/matches/
   ```

## 📊 Monitoring

### Key Metrics to Monitor
- Form creation success rate
- Response sync frequency
- API quota usage
- Error rates

### Logging
All Google API operations are logged with structured logging:
- Success/failure status
- Response times
- Error details
- Job and form IDs

## 🚀 Next Steps

1. **Set up credentials** following this guide
2. **Test the integration** with sample data
3. **Create your first real job** posting
4. **Monitor the automation** in production
5. **Set up automated syncing** with cron jobs

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Run validation commands
3. Review the logs
4. Check Google Cloud Console for API errors

The integration is designed to be robust with fallbacks, so your job creation will continue working even if Google APIs are temporarily unavailable. 