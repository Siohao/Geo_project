from geo_project.storage.storage import PlacesRepository
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

