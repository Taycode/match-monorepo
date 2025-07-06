import os
import json
import logging
from typing import Tuple, Dict, Any
from django.conf import settings

from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# Google API scopes needed for Forms and Sheets
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/forms.responses.readonly',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]


def get_google_credentials():
    """
    Get Google API credentials from environment variables or service account file
    """
    try:
        # Try service account first (recommended for production)
        if settings.GOOGLE_CREDENTIALS_FILE and os.path.exists(settings.GOOGLE_CREDENTIALS_FILE):
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_FILE,
                scopes=SCOPES
            )
            return credentials
        
        # Fallback to OAuth2 credentials
        elif settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET and settings.GOOGLE_REFRESH_TOKEN:
            credentials = Credentials(
                token=None,
                refresh_token=settings.GOOGLE_REFRESH_TOKEN,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                scopes=SCOPES
            )
            
            # Refresh the token
            credentials.refresh(Request())
            return credentials
        
        else:
            raise ValueError("Google credentials not configured. Please set GOOGLE_CREDENTIALS_FILE or OAuth2 credentials.")
    
    except Exception as e:
        logger.error(f"Error getting Google credentials: {str(e)}")
        raise


def create_google_form(job_title: str, job_description: str) -> Tuple[str, str]:
    """
    Create a Google Form for job applications
    
    Returns:
        Tuple of (form_id, form_url)
    """
    try:
        credentials = get_google_credentials()
        service = build('forms', 'v1', credentials=credentials)
        
        # Create the form
        form_body = {
            "info": {
                "title": f"Application for {job_title}",
                "description": f"Please fill out this form to apply for the position: {job_title}\n\n{job_description[:200]}..."
            }
        }
        
        # Create form
        form = service.forms().create(body=form_body).execute()
        form_id = form['formId']
        
        # Add questions to the form
        questions = [
            {
                "title": "Full Name",
                "description": "Please enter your full name",
                "required": True,
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Email Address",
                "description": "Please enter your email address",
                "required": True,
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Phone Number",
                "description": "Please enter your phone number",
                "required": False,
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Resume/CV",
                "description": "Please provide a link to your resume/CV (Google Drive, Dropbox, etc.)",
                "required": True,
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Cover Letter",
                "description": "Please write a brief cover letter explaining why you're interested in this position",
                "required": False,
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Years of Experience",
                "description": "How many years of relevant experience do you have?",
                "required": True,
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "DROP_DOWN",
                            "options": [
                                {"value": "0-1 years"},
                                {"value": "1-3 years"},
                                {"value": "3-5 years"},
                                {"value": "5-10 years"},
                                {"value": "10+ years"}
                            ]
                        }
                    }
                }
            }
        ]
        
        # Add questions to form
        requests = []
        for i, question in enumerate(questions):
            requests.append({
                "createItem": {
                    "item": question,
                    "location": {
                        "index": i
                    }
                }
            })
        
        # Batch update to add all questions
        service.forms().batchUpdate(
            formId=form_id,
            body={"requests": requests}
        ).execute()
        
        # Get the form URL
        form_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
        
        logger.info(f"Successfully created Google Form: {form_id}")
        return form_id, form_url
        
    except HttpError as error:
        logger.error(f"Google Forms API error: {error}")
        raise Exception(f"Failed to create Google Form: {error}")
    except Exception as e:
        logger.error(f"Error creating Google Form: {str(e)}")
        raise


def create_google_sheet(job_title: str, form_id: str) -> Tuple[str, str]:
    """
    Create a Google Sheet to collect form responses
    
    Returns:
        Tuple of (sheet_id, sheet_url)
    """
    try:
        credentials = get_google_credentials()
        sheets_service = build('sheets', 'v4', credentials=credentials)
        forms_service = build('forms', 'v1', credentials=credentials)
        
        # Create the spreadsheet
        spreadsheet_body = {
            'properties': {
                'title': f"Applications for {job_title}"
            },
            'sheets': [{
                'properties': {
                    'title': 'Form Responses'
                }
            }]
        }
        
        spreadsheet = sheets_service.spreadsheets().create(
            body=spreadsheet_body
        ).execute()
        
        sheet_id = spreadsheet['spreadsheetId']
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        
        # Set up headers for the responses
        headers = [
            'Timestamp',
            'Full Name',
            'Email Address',
            'Phone Number',
            'Resume/CV',
            'Cover Letter',
            'Years of Experience'
        ]
        
        # Add headers to the sheet
        values = [headers]
        body = {
            'values': values
        }
        
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='A1:G1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        # Format the header row
        format_request = {
            'requests': [{
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 7
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {
                                'bold': True
                            },
                            'backgroundColor': {
                                'red': 0.9,
                                'green': 0.9,
                                'blue': 0.9
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(textFormat,backgroundColor)'
                }
            }]
        }
        
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body=format_request
        ).execute()
        
        # Link the form to the sheet (this creates the automatic response collection)
        try:
            forms_service.forms().batchUpdate(
                formId=form_id,
                body={
                    "requests": [{
                        "updateFormInfo": {
                            "info": {
                                "linkedSheetId": sheet_id
                            },
                            "updateMask": "linkedSheetId"
                        }
                    }]
                }
            ).execute()
        except Exception as e:
            logger.warning(f"Could not link form to sheet automatically: {str(e)}")
            # This is not critical, responses can still be fetched manually
        
        logger.info(f"Successfully created Google Sheet: {sheet_id}")
        return sheet_id, sheet_url
        
    except HttpError as error:
        logger.error(f"Google Sheets API error: {error}")
        raise Exception(f"Failed to create Google Sheet: {error}")
    except Exception as e:
        logger.error(f"Error creating Google Sheet: {str(e)}")
        raise


def get_form_responses(form_id: str) -> list:
    """
    Get all responses from a Google Form
    
    Returns:
        List of response dictionaries
    """
    try:
        credentials = get_google_credentials()
        service = build('forms', 'v1', credentials=credentials)
        
        # Get form responses
        responses = service.forms().responses().list(formId=form_id).execute()
        
        if 'responses' not in responses:
            return []
        
        # Parse responses
        parsed_responses = []
        for response in responses['responses']:
            parsed_response = {
                'response_id': response['responseId'],
                'timestamp': response['lastSubmittedTime'],
                'answers': {}
            }
            
            if 'answers' in response:
                for question_id, answer in response['answers'].items():
                    if 'textAnswers' in answer:
                        parsed_response['answers'][question_id] = answer['textAnswers']['answers'][0]['value']
                    elif 'choiceAnswers' in answer:
                        parsed_response['answers'][question_id] = answer['choiceAnswers']['answers'][0]['value']
            
            parsed_responses.append(parsed_response)
        
        logger.info(f"Retrieved {len(parsed_responses)} responses from form {form_id}")
        return parsed_responses
        
    except HttpError as error:
        logger.error(f"Google Forms API error: {error}")
        return []
    except Exception as e:
        logger.error(f"Error getting form responses: {str(e)}")
        return []


def get_sheet_responses(sheet_id: str) -> list:
    """
    Get all responses from a Google Sheet
    
    Returns:
        List of response dictionaries
    """
    try:
        credentials = get_google_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        
        # Get all data from the sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='A:Z'  # Get all columns
        ).execute()
        
        values = result.get('values', [])
        
        if not values or len(values) < 2:
            return []
        
        # First row is headers
        headers = values[0]
        responses = []
        
        for row in values[1:]:  # Skip header row
            response = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    response[header] = row[i]
                else:
                    response[header] = ''
            responses.append(response)
        
        logger.info(f"Retrieved {len(responses)} responses from sheet {sheet_id}")
        return responses
        
    except HttpError as error:
        logger.error(f"Google Sheets API error: {error}")
        return []
    except Exception as e:
        logger.error(f"Error getting sheet responses: {str(e)}")
        return [] 