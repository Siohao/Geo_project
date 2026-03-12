from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class WeatherResponse(BaseModel):
    main: str
    description: str
    clouds_all: int
    temp: float
    temp_feels_like: float
    pressure: int
    humidity: int
    visibility: int
    wind_speed: float
    wind_deg: int
    sys_sunrise: int
    sys_sunset: int

    @classmethod
    def parse_weather(cls, response: Dict[str, str|int|float]) -> "WeatherResponse":
        return cls(
            main =              response["weather"][0]["main"],
            description =       response["weather"][0]["description"],
            clouds_all =        response["clouds"]["all"],
            temp =              response["main"]["temp"],
            temp_feels_like =   response["main"]["feels_like"],
            pressure =          response["main"]["pressure"],
            humidity =          response["main"]["humidity"],
            visibility =        response["visibility"],
            wind_speed =        response["wind"]["speed"],
            wind_deg =          response["wind"]["deg"],
            sys_sunrise =       response["sys"]["sunrise"],
            sys_sunset =        response["sys"]["sunset"]
        )

class ForecastResponse(BaseModel):
    response_utc_time: str
    response_local_time: str
    forecast_timezone: int
    city_id: int
    city_name: str
    longitude: float
    latitude: float

class ForecastItems(BaseModel):   
    local_time: list[str]
    temp: list[float]
    temp_feels_like: list[float]
    pressure: list[int]
    humidity: list[int]
    weather_id: list[int]
    weather_main: list[str]
    weather_description: list[str]
    clouds_all: list[int]
    wind_speed: list[float]
    wind_deg: list[int]
    visibility: list[int]
    rain_3h: list[float]

class ForecastSummary(BaseModel):
     forecast_info: list[ForecastResponse]
     forecast_items: list[ForecastItems]
        
class AirPollutionResponse(BaseModel):
    aqi: int
    aqi_symbol: str

    @classmethod
    def parse_air_pollution(cls, response: Dict[str, int]) -> "AirPollutionResponse":

        return cls(
            aqi =  response["list"][0]["main"]["aqi"],
            aqi_symbol = ""
        )