from geo_project.geo_config.logger import get_logger
from geo_project.storage.db import get_conn, release_conn
from typing import Any
from logging import Logger
from fastapi import HTTPException
from geo_project.main import app

logger: Logger = get_logger(__name__)

def check_db():
    conn: Any = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
    finally:
        if conn:
            release_conn(conn)

@app.get("/health")
def health():
    try:
        check_db()
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Healthcheck failed"
        )
