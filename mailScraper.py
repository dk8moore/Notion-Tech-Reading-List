import config
import google.auth
from googleapiclient.discovery import build

# Authenticate with Gmail API
credentials, _ = google.auth.default()
service = build('gmail', 'v1', credentials=credentials)

# List unread emails
results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
messages = results.get('messages', [])

if not messages:
    print('No unread messages found.')
else:
    print('Unread messages:')
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        print(f'Subject: {msg["subject"]}')
        # Process the email content here

# Add further processing logic for email content
