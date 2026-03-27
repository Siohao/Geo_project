from alembic import op

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
    CREATE TABLE map_points (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        name TEXT NOT NULL,
        geom geometry(Point,4326) NOT NULL,
        place_type TEXT,
        height DOUBLE PRECISION,
        created_at TIMESTAMPTZ DEFAULT now(),
        map_id NUMERIC UNIQUE,
        last_checked TIMESTAMP
    );
    """)
    op.execute("""
    CREATE TABLE trip_points (
        id TEXT PRIMARY KEY,
        geom geometry(Geometry,4326) NOT NULL,
        properties JSONB
    );
    """)
    op.execute("""
    CREATE TABLE weather_forecast (
        id BIGINT PRIMARY KEY,
        geom geography(Point,4326) NOT NULL,
        forecast_time TIMESTAMP NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        raw_json JSONB,
        created_at TIMESTAMP DEFAULT now()
    );
    """)
    op.execute("""
    CREATE TABLE trips_ (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        point_id NUMERIC REFERENCES map_points(map_id),
        trail_id TEXT[],
        weather_id BIGINT REFERENCES weather_forecast(id) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT now(),
        trip_date DATE NOT NULL,
        UNIQUE(point_id, trip_date)
    );
    """)

def downgrade():
    op.execute("DROP TABLE IF EXISTS trips_ CASCADE;")
    op.execute("DROP TABLE IF EXISTS trip_points CASCADE;")
    op.execute("DROP TABLE IF EXISTS map_points CASCADE;")
    op.execute("DROP TABLE IF EXISTS weather_forecast CASCADE;")