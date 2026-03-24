# Geo_project

# 📍 Geo Project
Aplikacja webowa do planowania wycieczek górskich w Korei Południowej z wykorzystaniem danych z OpenStreetMap.

# ❓ Problem
Mapy takie jak Naver Map nie pokazują dobrze szlaków górskich ani nie ułatwiają planowania wycieczek. Oraz nie są tak intuicyjne i nie wyszczególniają szczytów górskich i punktów widokowych.

# 💡 Rozwiązanie
Aplikacja umożliwia:
* przeglądanie mapy Korei Południowej
* pobieranie punktów (szczyty, punkty widokowe) z OpenStreetMap
* wyświetlanie szlaków w promieniu 2 km
* oznaczanie trudności szlaków kolorami
* sprawdzanie prognozy pogody na 5 dni
* planowanie wycieczki w kalendarzu
* zapisywanie wydarzeń w Google Calendar (z linkiem do mapy)

# 🏗 Architektura
Projekt oparty na architekturze wielowarstwowej:
```
Frontend (JavaScript)
    ↓
Backend (FastAPI)
    ↓
Services / Models / External APIs
    ↓
Cache (Redis) → Database (PostgreSQL) → External APIs
```

# Strategia pobierania danych:
1. Cache (Redis)
2. Baza danych (PostgreSQL)
3. Zewnętrzne API (OpenStreetMap/OpenWeatherMap)

# 🐳 Docker
Cała aplikacja działa w kontenerach:
* frontend
* backend
* PostgreSQL
* Redis (cache)
* OpenStreetMap API (lokalnie)

# Uruchomienie:
```bash
docker-compoes up --build
```

# Funkcjonalności:
* Markery szczytów i punktów widokowych (OpenStreetMap)
* Szlaki górskie wokół wybranego punktu
* Kolorowanie szlaków według trudności
* Prognoza pogody (5 dni)
* Wybór daty wycieczki
* Integracja z Google Calendar (#geo + link do mapy)

# Technologie:
* Python + FastAPI
* PostgreSQL
* Redis (cache)
* Docker / docker-compose
* OpenStreetMap API
* Google Calendar API
* OpenWeatherMap API
* JavaScript (frontend)

# Wzorce i dobre praktyki:
* Dependency Injection
* Retry & timeout dla API
* Healthchecki usług
* Dekoratory (np. do obsługi retry/logiki)
* Podział na warstwy:
    * services
    * models
    * integracje z API

# Testy:
* pytest
* coverage
# Uruchomienie:
```bash
pytest
```

# CI skonfigurowane w GitHub Actions:
* uruchomienie testów
* sprawdzenie jakości kodu

# Baza danych:
* PostgreSQL
* dump struktury danych (bez danych) w repo
* cron do usuwania starych/nieaktualnych danych
* dane o:
    * trasach
    * punktach
    * pogodzie
    * wydarzeniach

# Decyzje projektowe:
* OpenStreetMap zamiast Google Maps - brak ograniczeń API
* OpenWeatherMap zamiast Google Weather API - brak większych ograniczeń API
* Baza danych (PostgreSQL) - zmniejszenie zapytać do API
* Cache (Redis) - zmniejszenie zapytań do bazy danych/API
* Docker - łatwe uruchomienie całego środowiska
* Warstwowa architektura - czytelność i skalowalność

# Google Calendar
Link w wydarzeniu Google Calendar przenosi użytkownika do widoku read-only, który pokazuje szczegóły zaplanowanej wycieczki:

* wybrane szlaki i punkt
* prognozę pogody na dzień wydarzenia
* bez możliwości zmiany daty czy dodawania nowych punktów, aby zachować spójność zaplanowanego terminu i trasy

# Możliwe ulepszenia:
* autoryzacja użytkowników
* CI/CD (deploy)
* lepsze filtrowanie tras