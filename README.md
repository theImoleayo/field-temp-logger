# Field Worker Temperature Monitoring System

A Flask-based web application for monitoring field workers' body temperature using ESP32 sensors and ThingSpeak integration.

## Features

- **Worker Registration**: Public page for daily check-in with element ID assignment
- **Admin Dashboard**: Real-time temperature monitoring with automatic updates every 11 seconds
- **ThingSpeak Integration**: Receives temperature data from ESP32 sensors via API
- **Database Storage**: SQLite database for worker records and temperature readings
- **Responsive UI**: Clean, modern interface using TailwindCSS

## System Architecture

1. **Hardware**: ESP32 + temperature sensor attached to worker helmets/equipment
2. **Data Flow**: ESP32 → ThingSpeak → Flask API → Database → Admin Dashboard
3. **Real-time Updates**: JavaScript automatically fetches latest temperature readings

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

3. **Initialize Database**:
   ```bash
   python3 create_db.py
   python3 seed_admin.py
   ```

4. **Run Application**:
   ```bash
   python3 app.py
   ```
   
   The app will be available at: http://localhost:5001

## Default Login

- **Username**: admin
- **Password**: admin123

## API Endpoints

### Data Ingestion (for ThingSpeak/ESP32)
```http
POST /api/ingest
Content-Type: application/json
X-INGEST-KEY: super-secret-device-key

{
  "element_id": "helmet_001", 
  "temperature_c": 36.5
}
```

**ThingSpeak Format** (field number = element_id, field value = temperature):
```http
POST /api/ingest
X-INGEST-KEY: super-secret-device-key
{
  "field1": "30.5",    // Element ID 1 with temperature 30.5°C
  "field2": "38.0",    // Element ID 2 with temperature 38.0°C
  "field3": "36.2"     // Element ID 3 with temperature 36.2°C
}
```

**ESP32 Configuration:**
- Read API Key: `YKWSHBBTJZP4EZ46`
- Write API Key: `RAPODLW686AVLMSN`
- Server: `api.thingspeak.com`

### Dashboard Data (Internal)
```http
GET /api/today/latest
```
Returns latest temperature readings for all registered workers for the current day.

## Usage

### For Workers (Public Access)
1. Visit `/checkin` 
2. Enter your full name, worker ID, and element ID for the day
3. Submit to register your presence

### For Administrators
1. Visit `/login`
2. Login with admin credentials
3. View real-time temperature monitoring on the dashboard
4. Temperature readings automatically update every 11 seconds
5. High temperature readings (≥38°C) are highlighted in red

## Configuration

Key settings in `.env`:
- `SECRET_KEY`: Flask session security key
- `ADMIN_USERNAME`: Admin login username
- `ADMIN_PASSWORD`: Admin login password  
- `INGEST_API_KEY`: Optional API key for data ingestion security
- `TIMEZONE`: Timezone for date/time display (default: Africa/Lagos)

## Database Schema

### daily_checkins
- `id`: Primary key
- `date_str`: Date in YYYY-MM-DD format
- `worker_id`: Unique worker identifier
- `full_name`: Worker's full name
- `element_id`: Hardware element ID assigned to worker
- `created_at`: Timestamp of check-in

### readings
- `id`: Primary key
- `element_id`: Hardware element ID
- `temperature_c`: Temperature in Celsius
- `recorded_at`: UTC timestamp of reading

### admin
- `id`: Primary key
- `username`: Admin username
- `password_hash`: Hashed password

## Hardware Setup

The system expects ESP32 devices to:
1. Read temperature from attached sensors
2. Send data to ThingSpeak with element_id and temperature
3. Configure ThingSpeak to forward data to your Flask app's `/api/ingest` endpoint

## Security

- Admin authentication using secure password hashing
- Optional API key protection for data ingestion
- Session-based authentication for admin dashboard
- Input validation and sanitization

## Development

To contribute or modify:
1. Create a virtual environment: `python3 -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Make changes and test
5. Ensure database migrations work properly

## Troubleshooting

- If database errors occur, delete `instance/app.db` and run `python3 create_db.py` again
- Check the `.env` file configuration if login fails
- Verify ThingSpeak webhook is configured correctly for API data ingestion
- Check browser console for JavaScript errors if dashboard updates fail

## License

This project is for internal use and monitoring field worker safety.
