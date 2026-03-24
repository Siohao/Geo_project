from typing import Dict, Any
from googleapiclient.discovery import build
from geo_project.geo_config.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_fixed

logger = get_logger(__name__)

class CalendarApi:
    
  def __init__(self, creds):
        self.service = build("calendar", "v3", credentials=creds)

  @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
  def create_calendar_event(self, event: Dict[str, Any]):

    try:
      save_event = self.service.events().insert(calendarId='primary', body=event).execute()
    except Exception as e:
      logger.error(f"Event creation error: {e}")
      raise
    
    logger.info('Event created: %s' % (save_event.get('htmlLink')))