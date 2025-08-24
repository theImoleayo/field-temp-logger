#!/usr/bin/env python3
"""
ThingSpeak Data Synchronization Service
Fetches temperature data from ThingSpeak and syncs it with local database
"""

import requests
import time
import json
from datetime import datetime, timedelta
from config import Config
from app import create_app
from database import db
from models import Reading

class ThingSpeakSync:
    def __init__(self):
        self.app = create_app()
        self.channel_id = "3022640"  # From your ThingSpeak URL
        self.read_api_key = Config.THINGSPEAK_READ_API_KEY
        self.base_url = f"https://api.thingspeak.com/channels/{self.channel_id}"
        self.last_entry_id = self.get_last_processed_entry_id()
        
    def get_last_processed_entry_id(self):
        """Get the last processed entry ID to avoid duplicates"""
        with self.app.app_context():
            # Look for a way to track last processed entry
            # For now, start from the most recent database reading
            return 0
    
    def fetch_latest_readings(self, results=100):
        """Fetch latest readings from ThingSpeak"""
        url = f"{self.base_url}/feeds.json"
        params = {
            'api_key': self.read_api_key,
            'results': results
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'feeds' not in data:
                print(f"No feeds data in response: {data}")
                return []
                
            return data['feeds']
            
        except requests.RequestException as e:
            print(f"Error fetching from ThingSpeak: {e}")
            return []
    
    def fetch_single_latest(self):
        """Fetch just the latest single reading from ThingSpeak"""
        url = f"{self.base_url}/feeds/last.json"
        params = {
            'api_key': self.read_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [data] if data else []
            
        except requests.RequestException as e:
            print(f"Error fetching latest from ThingSpeak: {e}")
            return []
    
    def process_reading(self, feed_data):
        """Process a single ThingSpeak feed entry"""
        entry_id = feed_data.get('entry_id')
        created_at = feed_data.get('created_at')
        
        if not entry_id or not created_at:
            return False
            
        # Skip if we've already processed this entry
        if entry_id <= self.last_entry_id:
            return False
            
        # Process each field (field1, field2, etc.)
        readings_added = 0
        for field_num in range(1, 9):
            field_key = f'field{field_num}'
            if field_key in feed_data and feed_data[field_key] is not None:
                try:
                    temperature = float(feed_data[field_key])
                    element_id = str(field_num)
                    
                    # Parse ThingSpeak timestamp
                    ts = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    
                    # Check if this reading already exists
                    existing = Reading.query.filter_by(
                        element_id=element_id,
                        recorded_at=ts
                    ).first()
                    
                    if not existing:
                        reading = Reading(
                            element_id=element_id,
                            temperature_c=temperature,
                            recorded_at=ts
                        )
                        db.session.add(reading)
                        readings_added += 1
                        print(f"Added reading: Element {element_id} = {temperature}°C at {ts}")
                        
                except (ValueError, TypeError) as e:
                    print(f"Error processing {field_key}: {e}")
                    continue
        
        if readings_added > 0:
            db.session.commit()
            self.last_entry_id = max(self.last_entry_id, entry_id)
            
        return readings_added > 0
    
    def sync_once(self):
        """Perform a single sync operation"""
        print(f"Syncing ThingSpeak data at {datetime.now()}")
        
        with self.app.app_context():
            # Fetch latest readings
            feeds = self.fetch_single_latest()
            
            if not feeds:
                print("No new data from ThingSpeak")
                return
            
            processed = 0
            for feed in feeds:
                if self.process_reading(feed):
                    processed += 1
            
            print(f"Processed {processed} new readings")
    
    def run_continuous(self, interval_seconds=30):
        """Run continuous sync with specified interval"""
        print(f"Starting ThingSpeak sync service (interval: {interval_seconds}s)")
        print(f"Channel ID: {self.channel_id}")
        print(f"API Key: {self.read_api_key}")
        
        while True:
            try:
                self.sync_once()
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\nSync service stopped by user")
                break
            except Exception as e:
                print(f"Error in sync loop: {e}")
                time.sleep(interval_seconds)

def main():
    """Main function for running the sync service"""
    import sys
    
    sync = ThingSpeakSync()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once and exit
        sync.sync_once()
    else:
        # Run continuously
        sync.run_continuous(interval_seconds=30)

if __name__ == '__main__':
    main()
