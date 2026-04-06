# Geo_project

<p align="center">
    <img src="img/Peaks.jpg" width="600">
</p>

# 📍 Geo Project
A web application for planning mountain trips in South Korea using OpenStreetMap data.

## 📸 Screenshots
<details>
<summary>More photos</summary>
<br>
<p align="center">
    <img src="img/EventLink.jpg" width="600"><br>
    <img src="img/Calendar.jpg" width="600"><br>
</p>
</details>

## 💡 Solutions
The app allows you to:
* browse the map of South Korea
* fetch points (peaks, viewpoints) from OpenStreetMap
* display trails within a 2 km radius
* visualizing trail difficulty with color-coding
* check the 5-day weather forecast
* save events to Google Calendar (with a link to the map)

## 🏗 Architecture
The project is based on a multi-tier architecture:
```
Frontend (JavaScript)
    ↓
Backend (FastAPI)
    ↓
Backend (Services / Models)
    ↓
Cache (Redis) → Database (PostgreSQL) → External APIs
```

### Data retrieval strategy:
1. Cache (Redis)
2. Database (PostgreSQL)
3. External API (OpenStreetMap/OpenWeatherMap)

## 🐳 Docker
The entire application runs in containers:
* frontend
* backend
* PostgreSQL
* Redis (cache)
* OpenStreetMap API (local)

## Features:
* Peak and viewpoint markers (OpenStreetMap)
* Hiking trails around the selected point
* Trail coloring by difficulty
* 5-day weather forecast
* Select trip date
* Google Calendar integration (#geo + map link)

## ⚙️ Backend Details
### Technologies:
* Python + FastAPI
* PostgreSQL
* Redis (cache)
* Docker / docker-compose
* OpenStreetMap API
* Google Calendar API
* OpenWeatherMap API
* JavaScript (frontend)

### Patterns and best practices:
* Dependency Injection
* API Retry & Timeout
* Service Health Checks
* Decorators (e.g., for handling retry/logic)
* Layering:
    * services
    * models
    * API integrations

### Tests:
* pytest
* coverage

### Running tests:

```bash
pytest
```

### Database:
* PostgreSQL
* Alembic
* dump data structure (without data) in repo
* cron job to delete old/obsolete data
* data about:
    * routes
    * waypoints
    * weather
    * events

## Design Decisions:
* Using local maps allows us to bypass the limits imposed by external APIs
* OpenWeatherMap instead of Google Weather API - no major API limitations
* Database (PostgreSQL) - reduced API queries
* Cache (Redis) - keeping a local copy to speed up responses and reduce the number of API queries
* Docker - easy to run the entire environment
* Layered architecture - readability and scalability
* Alembic - control of the database architecture between developers and easy testing of changes

## Google Calendar
The link in the Google Calendar event takes the user to a read-only view that shows the details of the planned trip:

* selected trails and waypoint
* weather forecast for the day of the event
* no option to change the date or add new waypoints to maintain consistency between the planned date and route

## Possible improvements:
* User authorization
* CI/CD (deploy)
* Better route filtering

## Getting started (Installation):
1. Download the map of South Korea from: `http://download.geofabrik.de/asia/south-korea.html`.<br>
2. Convert the map from `.osm.pbf` to `.osm.bz2` format using `Osmium`. Put the converted map into the `docker_db_frontend/overpass_db/`.<br>
3. Into the folder `geo_project/geo_project/tokens/` insert file `credentials.json`, which we get from website: `https://console.cloud.google.com/`.<br>
4. In the `docker_db_frontend` folder:

```bash
docker compose up
```
Note: The map container may take about 20 minutes to start during first run.<br>

5. Run the `docker_db_frontend/DB/init/init_db.sh` file by using `bash init_db.sh`.<br>
6. The first time you try to save an event to the calendar, you will need to log in to your Google account in a browser to get a `token.json` file.
