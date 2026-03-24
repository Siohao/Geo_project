import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_conn():
    conn = psycopg2.connect(
        dbname= "test_db",
        user= "test_user",
        password= "test123",
        host= "localhost",
        port= 5432
    )
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS test_schema")
        cur.execute("SET search_path TO test_schema, public")
        cur.execute("DROP TABLE IF EXISTS map_points")
        cur.execute("""
                CREATE TABLE map_points (
                    id NUMERIC,
                    name TEXT,
                    map_id NUMERIC UNIQUE,
                    geom Geometry (Point, 4326),
                    place_type TEXT,
                    height DOUBLE PRECISION,
                    last_checked TIMESTAMP
                )
        """)
    
    yield conn

    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS map_points")
    conn.close()