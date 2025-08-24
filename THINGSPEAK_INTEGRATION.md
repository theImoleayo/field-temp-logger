# ThingSpeak Integration

This directory contains a complete ThingSpeak integration system that automatically syncs temperature data from ThingSpeak to your local Flask application database.

## Overview

Your ESP32 device is currently sending temperature data to ThingSpeak channel 3022640. This integration:

1. **Fetches** new temperature data from ThingSpeak API every 30 seconds
2. **Processes** the data and stores it in your local database 
3. **Avoids duplicates** by tracking processed entries
4. **Provides** the data through your existing Flask API endpoints

## Files

- `thingspeak_sync.py` - Main sync service script
- `test_thingspeak.py` - Test script to verify ThingSpeak connectivity
- `thingspeak-sync.service` - Systemd service file for production
- `manage_sync_service.sh` - Management script for systemd service
- `run_sync_background.sh` - Alternative script using screen sessions

## Quick Start

### 1. Test ThingSpeak Connection
```bash
python3 test_thingspeak.py
```

### 2. Run One-Time Sync
```bash
python3 thingspeak_sync.py --once
```

### 3. Run Continuous Sync (Development)
```bash
# Option A: Using screen session (recommended for development)
./run_sync_background.sh start

# Check status
./run_sync_background.sh status

# View logs
./run_sync_background.sh logs

# Stop service
./run_sync_background.sh stop
```

### 4. Install as System Service (Production)
```bash
# Install the systemd service
./manage_sync_service.sh install

# Start the service
./manage_sync_service.sh start

# Check status
./manage_sync_service.sh status

# View logs
./manage_sync_service.sh logs
```

## Configuration

The sync service uses your existing configuration from `config.py`:

- **Channel ID**: 3022640 (hardcoded in sync script)
- **Read API Key**: `THINGSPEAK_READ_API_KEY` from environment or config
- **Database**: Same SQLite database used by your Flask app

### Environment Variables

Make sure these are set in your `.env` file:
```bash
THINGSPEAK_READ_API_KEY=YKWSHBBTJZP4EZ46
THINGSPEAK_WRITE_API_KEY=RAPODLW686AVLMSN  # Currently not used
```

## How It Works

### Data Flow
```
ESP32 → ThingSpeak Channel 3022640 → Sync Service → Local Database → Flask API
```

### Field Mapping
- ThingSpeak `field1` → Database `element_id=1`
- ThingSpeak `field2` → Database `element_id=2`
- ...and so on for up to 8 fields

### Sync Process
1. Fetches latest entry from ThingSpeak
2. Checks if entry ID was already processed
3. Extracts temperature data from all fields
4. Creates Reading records in local database
5. Tracks last processed entry ID to avoid duplicates

## Verification

After running the sync, verify data is available:

### 1. Check Database Directly
```bash
python3 -c "
from app import create_app
from models import Reading
app = create_app()
with app.app_context():
    readings = Reading.query.order_by(Reading.recorded_at.desc()).limit(5).all()
    for r in readings:
        print(f'Element {r.element_id}: {r.temperature_c}°C at {r.recorded_at}')
"
```

### 2. Test Flask API
```bash
# Start your Flask app first
python3 run.py

# Then in another terminal:
curl http://localhost:5000/api/today/latest
```

## Troubleshooting

### Service Won't Start
- Check if Python dependencies are installed
- Verify config.py has correct ThingSpeak API key
- Check permissions on service files

### No Data Syncing
```bash
# Test ThingSpeak connection
python3 test_thingspeak.py

# Run single sync with debug output
python3 thingspeak_sync.py --once

# Check recent ThingSpeak data manually
curl "https://api.thingspeak.com/channels/3022640/feeds/last.json?api_key=YKWSHBBTJZP4EZ46"
```

### View Service Logs
```bash
# For systemd service
./manage_sync_service.sh logs

# For screen session
./run_sync_background.sh logs
```

## Production Recommendations

1. **Use systemd service** for production deployment
2. **Monitor logs** regularly for any API errors
3. **Set up log rotation** to prevent log files from growing too large
4. **Consider webhook approach** for real-time updates (see Alternative Approaches)

## Alternative Approaches

### 1. ThingSpeak Webhook (Recommended for Real-time)
Configure a ThingSpeak webhook to POST directly to your Flask API endpoint:
- URL: `http://your-server.com/api/ingest`
- Method: POST
- Body: Include field1 as temperature data

### 2. ESP32 Dual Posting
Modify ESP32 firmware to send data to both:
- ThingSpeak (for cloud backup/visualization)
- Your Flask API directly (for real-time local processing)

### 3. Increase Sync Frequency
Edit `thingspeak_sync.py` to change sync interval from 30 seconds to desired frequency.

## Current Status

✓ ESP32 sending data to ThingSpeak
✓ ThingSpeak API accessible and working
✓ Sync service fetching and storing data
✓ Flask API serving synced data
✓ Service management scripts ready

The integration is complete and ready for use!
