from psycopg2 import pool
from typing import Any

# Minimalny i maksymalny rozmiar puli połączeń
db_pool = pool.SimpleConnectionPool(
    1, 10, 
    host="127.0.0.1",
    port=5433,
    database="geo_project_db",
    user="admin",
    password="admin"
)

def get_conn() -> Any:
    return db_pool.getconn()

def release_conn(conn) -> None:
    db_pool.putconn(conn)