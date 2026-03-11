from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import date
from geo_project.services.calendar_services import CalendarServices
from geo_project.services.calendar_services import get_event_from_calendar_uuid
from geo_project.frontend_logic.frontend_utils import (
                            get_calendar_service, 
                            check_inserted_location)

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/calendar_event")
def save_trip_to_calendar(lat: float,
                          lon: float,
                          id: int,
                          trip_date: date,
                          location_name: str,
                          calendar_service: CalendarServices = Depends(get_calendar_service)) -> Any:
    
    check_inserted_location(lat, lon)
    data: Any = calendar_service.send_event_calendar(lat, lon, id, trip_date, location_name)
    return None

@router.get("/event")
def get_trip_from_calendar_uuid (uuid: str) -> Any:
    data: Dict[str, Any] = get_event_from_calendar_uuid(uuid)
    return data