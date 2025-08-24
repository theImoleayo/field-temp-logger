#!/usr/bin/env python3
"""
Test script to demonstrate the Field Worker Temperature Monitoring System
"""

import requests
import json
import time
import random

# Configuration
BASE_URL = "http://localhost:5002"
API_KEY = "super-secret-device-key"

def test_thingspeak_ingestion():
    """Test ThingSpeak format data ingestion"""
    print("🔄 Testing ThingSpeak data ingestion...")
    
    # Simulate temperature readings from different elements
    test_data = [
        {"field1": "36.2"},  # Element 1
        {"field2": "37.8"},  # Element 2  
        {"field3": "38.5"},  # Element 3 (fever alert)
        {"field4": "35.9"},  # Element 4
    ]
    
    for i, data in enumerate(test_data):
        response = requests.post(
            f"{BASE_URL}/api/ingest",
            headers={
                "Content-Type": "application/json",
                "X-INGEST-KEY": API_KEY
            },
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            element_id = list(data.keys())[0].replace('field', '')
            temp = data[list(data.keys())[0]]
            print(f"✅ Element {element_id}: {temp}°C - Recorded as ID {result['id']}")
        else:
            print(f"❌ Failed to ingest data: {response.text}")
        
        time.sleep(1)  # Simulate real-time interval

def test_dashboard_api():
    """Test dashboard API endpoint"""
    print("\n📊 Testing dashboard API...")
    
    response = requests.get(f"{BASE_URL}/api/today/latest")
    if response.status_code == 200:
        data = response.json()
        print("✅ Dashboard API response:")
        print(json.dumps(data, indent=2))
        
        # Check for fever alerts
        for worker_id, reading in data.items():
            temp = reading.get('temperature_c', 0)
            if temp >= 38:
                print(f"🚨 FEVER ALERT: Worker {worker_id} - {temp}°C")
    else:
        print(f"❌ Dashboard API failed: {response.text}")

def simulate_continuous_monitoring():
    """Simulate continuous temperature monitoring"""
    print("\n🔄 Simulating continuous monitoring for 30 seconds...")
    
    elements = [1, 2, 3, 4]
    start_time = time.time()
    
    while time.time() - start_time < 30:
        # Pick a random element and simulate temperature reading
        element = random.choice(elements)
        # Generate realistic temperature (35-39°C range)
        temperature = round(random.uniform(35.0, 39.0), 1)
        
        data = {f"field{element}": str(temperature)}
        
        response = requests.post(
            f"{BASE_URL}/api/ingest",
            headers={
                "Content-Type": "application/json",
                "X-INGEST-KEY": API_KEY
            },
            json=data
        )
        
        if response.status_code == 200:
            status = "🚨" if temperature >= 38 else "✅"
            print(f"{status} Element {element}: {temperature}°C")
        else:
            print(f"❌ Failed: {response.text}")
        
        time.sleep(10)  # Every 10 seconds like real ThingSpeak

if __name__ == "__main__":
    print("🏭 Field Worker Temperature Monitoring - System Test")
    print("=" * 50)
    
    try:
        # Test basic ingestion
        test_thingspeak_ingestion()
        
        # Test dashboard API
        test_dashboard_api()
        
        # Ask user if they want continuous monitoring
        choice = input("\n🤔 Run continuous monitoring simulation? (y/n): ")
        if choice.lower() == 'y':
            simulate_continuous_monitoring()
            
        print("\n✅ System test completed!")
        print(f"🌐 Access the dashboard at: {BASE_URL}/login")
        print("👤 Login: admin / admin123")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Flask application is not running!")
        print("Run 'python3 app.py' first!")
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
