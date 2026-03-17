from psycopg2 import pool
import os
from typing import Any

_db_pool = None

def get_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = pool.SimpleConnectionPool(
            1, 10, 
            host=os.getenv("POSTGRES_HOST", "postgres-db"),
            port=os.getenv("POSTGRES_PORT",5432),
            database="geo_project_db",
            user="admin",
            password="admin"
        )
    return _db_pool

def get_conn() -> Any:
    return get_pool().getconn()

def release_conn(conn) -> None:
    get_pool().putconn(conn)