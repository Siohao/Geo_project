from geo_project.storage.storage import PlacesRepository
from typing import Dict, Any
import datetime

def test_no_row_returns_true(db_conn):
    repo = PlacesRepository()
    result = repo.check_trails_for_point_in_db(db_conn, id=1)
    assert result is True

def test_old_row_returns_true(db_conn):
    old_date: datetime = datetime.datetime.now() - datetime.timedelta(days=31)
    with db_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO trips_test (map_id, last_checked)
            VALUES (%s, %s)
        """, (1, old_date)
        )

    repo = PlacesRepository()
    result = repo.check_trails_for_point_in_db(db_conn, id=1)
    assert result is True

def test_old_row_returns_false(db_conn):
    recent_date: datetime = datetime.datetime.now() - datetime.timedelta(days=5)
    with db_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO trips_test (map_id, last_checked)
            VALUES (%s, %s)
        """, (2, recent_date)
        )

    repo = PlacesRepository()
    result = repo.check_trails_for_point_in_db(db_conn, id=2)
    assert result is False

def test_update_last_check_for_point(db_conn):
    def fake_now():
        return datetime.datetime(2020, 2, 20, 20, 0, 0)

    repo = PlacesRepository()
    repo.update_last_check_for_point(db_conn, 1, fake_now)

    with db_conn.cursor() as cur:
        cur.execute("SELECT last_checked FROM trips_test WHERE map_id=%s", (1,))
        result = cur.fetchone()

    assert result[0] == fake_now()

def test_save_many_points(db_conn):

    data: Dict[str, Any] = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point",
                             "coordinates": ["10.0", "20.1"]},
                "properties": {"Name": "Test Name",
                                "Id": 3,
                                "Height": 200.0,
                                "Type": "natural"
                                }
            }
        ]
    }

    mock_repo = PlacesRepository()
    mock_repo.save_many_points(db_conn, points=data)

    with db_conn.cursor() as cur:
        cur.execute("SELECT name FROM trips_test WHERE map_id=%s", (3,))
        result = cur.fetchone()

    assert result[0] == "Test Name"