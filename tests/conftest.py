import pytest
from fastapi.testclient import TestClient
from datetime import date
from geo_project.main import app
from geo_project.frontend_logic.frontend_utils import get_overpass_service
from geo_project.frontend_logic.frontend_utils import get_weather_service


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
    
@pytest.fixture
def mock_overpass():
    return MockOverpass()

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
    
@pytest.fixture
def mock_weather():
    return MockWeatherServices()

@pytest.fixture
def client(mock_overpass, mock_weather):

    app.dependency_overrides[get_overpass_service] = lambda: mock_overpass
    app.dependency_overrides[get_weather_service] = lambda: mock_weather

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
        "lat": 35,
        "lon": 125,
        "id": 1
    }

@pytest.fixture
def weather1day_params():
    return {
        "lat": 35,
        "lon": 125,
    }

@pytest.fixture
def weather5days_params():
    return {
        "lat": 35,
        "lon": 125
    }