from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from geo_project.frontend_logic.osm import router as osm_router
from geo_project.frontend_logic.weather import router as owm_router
from geo_project.frontend_logic.calendar import router as calendar_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Lub konkretny adres frontendu
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(osm_router)
app.include_router(owm_router)
app.include_router(calendar_router)