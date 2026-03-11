from typing import Dict, Any
from googleapiclient.discovery import build

class CalendarApi:
    
  def __init__(self, creds):
        self.service = build("calendar", "v3", credentials=creds)

  def create_calendar_event(self, event: Dict[str, Any]):

    save_event = self.service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (save_event.get('htmlLink')))