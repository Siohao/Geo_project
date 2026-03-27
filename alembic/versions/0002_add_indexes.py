"""Add indexes and constraints

Revision ID: 0002_add_indexes
Revises: 0001_initial
Create Date: 2026-03-26 12:00:00
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0002_add_indexes'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Map Points indexes (BTREE)
    op.execute("CREATE INDEX IF NOT EXISTS idx_map_points_last_checked ON map_points USING btree (last_checked);")

    # Trip Points indexes (GIST for geo)
    op.execute("CREATE INDEX IF NOT EXISTS trip_points_geog_idx ON trip_points USING gist ((geom::geography));")

    # Trips indexes (BTREE)
    op.execute("CREATE INDEX IF NOT EXISTS idx_trips_created_at ON trips_ USING btree (created_at);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_trips_trip_date ON trips_ USING btree (trip_date);")

    # Weather Forecast indexes
    op.execute("CREATE INDEX IF NOT EXISTS idx_weather_expires ON weather_forecast USING btree (expires_at);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_weather_geom ON weather_forecast USING gist (geom);")


def downgrade():
    # drop indexes if rolling back
    op.execute("DROP INDEX IF EXISTS idx_map_points_last_checked;")
    op.execute("DROP INDEX IF EXISTS trip_points_geog_idx;")
    op.execute("DROP INDEX IF EXISTS idx_trips_created_at;")
    op.execute("DROP INDEX IF EXISTS idx_trips_trip_date;")
    op.execute("DROP INDEX IF EXISTS idx_weather_expires;")
    op.execute("DROP INDEX IF EXISTS idx_weather_geom;")