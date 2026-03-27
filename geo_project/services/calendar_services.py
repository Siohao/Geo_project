from datetime import date
from typing import Dict, Any

from geo_project.storage.storage import CalendarEventRepository
from geo_project.calendar.geo_calendar import CalendarApi
from geo_project.storage.db import get_conn, release_conn
from geo_project.storage.cache import cache



class CalendarServices:

    def __init__(self, client: CalendarApi):
        self.client = client

    def make_event (self, trip_date: date, url_uuid: str, location_name: str):
        date_str = trip_date.isoformat()
        return {
            'summary': 'Hiking Event #geo',
            'location': f'{location_name}',
            'description': f'Trip: http://localhost:5500/?event_id={url_uuid}',
            'start': {
                'date': date_str,
            },
            'end': {
                'date': date_str,
            },
        }

    def send_event_calendar (self, lat: float, lon: float, point_id: int, trip_date: date, location_name: str):

        conn: Any = get_conn()
        try:
            calendar_service = CalendarEventRepository()

            url_uuid: str = calendar_service.save_calendar_event_by_id(conn, lat, lon, point_id, trip_date)

            conn.commit()

            event_dict: Dict[str, Any] = self.make_event(trip_date=trip_date, url_uuid=url_uuid, location_name=location_name)

            self.client.create_calendar_event(event_dict)

        except Exception:
            conn.rollback()
            raise
        finally:
            release_conn(conn)

def get_event_from_calendar_uuid (uuid: str) -> Dict[str, Any]:
    conn: Any = get_conn()
    try:
        calendar_service: CalendarEventRepository = CalendarEventRepository()
        data: Dict[str, Any] = calendar_service.read_calendar_event_by_id(conn, uuid)
        return data
    except Exception:
        conn.rollback()
        raise
    finally:
        release_conn(conn)