--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Debian 16.9-1.pgdg110+1)
-- Dumped by pg_dump version 16.9 (Debian 16.9-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pg_cron; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_cron WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION pg_cron; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_cron IS 'Job scheduler for PostgreSQL';


--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO admin;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO admin;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO admin;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


--
-- Name: cleanup_old_rows(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.cleanup_old_rows() RETURNS void
    LANGUAGE sql
    AS $$
DELETE FROM trips_ WHERE trip_date < NOW() - INTERVAL '4 days';
DELETE FROM trips_test WHERE created_at < NOW() - INTERVAL '14 days';
DELETE FROM weather_cache WHERE expires_at < NOW() - INTERVAL '4 days';
$$;


ALTER FUNCTION public.cleanup_old_rows() OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: map_points; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.map_points (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    geom public.geometry(Point,4326) NOT NULL,
    place_type text,
    height double precision,
    created_at timestamp with time zone DEFAULT now(),
    map_id numeric,
    last_checked timestamp without time zone
);


ALTER TABLE public.map_points OWNER TO admin;

--
-- Name: trip_points; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trip_points (
    id text NOT NULL,
    geom public.geometry(Geometry,4326) NOT NULL,
    properties jsonb
);


ALTER TABLE public.trip_points OWNER TO admin;

--
-- Name: trips_; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trips_ (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    point_id numeric,
    trail_id text[],
    weather_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    trip_date date NOT NULL
);


ALTER TABLE public.trips_ OWNER TO admin;

--
-- Name: trips__weather_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trips__weather_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trips__weather_id_seq OWNER TO admin;

--
-- Name: trips__weather_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trips__weather_id_seq OWNED BY public.trips_.weather_id;


--
-- Name: weather_forecast; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.weather_forecast (
    id bigint NOT NULL,
    geom public.geography(Point,4326) NOT NULL,
    forecast_time timestamp without time zone NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    raw_json jsonb,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.weather_forecast OWNER TO admin;

--
-- Name: weather_cache_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.weather_cache_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weather_cache_id_seq OWNER TO admin;

--
-- Name: weather_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.weather_cache_id_seq OWNED BY public.weather_forecast.id;


--
-- Name: trips_ weather_id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trips_ ALTER COLUMN weather_id SET DEFAULT nextval('public.trips__weather_id_seq'::regclass);


--
-- Name: weather_forecast id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.weather_forecast ALTER COLUMN id SET DEFAULT nextval('public.weather_cache_id_seq'::regclass);


--
-- Name: trip_points trip_points_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trip_points
    ADD CONSTRAINT trip_points_pkey PRIMARY KEY (id);


--
-- Name: trips_ trips__pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trips_
    ADD CONSTRAINT trips__pkey PRIMARY KEY (id);


--
-- Name: trips_ trips__point_date_unique; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trips_
    ADD CONSTRAINT trips__point_date_unique UNIQUE (point_id, trip_date);


--
-- Name: map_points trips_test_map_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.map_points
    ADD CONSTRAINT trips_test_map_id_key UNIQUE (map_id);


--
-- Name: map_points trips_test_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.map_points
    ADD CONSTRAINT trips_test_pkey PRIMARY KEY (id);


--
-- Name: weather_forecast weather_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.weather_forecast
    ADD CONSTRAINT weather_cache_pkey PRIMARY KEY (id);


--
-- Name: idx_trips__created_at; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_trips__created_at ON public.trips_ USING btree (created_at);


--
-- Name: idx_trips__trip_date; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_trips__trip_date ON public.trips_ USING btree (trip_date);


--
-- Name: idx_trips_test_created_at; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_trips_test_created_at ON public.map_points USING btree (last_checked);


--
-- Name: idx_weather_expires; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_weather_expires ON public.weather_forecast USING btree (expires_at);


--
-- Name: idx_weather_geom; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_weather_geom ON public.weather_forecast USING gist (geom);


--
-- Name: trip_points_geog_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trip_points_geog_idx ON public.trip_points USING gist (((geom)::public.geography));


--
-- Name: trips_ trips__point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trips_
    ADD CONSTRAINT trips__point_id_fkey FOREIGN KEY (point_id) REFERENCES public.map_points(map_id);


--
-- Name: trips_ trips__weather_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trips_
    ADD CONSTRAINT trips__weather_id_fkey FOREIGN KEY (weather_id) REFERENCES public.weather_forecast(id);


--
-- PostgreSQL database dump complete
--

