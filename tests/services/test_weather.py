from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import Any
import pytest

from geo_project.services.weather_services import (WeatherAirSummary,
                                                   WeatherServices)

@dataclass
class DummyAir:
        aqi: int
        aqi_symbol: str = ""
@dataclass
class DummyWeather:
     pass

@patch("geo_project.services.weather_services.WeatherResponse.parse_weather")
@patch("geo_project.services.weather_services.AirPollutionResponse.parse_air_pollution")
def test_get_weather_summary(mock_parse_air, mock_parse_weather):
    mock_client: Mock = Mock()
    mock_service: WeatherServices = WeatherServices(client=mock_client)

    mock_client.get_weather.return_value = {"w_summary": "w"}
    mock_client.get_air_pollution.return_value = {"a_summary": "a"}

    mock_parse_weather.return_value = DummyWeather()
    mock_parse_air.return_value = DummyAir(3)

    with patch.object(mock_service, "aqi_symbol", return_value="😷"):
        result: WeatherAirSummary = mock_service.get_weather_summary(
            "10.0", "20.0"
        )

        mock_client.get_weather.assert_called_once()
        mock_client.get_air_pollution.assert_called_once()
        mock_parse_weather.assert_called_once()
        mock_parse_air.assert_called_once()
        mock_service.aqi_symbol.assert_called_once()
        assert result["air_pollution"]["aqi_symbol"] == "😷"

@pytest.mark.parametrize(
    "data_in_db", (True, False)
)
@patch("geo_project.services.weather_services.WeatherRepository")
@patch("geo_project.services.weather_services.release_conn")
@patch("geo_project.services.weather_services.get_conn")
def test_forecast_summary(mock_get_conn, mock_release_conn, mock_repo, data_in_db):
    mock_conn: Mock = Mock()
    mock_get_conn.return_value = mock_conn
    mock_release_conn.return_value = None

    mock_repo_instance: Mock = Mock()
    mock_repo.return_value = mock_repo_instance

    mock_client: Mock = Mock()
    mock_service: WeatherServices = WeatherServices(client=mock_client)

    mock_client.get_weather.return_value = {
        "city": {
            "id": 123,
            "name": "TestCity",
            "coord": {"lon": 10.0, "lat": 50.0},
            "timezone": 3600  # +1h
        },
        "list": [
            {
                "dt": 1678920000,  # przykładowy timestamp UTC
                "main": {"temp": 15, "feels_like": 14, "pressure": 1012, "humidity": 80},
                "weather": [{"id": 500, "main": "Rain", "description": "light rain"}],
                "clouds": {"all": 90},
                "wind": {"speed": 5, "deg": 180},
                "visibility": 10000,
                "pop": 0.2
            },
            # można dodać więcej wpisów w różnych godzinach do testu filtracji
        ]
    }

    if data_in_db:
        mock_repo_instance.check_weather_cache.return_value = data_in_db
    else:
        mock_repo_instance.check_weather_cache.side_effect = [
            None,
            {"forecast_test"}
        ]

    mock_repo_instance.save_weather.return_value = None

    result: Any = mock_service.get_forecast_summary(
        10.0, 20.0
    )

    if data_in_db:
        mock_repo_instance.check_weather_cache.assert_called_once()
        mock_repo_instance.save_weather.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_release_conn.assert_called_once_with(mock_conn)
    else:    
        assert mock_repo_instance.check_weather_cache.call_count == 2
        mock_repo_instance.save_weather.assert_called_once()
        mock_conn.commit.assert_called_once()

    mock_release_conn.assert_called_once_with(mock_conn)

    assert result == data_in_db or result == {"forecast_test"}