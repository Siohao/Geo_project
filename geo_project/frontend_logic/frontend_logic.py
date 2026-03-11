from fastapi import Depends
from geo_project.services.map_services import OverPass
from geo_project.services.weather_services import WeatherServices
from geo_project.services.calendar_services import CalendarServices
from typing import Dict, Any
from datetime import date
from geo_project.services.calendar_services import get_event_from_calendar_uuid
# from geo_project.frontend_logic.frontend_utils import (app, 
#                             get_overpass_service, 
#                             get_weather_service, 
#                             get_calendar_service, 
#                             check_inserted_coordinates, 
#                             check_inserted_location, 
#                             elements, 
#                             tags_peak, 
#                             tags_routes, 
#                             tags_hiking_routes, 
#                             tags_viewpoint)

from fastapi import FastAPI, Depends, HTTPException
from geo_project.services.map_services import OverPass
from geo_project.services.weather_services import WeatherServices
from geo_project.services.calendar_services import CalendarServices
from fastapi.middleware.cors import CORSMiddleware
from geo_project.calendar.geo_calendar import CalendarApi
from geo_project.api.api import WeatherMapClient
from geo_project.api.api import OSMOverpass
from geo_project.calendar.oauth_utils import geo_calendar_oauth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Lub konkretny adres frontendu
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_overpass_service():
    omsclient = OSMOverpass()
    return OverPass(omsclient)

def get_weather_service():
    client = WeatherMapClient()
    return WeatherServices(client)

def get_calendar_credentials():
    return geo_calendar_oauth()

def get_calendar_client(
    creds = Depends(get_calendar_credentials)
):
    return CalendarApi(creds)

def get_calendar_service(
    client: CalendarApi = Depends(get_calendar_client)
):
    return CalendarServices(client)

elements: list[str] = ["node", "way", "area", "relation"]

#node
tags_peak = {
    "natural": "peak"
}

#node
tags_viewpoint = {
    "tourism": "viewpoint"
    # "tourism": "attraction"
}

#relation
tags_routes = {
    # "highway": "path",
    # "sac_scale": None,
    "route": "hiking"
}

#way
tags_hiking_routes = {
    "highway": ["path", "steps", "track"]
}


def check_inserted_coordinates(south: float, west: float, north: float, east: float) -> bool:
    MAXDiff: float = 0.08
    if ((north < south or east < west) or
        (north - south > MAXDiff or east - west > MAXDiff) or
        (north > 38.612 or south < 33.106 or east > 131.872 or west < 124.609)  #The border coordinates of South Korea
        ):
        raise HTTPException(status_code=400, detail="Coordinates outside of South Korea or bbox too big.")

def check_inserted_location(lat: float, lon: float) -> bool:
    if (lat > 38.612 or lat < 33.106 or lon > 131.872 or lon < 124.609):  #The border coordinates of South Korea
        raise HTTPException(status_code=400, detail="Coordinates outside of South Korea.")


@app.get("/OSM/peaks")
def get_mount_peaks_from_box(south: float,
                             west: float,
                             north: float,
                             east: float,
                             service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_coordinates(south, west, north, east)
    data: Dict[str, Any] = service.get_viewpoints_summary(south, west, north, east, tags=tags_peak)
    return data

@app.get("/OSM/viewpoints")
def get_viewpoints_from_box(south: float,
                             west: float,
                             north: float,
                             east: float,
                             service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_coordinates(south, west, north, east)
    data: Dict[str, Any] = service.get_viewpoints_summary(south, west, north, east, tags=tags_viewpoint)
    return data

@app.get("/OSM/routes")
def get_mount_trails(lat: float,
                     lon: float,
                     id: int,
                     service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_location(lat, lon)
    data: Dict[str, Any] = service.get_hiking_routes_summary(2000, lat, lon, elements[1], tags_hiking_routes, id)
    return data

@app.get("/OSM/premade_routes")
def get_mount_trails(lat: float,
                     lon: float,
                     id: int,
                     service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_location(lat, lon)
    data: Dict[str, Any] = service.get_hiking_routes_summary(5000, lat, lon, elements[3], tags_routes, id)
    return data

@app.get("/OWM/weather_day_of_trip")
def get_weather_for_trail_day(lat: float,
                              lon: float,
                              trip_date: date,
                              owm_service: WeatherServices = Depends(get_weather_service)) -> Dict[str, Any]:
    
    check_inserted_location(lat, lon)
    data: Dict[str, Any] = owm_service.get_weather_summary(lat, lon)
    return data

@app.get("/OWM/day_weather_forecast")
def get_forecast_summary_for_5days(lat: float,
                                   lon: float,
                                   owm_service: WeatherServices = Depends(get_weather_service)) -> Any:
    
    check_inserted_location(lat, lon)
    data: Any = owm_service.get_forecast_summary(lat, lon)
    return data


@app.get("/calendar/calendar_event")
def save_trip_to_calendar(lat: float,
                          lon: float,
                          id: int,
                          trip_date: date,
                          location_name: str,
                          calendar_service: CalendarServices = Depends(get_calendar_service)) -> Any:
    
    check_inserted_location(lat, lon)
    data: Any = calendar_service.send_event_calendar(lat, lon, id, trip_date, location_name)
    return None

@app.get("/calendar/event")
def get_trip_from_calendar_uuid (uuid: str) -> Any:
    data: Dict[str, Any] = get_event_from_calendar_uuid(uuid)
    return data