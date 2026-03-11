from pydantic import BaseModel
from typing import Dict, Any

class MapResponse(BaseModel):
    distance: str
    duration: str

    @classmethod
    def parse_map(cls, response: Dict) -> MapResponse:
        return cls(
            distance = response["routes"][0]["legs"][0]["distance"]["text"],
            duration = response["routes"][0]["legs"][0]["duration"]["text"]
        )
    
class POI(BaseModel):
    place_id: str
    name: str
    latitude: float
    longitude: float
    place_type: list[str]
    place_url: str
    
class MapResponsePOI(BaseModel):
    places: list[POI]

    @classmethod
    def parse_poi(cls, response: Dict[str, Any]) -> MapResponsePOI:

        parsed_places: list[POI] = []

        for place in response.get("places", []):
            parsed_places.append(
                POI(
                    place_id =      place.get("id"),
                    name =          place.get("displayName",{}).get("text"),
                    latitude =      place.get("location", {}).get("latitude"),
                    longitude =     place.get("location", {}).get("longitude"),
                    place_type =    place.get("types", []),
                    place_url =     place.get("googleMapsUri")
                )
            )

        return cls(places = parsed_places)

class OSMPointsResponse(BaseModel):

    @classmethod
    def parse_oms_points(cls, response: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [point.get("lon"), point.get("lat")]},
                    "properties": {"Name": (point.get("tags", {}).get("name:en") or
                                            point.get("tags", {}).get("name") or
                                            "Unknown"),
                                    "Id": point.get("id"),
                                    "Height": point.get("tags", {}).get("ele"),
                                    "Type": (point.get("tags", {}).get("natural") or
                                             point.get("tags", {}).get("tourism"))
                                    }
                } for point in response.get("elements", [])
            ]
        }