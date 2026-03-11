from fastapi import APIRouter, Depends
from typing import Dict, Any
from geo_project.services.map_services import OverPass
from geo_project.frontend_logic.frontend_utils import (
                            get_overpass_service,
                            check_inserted_coordinates, 
                            check_inserted_location, 
                            elements, 
                            tags_peak, 
                            tags_routes, 
                            tags_hiking_routes, 
                            tags_viewpoint)

router = APIRouter(prefix="/OSM", tags=["osm"])

@router.get("/peaks")
def get_mount_peaks_from_box(south: float,
                             west: float,
                             north: float,
                             east: float,
                             service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_coordinates(south, west, north, east)
    data: Dict[str, Any] = service.get_viewpoints_summary(south, west, north, east, tags=tags_peak)
    return data

@router.get("/viewpoints")
def get_viewpoints_from_box(south: float,
                             west: float,
                             north: float,
                             east: float,
                             service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_coordinates(south, west, north, east)
    data: Dict[str, Any] = service.get_viewpoints_summary(south, west, north, east, tags=tags_viewpoint)
    return data

@router.get("/routes")
def get_mount_trails(lat: float,
                     lon: float,
                     id: int,
                     service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_location(lat, lon)
    data: Dict[str, Any] = service.get_hiking_routes_summary(2000, lat, lon, elements[1], tags_hiking_routes, id)
    return data

@router.get("/premade_routes")
def get_mount_trails(lat: float,
                     lon: float,
                     id: int,
                     service: OverPass = Depends(get_overpass_service)) -> Dict[str, Any]:
    
    check_inserted_location(lat, lon)
    data: Dict[str, Any] = service.get_hiking_routes_summary(5000, lat, lon, elements[3], tags_routes, id)
    return data