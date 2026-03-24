import datetime
import json
from psycopg2.extras import Json
from typing import Dict, Any, Tuple, Optional
from geo_project.models.map_models import POI
from geo_project.models.map_models import OSMPointsResponse
from datetime import date


class PlacesRepository:

    def check_trails_for_point_in_db (self, conn: Any, id: int, ttl_days = 30) -> bool:
        cutoff: datetime = datetime.datetime.now() - datetime.timedelta(days=ttl_days)
        with conn.cursor() as cur:
            cur.execute("SELECT last_checked FROM map_points WHERE map_id=%s", (id,))
            row: Optional[Tuple] = cur.fetchone()

        if row is None or row[0] is None or row[0] < cutoff:
            return True #No trails need to get them from API
        return False #There are trails for that point
        
    def update_last_check_for_point (self, conn: Any, id: int, now_fn= datetime.datetime.now):
        now: datetime = now_fn()
        with conn.cursor() as cur:
            cur.execute("UPDATE map_points SET last_checked=%s WHERE map_id=%s", (now, id))

    def save_many(self, conn: Any, pois: list[POI]):
        """
        Wstawia wiele POI do tabeli places
        """
        with conn.cursor() as cur:
            for poi in pois:
                if poi.latitude is None or poi.longitude is None:
                    continue #just continue if point don't have lat nor long

                cur.execute(
                    """
                    INSERT INTO places (google_place_id, name, geom, place_type, place_url)
                    VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
                    ON CONFLICT (google_place_id) DO NOTHING
                    """,
                    (
                        poi.place_id,
                        poi.name,
                        poi.longitude,   # caution: ST_MakePoint(longitude, latitude)
                        poi.latitude,
                        poi.place_type,
                        poi.place_url
                    )
                )
    
    def save_many_points(self, conn: Any, points: OSMPointsResponse):
        """
        Wstawia wiele POI do tabeli trips
        """
        with conn.cursor() as cur:
            for point in points.get("features", []):
                coordinates: list[float] = point.get("geometry", {}).get("coordinates")
                if coordinates[0] is None or coordinates[1] is None:
                    continue  #just continue if point don't have coordinations

                cur.execute(
                    """
                    INSERT INTO map_points (name, map_id, geom, place_type, height)
                    VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
                    ON CONFLICT (map_id) DO NOTHING;
                    """,
                    (
                        point.get("properties", {}).get("Name"),
                        point.get("properties", {}).get("Id"),
                        coordinates[0],   # caution: ST_MakePoint(longitude, latitude)
                        coordinates[1],
                        point.get("properties", {}).get("Type"),
                        point.get("properties", {}).get("Height")
                    )
                )

    def save_trails(self, conn: Any, trails_summary: Dict[str, Any]):

        with conn.cursor() as cur:
            for feature in trails_summary["features"]:
                trail_id = feature["id"]
                geometry_json = json.dumps(feature["geometry"])   # only geometry!
                props_json = json.dumps(feature["properties"])    # properties as JSON

                cur.execute("""
                    INSERT INTO trip_points (id, geom, properties)
                    VALUES (%s,
                            ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326),
                            %s)
                    ON CONFLICT (id) DO NOTHING
                """, (trail_id, geometry_json, props_json))

    def read_trails (self, conn: Any, radius: int, lat: float, lon: float) -> Dict[str, Any]:
        
        with conn.cursor() as cur:
            cur.execute("""
                SELECT jsonb_build_object(
                    'type', 'FeatureCollection',
                    'features', jsonb_agg(
                        jsonb_build_object(
                            'type', 'Feature',
                            'id', id,
                            'geometry', ST_AsGeoJSON(geom)::jsonb,
                            'properties', properties
                        )
                    )
                )
                FROM trip_points
                WHERE ST_DWithin(
                    geom::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                    %s
                );
            """, (lon, lat, radius))

            geojson = cur.fetchone()[0]

        return geojson


class WeatherRepository:
        
    def check_weather_cache (self, conn: Any, lon: float, lat: float, radius = 7000) -> Any:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT raw_json
                FROM weather_forecast
                WHERE ST_DWithin(
                    geom::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                    %s
                )
                AND expires_at > now()
                ORDER BY geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                LIMIT 1;
            """, (lon, lat, radius, lon, lat))

            row: Optional[Tuple] = cur.fetchone()

        if row:
            return row[0]   # There is weather forecast
        else:
            return None     # Need to download forecast from API

    def save_weather (self, conn: Any, lon: float, lat: float, response_utc: datetime, json_data: Dict[str, Any], ttl_hours = 3):

        expires: datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=ttl_hours)

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO weather_forecast (
                    geom,
                    forecast_time,
                    expires_at,
                    raw_json
                ) VALUES (
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    %s,
                    %s,
                    %s
                )
            """, (lon, lat, response_utc, expires, Json(json_data)))

class CalendarEventRepository:

    def read_calendar_event_by_id (self, conn: Any, uuid: str) -> Dict[str, Any]:

        with conn.cursor() as cur:
            cur.execute("SELECT point_id, trail_id, weather_id, trip_date FROM trips_ WHERE id=%s", (uuid,))
            row: Optional[Tuple] = cur.fetchone()

            cur.execute("""
                SELECT jsonb_build_object(
                    'type', 'FeatureCollection',
                    'features', features,
                    'trip_info', jsonb_build_object(
                        'trip_date', t.trip_date,
                        'point_id', t.point_id,
                        'point_coor', ST_AsGeoJSON(tt.geom)::jsonb,
                        'point_name', tt.name,
                        'point_type', tt.place_type,
                        'point_heigh', tt.height,
                        'weather', w.raw_json
                    )
                ) AS full_geojson
                FROM trips_ t
                JOIN map_points tt ON tt.map_id = t.point_id
                JOIN weather_forecast w ON t.weather_id = w.id
                CROSS JOIN LATERAL (
                    SELECT jsonb_agg(
                        jsonb_build_object(
                            'type', 'Feature',
                            'geometry', ST_AsGeoJSON(tp.geom)::jsonb,
                            'properties', tp.properties
                        )
                    ) AS features
                    FROM unnest(t.trail_id) AS trail_id
                    JOIN trip_points tp ON tp.id = trail_id
                ) AS sub
                WHERE t.point_id = %s
                AND t.trip_date = %s;
            """, (row[0], row[3])
            )

            row: Optional[Tuple] = cur.fetchone()[0]
        return row

    def save_calendar_event_by_id (self, conn: Any, lat: float, lon: float, point_id: int, trip_date: date, radius = 2000, radius_weather = 7000):

        check_ids: bool = True

        with conn.cursor() as cur:
            cur.execute("SELECT map_id FROM map_points WHERE map_id=%s", (point_id,))
            row_map_id: Optional[Tuple] = cur.fetchone()
            if row_map_id is None or row_map_id[0] is None:
                check_ids = False

            cur.execute(
                """
                SELECT id
                FROM trip_points
                WHERE ST_DWithin(
                    geom::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    %s
                )
            """, (lon, lat, radius)
            )

            rows: Any = cur.fetchall()
            row_trails_id: list[str] = [r[0] for r in rows]
            if row_trails_id is None or row_trails_id[0] is None:
                check_ids = False

            cur.execute("""
                SELECT id
                FROM weather_forecast
                WHERE ST_DWithin(
                    geom::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                    %s
                )
                ORDER BY geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                LIMIT 1;
            """, (lon, lat, radius_weather, lon, lat))

            row_weather_id: Optional[Tuple] = cur.fetchone()
            if row_weather_id is None or row_weather_id[0] is None:
                check_ids = False

            if check_ids:
                cur.execute("""
                    INSERT INTO trips_ (point_id, trail_id, weather_id, trip_date)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (point_id, trip_date) DO NOTHING
                    RETURNING id;
                """, (row_map_id[0], row_trails_id, row_weather_id[0], trip_date)
                )

                return cur.fetchone()[0]