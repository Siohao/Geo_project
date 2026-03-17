from typing import Any, Dict, Union
from osmtogeojson import osmtogeojson
import requests
import os
import time
from geo_project.geo_config.logger import get_logger

logger = get_logger(__name__)

headers = {
    'User-Agent': 'PythonOSMClient/1.0'
}

class GoogleMapsClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def get_directions (self, origin: str, destination: str, mode: str) -> Dict[str, Any]:
        url: str = "https://maps.googleapis.com/maps/api/directions/json"
        params: Dict[str, str] = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "key": self.api_key
        }

        try:
            response: Dict[str, Any] = requests.get(url, params = params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Błąd pobierania danych:", e)
            return {
                "geocoded_waypoints": [],
                "routes": [],
                "status": "ERROR",
                "message": str(e)
            }    
    
    def get_poi (self, lat: float, lon: float, rad: int, max_res: int, inc_types: list[str]) -> Dict[str, Any]:

        url: str = "https://places.googleapis.com/v1/places:searchNearby"

        fields = [
            "places.id",
            "places.displayName",
            "places.location",
            "places.types",
            "places.viewport",
            "places.googleMapsUri"
        ]

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": ",".join(fields)
        }

        data = {
            "includedTypes": inc_types,
            "maxResultCount": max_res,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lon
                    },
                    "radius": rad
                }
            }
        }

        try:
            response: Dict[str, Any] = requests.post(url, headers = headers,json = data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Błąd pobierania danych:", e)
            return {
                "results": [],
                "status": "ERROR",
                "message": str(e)
            }   

    def fake_get_directions(self, origin: str, destination: str, mode: str) -> Dict[str, Any]:
        return {
            "status": "OK",
            "routes": [
                {
                    "legs": [
                        {
                            "distance": {"text": "10 km"},
                            "duration": {"text": "15 mins"}
                        }
                    ]
                }
            ]
        }
    

class WeatherMapClient:

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")

    def get_weather(self, lat: str, lon: str) -> Dict[str, Any]:
        
        # url: str = "https://api.openweathermap.org/data/2.5/weather"
        url: str = "https://api.openweathermap.org/data/2.5/forecast"

        params: Dict [str, str] = {
            "lat": lat,
            "lon":  lon,
            #"exclude": "current,minutely,hourly,alerts",
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        try:
            response: Dict [str, Any] = requests.get(url, params = params, timeout = 5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Błąd pobierania danych:", e)
            return {
            "cod": "401",
            "message": str(e)
            }
    

    def get_air_pollution(self, lat: str, lon: str) -> Dict[str, Any]:

        url: str = "http://api.openweathermap.org/data/2.5/air_pollution"

        params: Dict[str, str] = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }

        try:
            response: Dict[str, Any] = requests.get(url, params = params, timeout = 5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Błąd pobierania danych:", e)
            return {
                "coord": {},
                "list": [],
                "cod": "REQUEST_FAILED",
                "message": str(e)
            }
    

class OSMOverpass:

    overpass_url = os.getenv("OVERPASS_URL", "http://overpass_sk/api/interpreter")

    def __init__(self):
        pass

    def get_hiking_routes(self, radius: int, lon: float, lat: float, element: str, tags: Dict[str, Union[str, list[str], None]]) -> Dict[str, Any]:

        tags_query = ""

        for key, value in tags.items():
            if value is None:
                #For key with None value
                tags_query += f'{element}(around:{radius},{lon},{lat})["{key}"];'

            elif isinstance(value, list):
                #For key with multiple values
                regex = "|".join(value)
                tags_query += f'{element}(around:{radius},{lon},{lat})["{key}"~"{regex}"];'

            else:
                #For key with only one value
                tags_query += f'{element}(around:{radius},{lon},{lat})["{key}"="{value}"];'
        
        query = f"""
            [out:json][timeout:60];
            (
            {tags_query}
            ); 
            (._;>;);
            out geom;
            """
        
        try:
            response: Dict[str, Any] = requests.post(self.overpass_url, data=query)
            response.raise_for_status()
            geo_response = osmtogeojson.process_osm_json(response.json())
            return geo_response
        except requests.RequestException as e:
            logger.error("Błąd pobierania danych:", e)
            return {
                "type": "",
                "features": [],
                "message": str(e)
            }

    def get_viewpoints(self, south: float, west: float, north: float, east: float, tags: Dict[str, str]) -> Dict[str, Any]:

        tags_query = "\n".join(
            f'["{key}"="{value}"]'
            for key, value in tags.items()
        )

        timestamp = int(time.time())
        query = f"""
            [out:json][timeout:60];
            // query_id: {timestamp}
            (
                node({south},{west},{north},{east})
                {tags_query};
            );
            out body;
            """
        try:
            response: Dict[str, Any] = requests.post(self.overpass_url, query, headers= headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Błąd pobierania danych:", e)
            return {
                "elements": [],
                "message": str(e)
            }