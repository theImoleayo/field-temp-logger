#!/usr/bin/env python3
"""
Test script to verify ThingSpeak data fetching
"""

import requests
import json
from datetime import datetime
from config import Config

def test_thingspeak_connection():
    """Test basic connection to ThingSpeak API"""
    channel_id = "3022640"
    read_api_key = Config.THINGSPEAK_READ_API_KEY
    
    print(f"Testing ThingSpeak API connection...")
    print(f"Channel ID: {channel_id}")
    print(f"Read API Key: {read_api_key}")
    print("-" * 50)
    
    # Test fetching channel info
    url = f"https://api.thingspeak.com/channels/{channel_id}.json"
    params = {'api_key': read_api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        channel_info = response.json()
        
        print("✓ Channel info retrieved successfully")
        print(f"Channel Name: {channel_info.get('name', 'Unknown')}")
        print(f"Description: {channel_info.get('description', 'No description')}")
        print(f"Created: {channel_info.get('created_at', 'Unknown')}")
        
        # Show field information
        if 'field1' in channel_info:
            print(f"Field 1: {channel_info.get('field1', 'Unnamed')}")
        if 'field2' in channel_info:
            print(f"Field 2: {channel_info.get('field2', 'Unnamed')}")
            
    except requests.RequestException as e:
        print(f"✗ Error fetching channel info: {e}")
        return False
    
    print("-" * 50)
    
    # Test fetching latest data
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds/last.json"
    params = {'api_key': read_api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        latest_data = response.json()
        
        if latest_data:
            print("✓ Latest data retrieved successfully")
            print(f"Entry ID: {latest_data.get('entry_id')}")
            print(f"Created at: {latest_data.get('created_at')}")
            
            # Show all field values
            for i in range(1, 9):
                field_key = f'field{i}'
                if field_key in latest_data and latest_data[field_key] is not None:
                    print(f"{field_key}: {latest_data[field_key]}")
                    
        else:
            print("✗ No data found in channel")
            
    except requests.RequestException as e:
        print(f"✗ Error fetching latest data: {e}")
        return False
    
    print("-" * 50)
    
    # Test fetching multiple recent entries
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        'api_key': read_api_key,
        'results': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        feeds = data.get('feeds', [])
        print(f"✓ Retrieved {len(feeds)} recent entries")
        
        for i, feed in enumerate(feeds):
            print(f"Entry {i+1}: ID={feed.get('entry_id')}, Time={feed.get('created_at')}")
            # Show first field with data
            for field_num in range(1, 9):
                field_key = f'field{field_num}'
                if field_key in feed and feed[field_key] is not None:
                    print(f"  {field_key}: {feed[field_key]}")
                    break
                    
    except requests.RequestException as e:
        print(f"✗ Error fetching recent data: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("ThingSpeak API Test")
    print("=" * 50)
    
    success = test_thingspeak_connection()
    
    if success:
        print("\n✓ All tests passed! ThingSpeak API is working correctly.")
        print("\nYou can now run the sync service with:")
        print("  python3 thingspeak_sync.py --once    # Run once")
        print("  python3 thingspeak_sync.py           # Run continuously")
    else:
        print("\n✗ Some tests failed. Please check your configuration.")
