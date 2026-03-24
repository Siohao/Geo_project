from unittest.mock import patch

CALENDAR_ENDPOINTS: list = [
    "/calendar/calendar-event",
    "/calendar/event"
]

@patch("geo_project.frontend_logic.calendar.check_inserted_location")
def test_save_trip_to_calendar(mock_check, client, save_trip_to_calendar_params, mock_calendar):
    response = client.get(CALENDAR_ENDPOINTS[0], params=save_trip_to_calendar_params)
    mock_check.assert_called_once()
    mock_calendar.send_event_calendar.assert_called_once()
    assert response.status_code == 200
    assert response.json() is None