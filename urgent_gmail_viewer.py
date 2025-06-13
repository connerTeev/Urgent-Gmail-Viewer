import os
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFontMetrics, QFont, QIcon
from email.utils import parsedate_to_datetime 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Urgent Email Viewer")
        self.setGeometry(100, 100, 800, 500)
        self.message_id_map = {}
        self.user_email = ""
        self.setup_ui()
        self.auto_refresh()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("You have urgent emails from the past 30 days:")
        bold_font = QFont()
        bold_font.setBold(True)
        self.label.setFont(bold_font)
        self.refresh_button = QPushButton("Refresh Messages")
        self.refresh_button.setIcon(QIcon("refresh.svg"))
        self.refresh_button.clicked.connect(self.show_emails)

        top_row = QHBoxLayout()
        top_row.addWidget(self.label)
        top_row.addStretch()
        top_row.addWidget(self.refresh_button)
        layout.addLayout(top_row)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

    def gmail_authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def search_urgent_messages(self, service, user_id='me', max_results=30):
        try:
            query = 'urgent OR asap OR important OR immediate OR attention'
            results = service.users().messages().list(
                userId=user_id, q=query, maxResults=max_results).execute()
            return results.get('messages', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def get_message(self, service, msg_id, user_id='me'):
        msg = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
        headers = msg['payload'].get('headers', [])
        subject = date_str = ''
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'Date':
                date_str = header['value']

        try:
            dt = parsedate_to_datetime(date_str)
            formatted_date = dt.strftime('%b %d, %Y - %I:%M %p')
        except Exception as e:
            print(f"Error parsing date: {e}")
            formatted_date = date_str
          
        return subject, formatted_date

    def make_open_email_callback(self, thread_id):
        return lambda: self.open_email_in_browser(thread_id)


    def show_emails(self):
        creds = self.gmail_authenticate()
        service = build('gmail', 'v1', credentials=creds)

        profile = service.users().getProfile(userId='me').execute()
        self.user_email = profile['emailAddress']

        messages = self.search_urgent_messages(service)

        for i in reversed(range(self.scroll_layout.count())):
            widget_to_remove = self.scroll_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        for msg in messages:
            subject, date = self.get_message(service, msg['id'])
            thread_id = msg['threadId']
            full_text = f"{date} - {subject}"

            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(5, 5, 5, 5)

            label = QLabel()
            font_metrics = QFontMetrics(label.font())
            elided_text = font_metrics.elidedText(full_text, Qt.ElideRight, 600)
            label.setText(elided_text)
            label.setToolTip(full_text)
            label.setMaximumWidth(600)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            row_layout.addWidget(label, stretch=1)

            visit_btn = QPushButton("Visit")
            visit_btn.clicked.connect(self.make_open_email_callback(thread_id))
            row_layout.addWidget(visit_btn)

            row_widget.setLayout(row_layout)
            self.scroll_layout.addWidget(row_widget)

    def open_email_in_browser(self, thread_id):
        if thread_id and self.user_email:
            url = f"https://mail.google.com/mail/?authuser={self.user_email}#inbox/{thread_id}"
            webbrowser.open(url)
        else:
            print("Could not open email — thread ID or user email missing.")

    def auto_refresh(self):
        self.show_emails()
        QTimer.singleShot(60000, self.auto_refresh)  # Refresh every 60 seconds

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = GmailApp()
    window.show()
    sys.exit(app.exec_())
