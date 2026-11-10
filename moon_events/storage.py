# mond_storage.py
import json
import os
from .data import get_default_location, EREIGNISSE_DB
from .utils import get_storage_path

FILENAME = "mond_einstellungen.json"


def load_data():
    all_names = [ev["name"] for ev in EREIGNISSE_DB]
    default_data = {
        "locations": [get_default_location()],
        "selected_location_index": 0,
        "selected_events_names": all_names,
        "selected_events_indices": list(range(len(EREIGNISSE_DB))),
    }

    file_path = get_storage_path(FILENAME)
    if not os.path.exists(file_path):
        return default_data

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "locations" not in data or not data["locations"]:
                data["locations"] = default_data["locations"]

            # Encoding-Korrektur für ältere Dateien ("GÃ¼nzburg" -> "Günzburg")
            for loc in data["locations"]:
                if isinstance(loc.get("name"), str) and "Ã" in loc["name"]:
                    try:
                        loc["name"] = loc["name"].encode("latin-1").decode("utf-8")
                    except Exception:
                        pass

            # Abwärtskompatible Auflösung: Namen bevorzugt, sonst aus Indizes ableiten
            if "selected_events_names" in data and isinstance(data["selected_events_names"], list):
                name_set = set(data["selected_events_names"])
                data["selected_events_indices"] = [
                    i for i, ev in enumerate(EREIGNISSE_DB) if ev["name"] in name_set
                ]
            elif "selected_events_indices" in data and isinstance(data["selected_events_indices"], list):
                valid_indices = [
                    i for i in data["selected_events_indices"]
                    if isinstance(i, int) and 0 <= i < len(EREIGNISSE_DB)
                ]
                data["selected_events_indices"] = valid_indices
                data["selected_events_names"] = [EREIGNISSE_DB[i]["name"] for i in valid_indices]
            else:
                data["selected_events_names"] = all_names
                data["selected_events_indices"] = list(range(len(EREIGNISSE_DB)))

            return data
    except Exception:
        return default_data


def save_data(data):
    file_path = get_storage_path(FILENAME)
    try:
        if "selected_events_indices" in data:
            data["selected_events_names"] = [
                EREIGNISSE_DB[i]["name"]
                for i in data["selected_events_indices"]
                if isinstance(i, int) and 0 <= i < len(EREIGNISSE_DB)
            ]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")
