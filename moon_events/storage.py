# mond_storage.py
import json
import os
from .data import get_default_location, EREIGNISSE_DB
from .utils import get_storage_path

FILENAME = "mond_einstellungen.json"

def load_data():
    default_data = {
        "locations": [get_default_location()],
        "selected_location_index": 0,
        "selected_events_indices": list(range(len(EREIGNISSE_DB))) 
    }
    
    file_path = get_storage_path(FILENAME)
    if not os.path.exists(file_path):
        return default_data
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "locations" not in data: data["locations"] = default_data["locations"]
            return data
    except:
        return default_data

def save_data(data):
    file_path = get_storage_path(FILENAME)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")
