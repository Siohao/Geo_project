import pytest

@pytest.mark.parametrize("endpoint", ["/owm/weather-day-of-trip"])
def test_weather_for_trail_day(client, weather1day_params, endpoint):
    response = client.get(endpoint, params= weather1day_params)
    assert response.status_code == 200
    data = response.json()
    assert "list" in data

@pytest.mark.parametrize("endpoint", ["/owm/day-weather-forecast"])
def test_forecast_summary_for_5days(client, weather5days_params, endpoint):
    response = client.get(endpoint, params=weather5days_params)
    assert response.status_code == 200
    data = response.json()
    assert "list" in data