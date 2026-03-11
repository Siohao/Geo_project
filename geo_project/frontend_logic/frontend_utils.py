from fastapi import Depends, HTTPException
from geo_project.services.map_services import OverPass
from geo_project.services.weather_services import WeatherServices
from geo_project.services.calendar_services import CalendarServices
from geo_project.calendar.geo_calendar import CalendarApi
from geo_project.api.api import WeatherMapClient
from geo_project.api.api import OSMOverpass
from geo_project.calendar.oauth_utils import geo_calendar_oauth

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
    if ((lat > 38.612 or lat < 33.106 or lon > 131.872 or lon < 124.609)):  #The border coordinates of South Korea
        raise HTTPException(status_code=400, detail="Coordinates outside of South Korea.")