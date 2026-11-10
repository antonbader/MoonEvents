# MoonEvents - Mondereignis-Rechner & Beobachtungsplaner

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/info.conf)
[![Database](https://img.shields.io/badge/Daten--Version-3.0-green.svg)](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/moon_events/data.py)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg)](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

**MoonEvents** ist eine spezialisierte Desktop-Anwendung zur präzisen Vorausberechnung und visuellen Planung lunarer Licht- und Schattenspiele (*Clair-obscur-Phänomene* wie der „Goldene Henkel“, das „Lunar X“, Kraterbeleuchtungen und Lichtstrahlen).

Die Software ermittelt für beliebige Erdstandorte die exakten Zeitpunkte optimaler Ausleuchtung und bewertet die reale Sichtbarkeit anhand lokaler astronomischer Horizont- und Dämmerungsbedingungen sowie der Mondlibration.

---

## Highlights & Funktionen

* **Präzise 2D-Beleuchtungsberechnung:**
  Im Gegensatz zu einfachen Näherungen über eine statische 1D-Colongitude löst MoonEvents die sphärische Beleuchtungsgleichung auf der Mondoberfläche unter Berücksichtigung der sonnenselenografischen Breite ($b_0$). Dadurch treten selbst bei hochbreitigen und polnahen Strukturen (z. B. *Lunar X*, *Barrow-Strahl*) keine jahreszeitlichen Driftfehler von mehreren Stunden auf.
* **Optische Libration & Randperspektive:**
  Berechnung der optischen Mondlibration in Breite und Länge ($\pm 8^\circ$). Randnahe Objekte werden auf tatsächliche Sichtbarkeit auf der erdzugewandten Seite geprüft ($< 89^\circ$ Scheibenmittelpunktsabstand).
* **Reale Standortsichtbarkeit:**
  Ein Ereignis wird nur als sichtbar eingestuft, wenn die bürgerliche Dämmerung beendet ist (Sonnenhöhe $\le -6^\circ$) und der Mond ausreichend hoch über dem Horizont steht ($\ge 5^\circ$). Die atmosphärische Refraktion wird über die barometrische Höhenformel an die Geländehöhe des Beobachtungsorts angepasst.
* **Intelligente Beobachtungsoptimierung:**
  Ist das theoretische geometrische Maximum von Ihrem Standort aus unsichtbar (z. B. am Taghimmel oder unter dem Horizont), prüft das System das gesamte Sichtbarkeitsfenster des Ereignisses und ermittelt das beste beobachtbare Teilfenster.
* **Umfangreiche Ereignisdatenbank (v3.0):**
  Enthält 42 astronomisch verifizierte Mondereignisse für zunehmenden und abnehmenden Mond, gegliedert nach Schwierigkeitsgrad (*Leicht*, *Mittel*, *Schwer*) inklusive spezifischer Beobachtungstipps für Teleskop- und Instrumentenwahl.
* **Automatische Zeitzonen- & Sommerzeitunterstützung (MEZ/MESZ):**
  Automatische Umschaltung zwischen Winterzeit (Normalzeit) und Sommerzeit über das Python-Modul `zoneinfo`.
* **Interaktive Mondkarte mit Libration:**
  Orthografische 2D-Projektion der ausgewählten Ereignisse auf den Mondglobus. Bei vorliegender Berechnung passt sich die Projektion dynamisch an die reale Libration des Ereigniszeitpunkts an. Intelligente Textplatzierung verhindert Überlappungen von Beschriftungen.
* **Detaillierte Analyseansicht:**
  Doppelklick auf ein Berechnungsergebnis öffnet ein Detailfenster mit genauen lokalen Zeiten, subsolarer Breite $b_0$, lokaler Sonnenhöhe am Krater, Randdistanz, Librationswerten, wahrem synodischem Mondalter und Beobachtungshinweisen.
* **Druckfertiger PDF-Export (A4 Querformat):**
  Exportiert übersichtliche Beobachtungstabellen für den Feldeinsatz mit farbiger Kennzeichnung beobachtbarer Phasen, Mondhöhen, Schwierigkeitsgraden und bereinigtem Zeichensatz.
* **Windows One-Click Standalone-Build:**
  Vorkonfigurierte Skripte (`build_exe.bat` und `start_auto_py_to_exe.bat`) zur schnellen Kompilierung in eine eigenständige, portable Windows-Anwendung ohne Python-Installationspflicht beim Endanwender.

---

## Projektstruktur

```text
MoonEvents/
├── main.py                     # Startpunkt der Anwendung
├── info.conf                   # Versionsnummer und Release-Datum
├── requirements.txt            # Python-Abhängigkeiten
├── mond_einstellungen.json     # Gespeicherte Benutzerdaten (Orte, Auswahl)
├── moon_map.jpg                # Bildressource für die Mondkarte
├── icon.ico                    # Anwendungs-Icon (Multi-Resolution)
├── build_exe.bat               # Ein-Klick-Build mit PyInstaller
├── start_auto_py_to_exe.bat    # Startet GUI-Tool auto-py-to-exe
├── auto_py_to_exe_config.json  # Vorkonfigurierte Build-Einstellungen
├── README.md                   # Projektübersicht und Schnellstart
├── BENUTZERHANDBUCH.md         # Ausführliche Bedienungsanleitung
├── LICENSE                     # GNU General Public License v3.0
└── moon_events/                # Anwendungspaket
    ├── __init__.py
    ├── calculations.py         # Intervallsuche, Newton-Verfahren, Zeitumrechnung
    ├── calculation_logic.py    # EphemCalculator: Refraktion, 2D-Sonnengleichung, Libration
    ├── data.py                 # EREIGNISSE_DB (v3.0, 42 Ereignisse, Koordinaten, Tipps)
    ├── gui.py                  # Tkinter-Benutzeroberfläche (Tabs für Orte, Ereignisse, etc.)
    ├── map.py                  # MoonMap: Orthografische Projektion & Kollisionsvermeidung
    ├── pdf.py                  # PDFReport: A4-Querformat-Export mit fpdf
    ├── storage.py              # Laden und Speichern der Benutzereinstellungen
    └── utils.py                # Pfadauflösung für Entwicklung & kompilierte .exe
```

---

## Systemvoraussetzungen & Installation

### Voraussetzungen
* **Betriebssystem:** Windows 10 / 11, Linux oder macOS
* **Python:** Version **3.9** oder neuer

### 1. Repository klonen
```bash
git clone https://github.com/antonbader/MoonEvents.git
cd MoonEvents
```

### 2. Abhängigkeiten installieren
Es wird empfohlen, eine virtuelle Umgebung (`venv`) zu verwenden:

```bash
# Virtuelle Umgebung erstellen und aktivieren (Windows)
python -m venv venv
venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

Die Kernbibliotheken umfassen:
* `ephem`: Hochpräzise astronomische Ephemeridenberechnungen
* `Pillow`: Laden und Rendern der Mondkarte
* `tkcalendar`: Komfortable Datumsauswahl in der Benutzeroberfläche
* `fpdf`: Generierung druckfertiger PDF-Dokumente
* `pyinstaller` / `auto-py-to-exe`: Erstellung der eigenständigen Windows-Executable

---

## Starten der Anwendung

Starten Sie die Anwendung über das Hauptskript:

```bash
python main.py
```

---

## Windows-Executable (.exe) erstellen

Für Benutzer ohne Python-Installation kann MoonEvents als eigenständige Windows-Executable (`.exe`) paketiert werden:

### Methode 1: Automatischer Build (Empfohlen)
Führen Sie die Datei [`build_exe.bat`](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/build_exe.bat) per Doppelklick aus oder rufen Sie sie im Terminal auf:
```cmd
build_exe.bat
```
Das Skript erstellt unter `dist\MoonEvents.exe` eine portable Einzeldatei, die alle Bildressourcen, Konfigurationsdateien und das Anwendungs-Icon enthält. Benutzereinstellungen (`mond_einstellungen.json`) werden dauerhaft im Verzeichnis der Executable gespeichert.

### Methode 2: Über die grafische Oberfläche (auto-py-to-exe)
1. Starten Sie [`start_auto_py_to_exe.bat`](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/start_auto_py_to_exe.bat).
2. Die Konfiguration [`auto_py_to_exe_config.json`](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/auto_py_to_exe_config.json) ist bereits hinterlegt (oder kann über *Configuration -> Import Config* importiert werden).
3. Klicken Sie auf **"Convert .py to .exe"**.

---

## Dokumentation

Eine umfassende Beschreibung aller Funktionen, mathematischen Grundlagen und Bedienhinweise finden Sie im [Benutzerhandbuch (BENUTZERHANDBUCH.md)](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/BENUTZERHANDBUCH.md).

---

## Lizenz & Kontakt

* **Autor:** Anton Bader ([https://www.anton-bader.de](https://www.anton-bader.de))
* **E-Mail:** [info@anton-bader.de](mailto:info@anton-bader.de)
* **Lizenz:** Dieses Projekt steht unter der [GNU General Public License v3.0](file:///c:/Users/info/Documents/GitHub/Mond_Rechner/MoonEvents/LICENSE).
