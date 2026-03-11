from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from geo_project.frontend_logic.osm import router as osm_router
from geo_project.frontend_logic.weather import router as owm_router
from geo_project.frontend_logic.calendar import router as calendar_router

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


tags_points = {
    # "tourism": "viewpoint",
    "natural": "peak"
}

#way
tags_routes = {
    "highway": "path",
    "sac_scale": None,
    # "route": "hiking"
}

#node
tags_hiking_routes = {
    "highway": ["path", "steps", "track"]
}



    # with open("test_calendar_event.json", "w", encoding="utf-8") as f:
    # #     ######## .model_dump() -> zmiana z obiektu klasy na dict
    #     json.dump(data, f, ensure_ascii=False, indent=2)
    # #     # json.dump(data.model_dump(), f, ensure_ascii=False, indent=2)
    #     print("Zapisano")
    # print("koniec")