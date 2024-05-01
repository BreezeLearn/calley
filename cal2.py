import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarAPI:
    def __init__(self, scopes):
        self.scopes = scopes
        self.creds = None

    def authenticate(self):
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

    def list_calendars(self):
        service = build("calendar", "v3", credentials=self.creds)
        calendar_list = service.calendarList().list().execute().get("items", [])
        for calendar in calendar_list:
            print(calendar["summary"])

    def create_calendar(self, summary, timezone):
        service = build("calendar", "v3", credentials=self.creds)
        new_calendar = {"summary": summary, "timeZone": timezone}
        created_calendar = service.calendars().insert(body=new_calendar).execute()
        print(f"Created calendar: {created_calendar['id']}")

    def schedule_event(self, calendar_id, summary, description, start_datetime, end_datetime, attendee_email):
        service = build("calendar", "v3", credentials=self.creds)
        event = {
            "summary": summary,
            "location": 'online',
            "description": description,

            "start": {"dateTime": start_datetime, "timeZone": "America/Los_Angeles"},
            "end": {"dateTime": end_datetime, "timeZone": "America/Los_Angeles"},

            'attendees': [
                {'email': attendee_email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Created event: {created_event['id']}")
        return "Created event: " + created_event['id']

    def update_event(self, calendar_id, event_id, description):
        service = build("calendar", "v3", credentials=self.creds)
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        event["description"] = description
        updated_event = service.events().update(
            calendarId=calendar_id, eventId=event_id, body=event
        ).execute()
        print(f"Updated event: {updated_event['id']}")

    def delete_event(self, calendar_id, event_id):
        service = build("calendar", "v3", credentials=self.creds)
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        print(f"Deleted event: {event_id}")

    def get_upcoming_events(self):
        service = build("calendar", "v3", credentials=self.creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        result = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
            result.append({"start": start, "summary": event["summary"]})

        return result


scopes = ["https://www.googleapis.com/auth/calendar"]
api = GoogleCalendarAPI(scopes)
api.authenticate()
