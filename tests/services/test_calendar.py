import pytest
from unittest.mock import Mock, patch
from datetime import date
from typing import Dict, Any

from geo_project.services.calendar_services import CalendarServices, get_event_from_calendar_uuid

def test_make_event():
    service: CalendarServices = CalendarServices(client= Mock())
    location_name: str = "Seoul"
    url_uuid: str = "uuid123"
    date_str: date = date(2026, 3, 11)

    event: Dict[str, Any] = service.make_event(date_str, url_uuid, location_name)

    assert event["summary"] == "Hiking Event #geo"
    assert event["location"] == location_name
    assert url_uuid in event["description"]
    assert event["start"]["date"] == date_str.isoformat()
    assert event["end"]["date"] == date_str.isoformat()

@patch("geo_project.services.calendar_services.CalendarEventRepository")
@patch("geo_project.services.calendar_services.get_conn")
@patch("geo_project.services.calendar_services.release_conn")
def test_send_event_calendar(mock_release, mock_get_conn, mock_repo):
    mock_conn: Mock = Mock()
    mock_get_conn.return_value = mock_conn
    mock_release.return_value = None

    mock_repo_instance: Mock = Mock()
    mock_repo.return_value = mock_repo_instance
    mock_repo_instance.save_calendar_event_by_id.return_value = "uuid123"

    mock_client: Mock = Mock()
    mock_service: CalendarServices = CalendarServices(client=mock_client)

    mock_service.send_event_calendar(
                                    lat=10.0,
                                    lon=15.0,
                                    point_id=2,
                                    trip_date=date(2026, 3, 11),
                                    location_name="Seoul"
                                    )

    mock_repo_instance.save_calendar_event_by_id.assert_called_once_with(
                                                                        mock_conn,
                                                                        10.0,
                                                                        15.0,
                                                                        2,
                                                                        date(2026, 3, 11)
                                                                        )
    
    mock_conn.commit.assert_called_once()

    mock_client.create_calendar_event.assert_called_once()

    mock_release.assert_called_once_with(mock_conn)

@patch("geo_project.services.calendar_services.CalendarEventRepository")
@patch("geo_project.services.calendar_services.get_conn")
@patch("geo_project.services.calendar_services.release_conn")
def test_get_event_from_calendar_uuid(mock_release, mock_get_conn, mock_repo):
    mock_conn: Mock = Mock()
    mock_get_conn.return_value = mock_conn
    mock_release.return_value = None

    mock_repo_instance = Mock()
    mock_repo.return_value = mock_repo_instance
    mock_repo_instance.read_calendar_event_by_id.return_value = {"id": "uuid123"}

    event: Dict[str, Any] = get_event_from_calendar_uuid("uuid123")

    assert event["id"] == "uuid123"

    mock_repo_instance.read_calendar_event_by_id.assert_called_once_with(mock_conn, "uuid123")

    mock_release.assert_called_once_with(mock_conn)