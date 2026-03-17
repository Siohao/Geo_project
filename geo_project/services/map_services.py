from geo_project.api.api import GoogleMapsClient
from geo_project.api.api import OSMOverpass
from geo_project.models.map_models import MapResponse
from geo_project.models.map_models import MapResponsePOI
from geo_project.models.map_models import OSMPointsResponse
from typing import Dict, Any, Union
from geo_project.storage.storage import PlacesRepository
from geo_project.storage.db import get_conn, release_conn

class MapServices: 

    def __init__ (self, client: GoogleMapsClient):
        self.client = client

    def get_route_summary(self, origin: str, destination: str, mode: str) -> MapResponse:
        # route_summary = self.client.get_directions(origin, destination, mode)
        route_summary: Dict[str, Any]= self.client.fake_get_directions(origin, destination, mode)

        if (route_summary["status"]) != "OK":
            return "Error"

        return MapResponse.parse_map(route_summary)
    
    def get_poi_summary(self, lat: float, lon: float, rad: int, max_res: int, inc_types: list[str]) -> MapResponsePOI:
        
        poi_summary: Dict[str, Any] = self.client.get_poi(lat, lon, rad, max_res, inc_types)
        
        return MapResponsePOI.parse_poi(poi_summary)

class OverPass:

    def __init__(self, client: OSMOverpass):
        self.client = client

    def get_hiking_routes_summary(self, radius: int, lon: float, lat: float, element: str, tags: Dict[str, Union[str, list[str], None]], id: int) -> Dict[str, Any]:
        
        conn: Any = get_conn()
        try:
            repo: PlacesRepository = PlacesRepository()
            
            if (repo.check_trails_for_point_in_db(conn, id)):
                hiking_routes_summary: Dict[str, Any] = self.client.get_hiking_routes(radius, lon, lat, element, tags)

                repo.save_trails(conn, hiking_routes_summary)
                repo.update_last_check_for_point(conn, id)

            conn.commit()
                
            db_routes: Dict[str, Any] = repo.read_trails(conn, radius, lon, lat)

            return db_routes
        
        except Exception:
            conn.rollback()
            raise
        finally:
            release_conn(conn)

    
    def get_viewpoints_summary(self, south: float, west: float, north: float, east: float, tags: Dict[str, str]) -> OSMPointsResponse:

        viewpoints_summary: Dict[str, Any] = self.client.get_viewpoints(south, west, north, east, tags=tags)
        viewpoints_parsed: OSMPointsResponse = OSMPointsResponse.parse_osm_points(viewpoints_summary)

        conn: Any = get_conn()

        try:
            repo: PlacesRepository = PlacesRepository()
            repo.save_many_points(conn, viewpoints_parsed)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            release_conn(conn)

        return viewpoints_parsed