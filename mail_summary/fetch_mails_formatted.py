from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import quopri
from datetime import datetime, timedelta

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails(time_interval):
    # Variable creds will store the user access token.
    creds = None

    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('token.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # Calculate the date for the query
    since_date = (datetime.now() - timedelta(hours=time_interval)).strftime('%Y/%m/%d')

    # Request a list of all the messages received since the calculated date
    result = service.users().messages().list(userId='me', q=f'after:{since_date}').execute()

    # Create an empty list to store the emails
    emails = []

    # Iterate through all the messages
    for msg in result.get('messages', []):
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject, Sender Email, and Time in the headers
            subject = next((d['value'] for d in headers if d['name'] == 'Subject'), '')
            sender = next((d['value'] for d in headers if d['name'] == 'From'), '')
            time = next((d['value'] for d in headers if d['name'] == 'Date'), '')

            # Decode the body of the message
            parts = payload.get('parts', [])
            if parts:
                data = parts[0]['body']['data']
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                soup = BeautifulSoup(decoded_data, 'html.parser')
                body = ' '.join(soup.get_text().split())
            else:
                body = "No content"

            # Add the email to the list
            emails.append({
                'Subject': subject,
                'From': sender,
                'Time': time,
                'Message': body
            })
        except Exception as e:
            print(f"Error processing email: {e}")

    # Return the list of emails
    return emails
