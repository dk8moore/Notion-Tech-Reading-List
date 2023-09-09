import os.path
import json, base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']


def main():

  creds = authenticate()
  
  try:
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    # List unread emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])

    if not messages:
      print('No unread messages found.')
    else:
      print('Unread messages:')
      for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        good_msg = {}
        # Headers handler
        for header in msg['payload']['headers']:
          if header['name'] in ['From', 'Subject', 'Date']:
            good_msg[header['name'].lower()] = header['value']
        # good_msg['body'] = base64.b64decode(msg['payload']['body'])
        # Body handler: body could be split into parts if the email is too long
        # AFAIK if the body object has no attribute "data", then there's another attribute "parts" containing all the parts (you don't say?!) of the body into other body objects
        if 'data' in msg['payload']['body']:
          good_msg['body'] = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
        else:
          good_msg['body'] = ''
          for part in msg['payload']['parts']:
            good_msg['body'] += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f'An error occurred: {error}')


def authenticate():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
      token.write(creds.to_json())
  return creds


if __name__ == '__main__':
  main()