# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Field Worker Temperature Monitoring System - A Flask-based web application for monitoring field workers' body temperature using ESP32 sensors and ThingSpeak integration. The system provides real-time temperature monitoring with automatic dashboard updates and fever alerts.

## Common Development Commands

### Initial Setup
```bash
# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python3 create_db.py
python3 seed_admin.py
```

### Running the Application
```bash
# Main application (port 5002)
python3 app.py

# Alternative using Flask CLI (port 5000)
flask --app app.py --debug run --port 5000

# Quick setup script (Linux/macOS)
bash run.sh
```

### Development & Testing
```bash
# Run system tests with simulated sensor data
python3 test_system.py

# Single test run (check if app is responding)
curl http://localhost:5002/api/today/latest

# Test data ingestion (ThingSpeak format)
curl -X POST http://localhost:5002/api/ingest \
  -H "Content-Type: application/json" \
  -H "X-INGEST-KEY: super-secret-device-key" \
  -d '{"field1": "36.5", "field2": "37.8"}'
```

### Database Operations
```bash
# Reset database (if corrupted)
rm -f instance/app.db
python3 create_db.py
python3 seed_admin.py

# View database records (requires sqlite3)
sqlite3 instance/app.db "SELECT * FROM daily_checkins;"
sqlite3 instance/app.db "SELECT * FROM readings ORDER BY recorded_at DESC LIMIT 10;"
```

## Architecture Overview

### Application Structure
- **Flask App Factory Pattern**: `app.py` creates app instance and registers blueprints
- **Blueprint Architecture**: Separated into `views` (web UI) and `ingest` (API) blueprints
- **Configuration Management**: Centralized in `config.py` with environment variable support
- **Database Layer**: SQLAlchemy with three main models (Admin, DailyCheckin, Reading)

### Data Flow Architecture
1. **Hardware Layer**: ESP32 + temperature sensors on worker equipment
2. **Data Ingestion**: ESP32 → ThingSpeak → Flask `/api/ingest` endpoint
3. **Storage**: Temperature readings stored in SQLite database
4. **Real-time Updates**: JavaScript polls `/api/today/latest` every 11 seconds
5. **Admin Interface**: Web dashboard with live temperature monitoring

### Key Components

#### Models (`models.py`)
- `Admin`: Authentication for dashboard access
- `DailyCheckin`: Worker registration with element ID assignment
- `Reading`: Temperature data from sensors with UTC timestamps

#### API Endpoints
- `POST /api/ingest`: Accepts temperature data in ThingSpeak field format (`field1`, `field2`, etc.) or direct JSON format
- `GET /api/today/latest`: Returns latest temperature readings for today's registered workers

#### Frontend Architecture
- **Templates**: Jinja2 templates with TailwindCSS styling
- **Real-time Updates**: `dashboard.js` handles automatic data refresh and visual feedback
- **Temperature Visualization**: Color-coded badges and visual thermometers based on temperature ranges

### Temperature Alert System
- **Normal**: < 37.5°C (green)
- **Monitor**: 37.5-37.9°C (amber/warning)
- **Fever Alert**: ≥ 38.0°C (red with pulse animation)

## Configuration

### Environment Variables (.env)
- `SECRET_KEY`: Flask session security
- `ADMIN_USERNAME`/`ADMIN_PASSWORD`: Dashboard credentials (default: admin/admin123)
- `INGEST_API_KEY`: Optional API security for sensor data (default: "super-secret-device-key")
- `DB_URL`: Database connection (default: SQLite in instance/ folder)

### ThingSpeak Integration
- **Read API Key**: `YKWSHBBTJZP4EZ46`
- **Write API Key**: `RAPODLW686AVLMSN`
- **Server**: `api.thingspeak.com`
- **Field Mapping**: Field number = element_id, field value = temperature

## Development Patterns

### Database Timezone Handling
- All database timestamps stored in UTC
- Local timezone conversions handled in views using pytz (Africa/Lagos)
- Daily check-ins use local date strings (YYYY-MM-DD format)

### Error Handling
- API endpoints return appropriate HTTP status codes
- Frontend displays connection errors with auto-hide timeout
- Database operations wrapped in try-catch with rollback support

### Real-time Updates
- Dashboard polls API every 11 seconds (matches typical ThingSpeak cadence)
- Visual feedback for data updates (scale animations)
- Connection error handling with retry logic

## Security Considerations

- Password hashing using Werkzeug security functions
- Session-based authentication for admin access
- Optional API key validation for data ingestion
- Input validation and sanitization on all endpoints
- No sensitive data in client-side JavaScript

## Testing & Debugging

### System Test Script
`test_system.py` provides comprehensive testing:
- ThingSpeak format data ingestion simulation
- Dashboard API endpoint verification  
- Continuous monitoring simulation (30 seconds)
- Fever alert detection testing

### Common Issues
- **Database lock errors**: Delete `instance/app.db` and reinitialize
- **ThingSpeak connection**: Verify webhook configuration and API keys
- **Dashboard not updating**: Check browser console for JavaScript errors
- **Port conflicts**: App defaults to port 5002, adjust if needed
- **Mobile menu not visible**: All pages now extend base.html with working mobile navigation

### Template Architecture
- **Base Template**: All pages extend `base.html` which includes responsive navigation
- **Immersive Pages**: Login and checkin pages hide main content area for full-screen experience
- **Mobile Navigation**: Hamburger menu button styled for visibility with proper JavaScript functionality

### Debug Mode
Run with `debug=True` for detailed error messages and auto-reload on file changes.

