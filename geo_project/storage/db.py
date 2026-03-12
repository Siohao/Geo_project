from psycopg2 import pool
import os
from typing import Any

# Minimalny i maksymalny rozmiar puli połączeń
db_pool = pool.SimpleConnectionPool(
    1, 10, 
    # host=os.getenv("POSTGRES_HOST", "postgres-db"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT",5432),
    database="geo_project_db",
    user="admin",
    password="admin"
)

def get_conn() -> Any:
    return db_pool.getconn()

def release_conn(conn) -> None:
    db_pool.putconn(conn)