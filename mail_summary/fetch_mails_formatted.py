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

def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
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

    # Get the date 24 hours ago
    date = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')

    # request a list of all the messages received in the last 24 hours
    result = service.users().messages().list(userId='me', q=f'after:{date}').execute()

    # messages is a list of dictionaries where each dictionary contains a message id.
    # iterate through all the messages
    for msg in result.get('messages', []):
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject, Sender Email, and Time in the headers
            subject = next((d['value'] for d in headers if d['name'] == 'Subject'), '')
            sender = next((d['value'] for d in headers if d['name'] == 'From'), '')
            time = next((d['value'] for d in headers if d['name'] == 'Date'), '')

            # The Body of the message is in Encoded format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")

            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')

            # Now, the data obtained is in text format.
            soup = BeautifulSoup(decoded_data, 'html.parser')
            body = ' '.join(soup.get_text().split())

            # Printing the subject, sender's email, time, and message
            print("Subject: ", subject)
            print("From: ", sender)
            print("Time: ", time)
            print("Message: ", body)
            print('\n')
        except Exception as e:
            print(f"Error processing email: {e}")

getEmails()