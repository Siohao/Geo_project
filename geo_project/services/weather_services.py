from geo_project.api.api import WeatherMapClient
from geo_project.storage.storage import WeatherRepository
from geo_project.models.weather_models import ForecastResponse, ForecastItems, ForecastSummary, WeatherResponse, AirPollutionResponse
from geo_project.storage.db import get_conn, release_conn
from typing import Dict, Any
from datetime import timezone, timedelta, datetime
from dataclasses import asdict, dataclass
from collections import defaultdict
import json


@dataclass
class WeatherAirSummary:
    weather: WeatherResponse
    air_pollution: AirPollutionResponse

class WeatherServices:

    def __init__(self, client: WeatherMapClient):
        self.client = client

    def aqi_symbol(self, aqi: int) -> str:
            return {
                1: "🍃",
                2: "🙂",
                3: "😷",
                4: "🤢",
                5: "☠️"
            }.get(aqi, "🌫️")

    def get_weather_summary(self, lat: str, lon: str) -> WeatherAirSummary:
        weather_summary: Dict[str, Any] = self.client.get_weather(lat, lon)
        air_summary: Dict[str, Any] = self.client.get_air_pollution(lat, lon)

        weather_obj: object = WeatherResponse.parse_weather(weather_summary)
        air_obj: object = AirPollutionResponse.parse_air_pollution(air_summary)

        air_obj.aqi_symbol = self.aqi_symbol(air_obj.aqi)

        w_a_summary =  WeatherAirSummary(weather_obj, air_obj)
    
        return asdict(w_a_summary)
    
    def get_forecast_summary(self, lat:str, lon: str) -> Any:
         
        forecast_summary: Dict[str, Any] = self.client.get_weather(lat, lon)
        timezone_forecast: int = forecast_summary["city"]["timezone"]
        forecast_response_actual_time: datetime = datetime.now(timezone.utc)
        forecast_response_local_time: datetime = datetime.now(timezone.utc) + timedelta(seconds=timezone_forecast)

        with open("test_test.json", "w", encoding="utf-8") as f:
        #     ######## .model_dump() -> zmiana z obiektu klasy na dict
            json.dump(forecast_summary, f, ensure_ascii=False, indent=2)
        #     # json.dump(data.model_dump(), f, ensure_ascii=False, indent=2)
            print("Zapisano")
        print("koniec")

        response: list[ForecastResponse] = []
        items: list[ForecastItems] = []
        hours: list[int] = [6,12,18]

        daily_data = defaultdict(lambda: {
            "local_times": [], "temp": [], "temp_feels_like": [], "pressure": [],
            "humidity": [], "weather_id": [], "weather_main": [],
            "weather_description": [], "clouds_all": [], "wind_speed": [],
            "wind_deg": [], "visibility": [], "rain_3h": []
        })

        for entry in forecast_summary["list"]:
            dt_utc: datetime = datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
            dt_local: datetime = dt_utc + timedelta(seconds=timezone_forecast)
            
            if dt_local.hour not in hours:
                continue

            date_str: str = dt_local.strftime("%Y-%m-%d")
            day: defaultdict = daily_data[date_str]

            day["local_times"].append(dt_local)
            day["temp"].append(entry["main"]["temp"])
            day["temp_feels_like"].append(entry["main"]["feels_like"])
            day["pressure"].append(entry["main"]["pressure"])
            day["humidity"].append(entry["main"]["humidity"])
            day["weather_id"].append(entry["weather"][0]["id"])
            day["weather_main"].append(entry["weather"][0]["main"])
            day["weather_description"].append(entry["weather"][0]["description"])
            day["clouds_all"].append(entry["clouds"]["all"])
            day["wind_speed"].append(entry["wind"]["speed"])
            day["wind_deg"].append(entry["wind"]["deg"])
            day["visibility"].append(entry.get("visibility", 0))
            day["rain_3h"].append(entry.get("pop", 0.0))

        for date_str, data in daily_data.items():

            items.append(ForecastItems(
                local_time =            [dt.isoformat() for dt in data["local_times"]],
                temp =                  data["temp"],
                temp_feels_like =       data["temp_feels_like"],
                pressure =              data["pressure"],
                humidity =              data["humidity"],
                weather_id =            data["weather_id"], 
                weather_main =          data["weather_main"],
                weather_description =   data["weather_description"],
                clouds_all =            data["clouds_all"],
                wind_speed =            data["wind_speed"],
                wind_deg =              data["wind_deg"],
                visibility =            data["visibility"],
                rain_3h =               data["rain_3h"]
            ))

        
        response.append(ForecastResponse(
            response_utc_time =     forecast_response_actual_time.isoformat(),
            response_local_time =   forecast_response_local_time.isoformat(),
            forecast_timezone =     timezone_forecast,
            city_id =               forecast_summary["city"]["id"],
            city_name =             forecast_summary["city"]["name"],
            longitude =             forecast_summary["city"]["coord"]["lon"],
            latitude =              forecast_summary["city"]["coord"]["lat"]
        ))

        forecast_obj: ForecastSummary = ForecastSummary(forecast_info= response, forecast_items= items)
        forecast_json: Dict[str, Any] = forecast_obj.model_dump()


        utc_time: datetime = forecast_json["forecast_info"][0]["response_utc_time"]
        forecast_lon: float = forecast_json["forecast_info"][0]["longitude"]
        forecast_lat: float = forecast_json["forecast_info"][0]["latitude"]

        conn = get_conn()
        try:
            repo = WeatherRepository()

            check: Any = repo.check_weather_cache(conn, forecast_lon, forecast_lat)

            if(check):
                return check
            else:
                repo.save_weather(conn, forecast_lon, forecast_lat, utc_time, forecast_json)
                conn.commit()
                return repo.check_weather_cache(conn, forecast_lon, forecast_lat)
        except Exception:
            conn.rollback()
            raise
        finally:
            release_conn(conn)