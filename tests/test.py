import requests
import json
from typing import Dict, Any

url: str = "https://maps.googleapis.com/maps/api/geocode/json"

api: str = "AIzaSyAN8Hx_hWJd-kkInC5GoIcDGtHz44IYDew"

address: str = "Piaseczno"

params: Dict[str, str] = {
    "address": address,
    "key": api
}

# response = requests.get(url, params = params)
# data: Dict[str, Any] = response.json()
json_string: str = "{'results': [{'address_components': [{'long_name': 'Piaseczno', 'short_name': 'Piaseczno', 'types': ['locality', 'political']}, {'long_name': 'Piaseczno County', 'short_name': 'Piaseczno County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Masovian Voivodeship', 'short_name': 'Masovian Voivodeship', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Poland', 'short_name': 'PL', 'types': ['country', 'political']}, {'long_name': '05-500', 'short_name': '05-500', 'types': ['postal_code']}], 'formatted_address': '05-500 Piaseczno, Poland', 'geometry': {'bounds': {'northeast': {'lat': 52.0994024, 'lng': 21.0613285}, 'southwest': {'lat': 52.0475472, 'lng': 20.9729303}}, 'location': {'lat': 52.0811536, 'lng': 21.0238602}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 52.0994024, 'lng': 21.0613285}, 'southwest': {'lat': 52.0475472, 'lng': 20.9729303}}}, 'place_id': 'ChIJAQLEDzkuGUcR9Rt6fpxax4g', 'types': ['locality', 'political']}], 'status': 'OK'}"

json_string = json_string.replace("\'", "\"")

print(json_string)

data: Dict[str, Any] = json.loads(json_string)

print(type(data))
if data["status"] == "OK" and len(data["results"]) > 0:
    location = data["results"][0]["geometry"]["location"]
    print("Lat: " + str(location["lat"]) + "\nLng: " + str(location["lng"]))
else:
    print("No results.")




###### do rysowania linii???
# import json
# import geopandas as gpd
# from shapely.geometry import LineString, Point

# with open("overpass_result.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# nodes = {}
# ways = []

# # zbierz wszystkie węzły
# for elem in data["elements"]:
#     if elem["type"] == "node":
#         nodes[elem["id"]] = (elem["lon"], elem["lat"])

# # utwórz LineString dla każdego way
# for elem in data["elements"]:
#     if elem["type"] == "way":
#         coords = [nodes[nid] for nid in elem["nodes"] if nid in nodes]
#         if coords:
#             ways.append({"geometry": LineString(coords), "tags": elem.get("tags", {})})

# # geopandas do wyświetlenia
# gdf = gpd.GeoDataFrame(ways)
# gdf.plot()
