from geo_project.frontend_logic.frontend_logic import app

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