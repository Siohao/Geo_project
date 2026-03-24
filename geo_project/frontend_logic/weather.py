from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import date
from geo_project.services.weather_services import WeatherServices
from geo_project.frontend_logic.frontend_utils import (
                            get_weather_service, 
                            check_inserted_location)

router = APIRouter(prefix="/owm", tags=["owm"])

@router.get("/weather-day-of-trip")
def get_weather_for_trail_day(lat: float,
                              lon: float,
                              owm_service: WeatherServices = Depends(get_weather_service)) -> Dict[str, Any]:
    
    check_inserted_location(lat, lon)
    data: Dict[str, Any] = owm_service.get_weather_summary(lat, lon)
    return data

@router.get("/day-weather-forecast")
def get_forecast_summary_for_5days(lat: float,
                                   lon: float,
                                   owm_service: WeatherServices = Depends(get_weather_service)) -> Any:
    
    check_inserted_location(lat, lon)
    data: Any = owm_service.get_forecast_summary(lat, lon)
    return data