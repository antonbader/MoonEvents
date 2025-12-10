# MoonEvents - Mondereignis-Rechner

MoonEvents ist eine Python-Anwendung zur Berechnung und Visualisierung von lunaren Ereignissen, wie z.B. dem "Goldenen Henkel" oder speziellen Lichteffekten auf der Mondoberfläche. Die Anwendung ermöglicht es Astronomen und Hobbybeobachtern, den optimalen Beobachtungszeitpunkt für verschiedene Standorte zu planen.

## Funktionen

*   **Standortverwaltung:** Speichern und Verwalten verschiedener Beobachtungsorte mit Koordinaten und Zeitzonen.
*   **Ereignisdatenbank:** Auswahl aus einer vordefinierten Liste von Mondereignissen ("Lunar 100" etc.).
*   **Präzise Berechnung:** Ermittlung der Sichtbarkeit basierend auf Mond- und Sonnenstand (Sichtbarkeit nur wenn Sonne < 0° und Mond > 5°).
*   **Optimierung:** Wenn das theoretische Maximum nicht sichtbar ist, sucht das Programm nach dem bestmöglichen Zeitpunkt innerhalb des Ereignisfensters.
*   **Visualisierung:** Interaktive Mondkarte, die die Position der ausgewählten Ereignisse anzeigt.
*   **PDF-Export:** Exportieren der Berechnungslisten als PDF für den Feldeinsatz.

## Projektstruktur

*   `main.py`: Einstiegspunkt der Anwendung.
*   `mond_gui.py`: Hauptfenster und UI-Logik (Tkinter).
*   `mond_berechnung.py`: Astronomische Berechnungen (Ephem).
*   `mond_daten.py`: Datenbank der Mondereignisse (Koordinaten, Ziel-Colongitude).
*   `mond_map.py`: Kartenvisualisierung.
*   `mond_pdf.py`: PDF-Generierung.
*   `mond_storage.py`: Speichern/Laden von Benutzerdaten (Orte, Selektionen).

## Installation

Die Anwendung benötigt **Python 3.x**.

1.  **Repository klonen:**
    ```bash
    git clone <repository-url>
    cd moonevents
    ```

2.  **Virtuelle Umgebung erstellen (empfohlen):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # oder
    venv\Scripts\activate     # Windows
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

    Die wichtigsten Bibliotheken sind:
    *   `ephem`: Für astronomische Berechnungen.
    *   `tkcalendar`: Für die Datumsauswahl in der GUI.
    *   `fpdf`: Für den PDF-Export.
    *   `Pillow` & `requests`: Für Bildverarbeitung.

## Starten der Anwendung

Führen Sie das Hauptskript aus:

```bash
python3 main.py
```
