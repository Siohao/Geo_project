from geo_project.geo_config.config import Config
from geo_project.services.map_services import MapServices
from geo_project.api.api import GoogleMapsClient

Config.load_language("pl")
client = GoogleMapsClient()
services = MapServices(client)

main_actions = {
    "add_event":    lambda: new_event_menu(),
    "choose_lang":  lambda: change_lang_menu(),
    "edit_event":   lambda: edit_event_menu()
}

def main_menu():
    print("==========MENU==========")
    for key, value in Config.lang.get("main_menu", {}).items():
        print(f"{key} - {Config.lang.get(value)}")

    choice: str = input(f"{Config.lang.get("choose_option")}")
    menu: str = Config.lang.get("main_menu", {})
    action: str = menu.get(choice)

    func = main_actions.get(action)
    

    if func:
        func()
    else:
        print("Źle")
        main_menu()

new_event_actions = {
    "hike_event": lambda: services.get_route_summary("a","b","c"),
    # "hike_event": lambda: hike_event(),
    # "bike_event": lambda: bike_event(),
    # "poi_event":  lambda: poi_event(),
    "exit": lambda: None
}

def new_event_menu():
    print(f"=========={Config.lang.get("new_event_")}==========")
    for key, value in Config.lang.get("new_events_menu", {}).items():
        print(f"{key} - {Config.lang.get(value)}")

    choice: str = input(f"{Config.lang.get("choose_option")}")
    n_event: str = Config.lang.get("new_events_menu", {})
    action: str = n_event.get(choice)

    func = new_event_actions.get(action)

    if func:
        func()
        main_menu()
    else:
        print("Źle")
        new_event_menu()

change_lang_actions = {
    "eng_lang": lambda: Config.load_language("en"),
    "pl_lang":  lambda: Config.load_language("pl"),
    "exit":     lambda: None
}

def change_lang_menu():
    print(f"=========={Config.lang.get("lang_")}==========")
    for key, value in Config.lang.get("change_lang_menu", {}).items():
        print(f"{key} - {Config.lang.get(value)}")

    choice: str = input(f"{Config.lang.get("choose_option")}")
    lang: str = Config.lang.get("change_lang_menu", {})
    action: str = lang.get(choice)

    func = change_lang_actions.get(action)

    if func:
        func()
        main_menu()
    else:
        print("Źle")

edit_event_actions = {
    # "edit_hike_event":  lambda: edit_hike_event(),
    # "edit_bike_event":  lambda: edit_bike_event(),
    # "edit_poi_event":   lambda: edit_poi_event(),
    "exit":             lambda: None
}

def edit_event_menu():
    print(f"=========={Config.lang.get("edit_event_")}==========")
    for key, value in Config.lang.get("edit_event_menu", {}).items():
        print(f"{key} - {Config.lang.get(value)}")
    
    choice: str = input(f"{Config.lang.get("choose_option")}")
    e_event: str = Config.lang.get("edit_event_menu", {})
    action: str = e_event.lang(choice)

    func = edit_event_actions(action)

    if func:
        func()
        main_menu()
    else:
        print("Źle")