# Field Temp Logger

ESP32-powered field worker temperature logger. **Flask** backend with **SQLite/MySQL**, **admin dashboard** that live-updates temperatures, and a **public check-in** page so workers bind themselves to a wearable element (helmet/band) for the day. Supports direct JSON or **ThingSpeak-style** payloads.

## Features
- Public **Daily Check-in** (no login): full name, worker_id, element_id
- **Admin login** + dashboard listing today’s check-ins
- **Live temperature updates** every ~11s without page refresh
- Ingest API:
  - JSON: `{ "element_id": "helmet-01", "temperature_c": 36.9 }`
  - ThingSpeak-style: `{ "field1": "helmet-01", "field2": 36.9 }`
- Optional ingest API key (`INGEST_API_KEY`)

## Tech
- Flask, Flask-SQLAlchemy
- SQLite (default) or MySQL
- HTML/CSS/JS frontend
- ESP32 firmware example (DHT22)

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# initialize DB and seed admin
python create_db.py
python seed_admin.py

# run
flask --app app.py --debug run --port 5000
