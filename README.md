# MoonEvents - Mondereignis-Rechner

MoonEvents ist eine Python-Anwendung zur Berechnung und Visualisierung von lunaren Ereignissen, wie z.B. dem "Goldenen Henkel" oder speziellen Lichteffekten auf der Mondoberfläche. Die Anwendung ermöglicht es Astronomen und Hobbybeobachtern, den optimalen Beobachtungszeitpunkt für verschiedene Standorte zu planen.

## Funktionen

*   **Standortverwaltung:** Speichern und Verwalten verschiedener Beobachtungsorte mit Koordinaten und Zeitzonen.
*   **Ereignisdatenbank:** Auswahl aus einer vordefinierten Liste von Mondereignissen ("Lunar 100" etc.).
*   **Präzise Berechnung:** Ermittlung der Sichtbarkeit basierend auf Mond- und Sonnenstand (Sichtbarkeit nur wenn Sonne < 0° und Mond > 5°).
*   **Optimierung:** Wenn das theoretische Maximum nicht sichtbar ist, sucht das Programm nach dem bestmöglichen Zeitpunkt innerhalb des Ereignisfensters.
*   **Detail-Ansicht:** Detaillierte Informationen zu jedem berechneten Ereignis (Position, Mondphase, genaue Zeiten) per Doppelklick.
*   **Visualisierung:** Interaktive Mondkarte, die die Position der ausgewählten Ereignisse anzeigt (inkl. Filter für sichtbare Ereignisse).
*   **PDF-Export:** Exportieren der Berechnungslisten als PDF für den Feldeinsatz.

## Projektstruktur

*   `main.py`: Einstiegspunkt der Anwendung.
*   `moon_events/`: Paket mit dem Quellcode.
    *   `gui.py`: Hauptfenster und UI-Logik (Tkinter).
    *   `calculations.py`: Astronomische Berechnungen (Ephem).
    *   `data.py`: Datenbank der Mondereignisse (Koordinaten, Ziel-Colongitude).
    *   `map.py`: Kartenvisualisierung.
    *   `pdf.py`: PDF-Generierung.
    *   `storage.py`: Speichern/Laden von Benutzerdaten (Orte, Selektionen).
    *   `utils.py`: Pfadauflösung für Ressourcen und Benutzereinstellungen (Entwicklung und Exe-Bundle).

## Installation

Die Anwendung benötigt **Python 3.x**.

1.  **Repository klonen:**
    ```bash
    git clone <repository-url>
    cd moonevents
    ```

2.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

    Die wichtigsten Bibliotheken sind:
    *   `ephem`: Für astronomische Berechnungen.
    *   `tkcalendar`: Für die Datumsauswahl in der GUI.
    *   `fpdf`: Für den PDF-Export.
    *   `Pillow`: Für Bildverarbeitung.
    *   `requests`: Für Netzwerkoperationen.

## Starten der Anwendung

Führen Sie das Hauptskript aus:

```bash
python main.py
```

## Exe-Datei erstellen (Windows)

Es stehen zwei komfortable Wege bereit, um eine eigenständige `.exe`-Datei zu erstellen:

1. **Automatisch per Batch-Skript (Empfohlen):**
   * Doppelklick auf [`build_exe.bat`](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/build_exe.bat).
   * Das Skript baut die ausführbare Datei `dist\MoonEvents.exe` als eigenständige One-File-Anwendung (inklusive eingebetteter Karte `moon_map.jpg`, Konfiguration und Anwendungs-Icon).

2. **Über die grafische Oberfläche (auto-py-to-exe):**
   * Starten Sie [`start_auto_py_to_exe.bat`](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/start_auto_py_to_exe.bat) oder laden Sie die Konfiguration [`auto_py_to_exe_config.json`](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/auto_py_to_exe_config.json) im Interface über *Configuration -> Import Config*.
   * Alle Parameter (One-File, Fensteranwendung ohne Konsolenfenster, Ressourcen, Icon) sind fertig hinterlegt.
   * Klicken Sie auf den blauen Button **"Convert .py to .exe"**.
