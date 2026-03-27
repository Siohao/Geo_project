import pytest, os
from fastapi.testclient import TestClient
from datetime import date
from unittest.mock import MagicMock
from geo_project.main import app
from geo_project.frontend_logic.frontend_utils import (get_overpass_service,
                                                       get_weather_service,
                                                       get_calendar_service)

def pytest_configure():
    os.environ["DISABLE_CACHE"] = "1"

class MockOverpass:
    def get_viewpoints_summary(self, south, west, north, east, tags):
        return {
            "features": [
                {"id": 1, "name": "MockPeak/Viewpoint"}
            ]
        }
    
    def get_hiking_routes_summary(self, radius, lat, lon, element, tags, id):
        return {
            "routes": [
                {"id": id, "name": f"Mock route {id}"}
            ]
        }

class MockWeatherServices:
    def get_weather_summary(self,
                            lat: float,
                            lon: float,
                            ):
        return {
            "list": [
                {"dt": 1772420400, "name": "MockWeatherDay"}
            ]
        }
        
    def get_forecast_summary(   self,
                                lat: float,
                                lon: float):
        return {
            "list": [
                {"dt": 1772420400, "name": "MockWeather5Day"}
            ]
        }

class CalendarServices:
    def send_event_calendar(self,
                            lan: float,
                            lon: float,
                            id: int,
                            trip_date: date,
                            location_name:str
    ):
        return {
            'done': ''
        }
    
@pytest.fixture
def mock_overpass():
    return MockOverpass()

@pytest.fixture
def mock_weather():
    return MockWeatherServices()

@pytest.fixture
def mock_calendar():
    return MagicMock(spec=CalendarServices)

@pytest.fixture
def client(mock_overpass, mock_weather, mock_calendar):

    app.dependency_overrides[get_overpass_service] = lambda: mock_overpass
    app.dependency_overrides[get_weather_service] = lambda: mock_weather
    app.dependency_overrides[get_calendar_service] = lambda: mock_calendar

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture
def bbox_params():
    return {
        "south": 36.3655,
        "west": 127.783,
        "north": 36.3657,
        "east": 127.7834
    }

@pytest.fixture
def location_params():
    return {
        "lat": 35.0,
        "lon": 125.0,
        "id": 1
    }

@pytest.fixture
def weather1day_params():
    return {
        "lat": 35.0,
        "lon": 125.0,
    }

@pytest.fixture
def weather5days_params():
    return {
        "lat": 35.0,
        "lon": 125.0
    }

@pytest.fixture
def save_trip_to_calendar_params():
    return {
        "lat": 35.0,
        "lon": 125.0,
        "id": 2,
        "trip_date": '2026-03-12',
        "location_name": "Test"
    }

@pytest.fixture
def get_trip_from_calendar_uuid_params():
    return {
        "uuid": "abc123"
    }