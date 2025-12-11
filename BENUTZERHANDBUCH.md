# MoonEvents - Benutzerhandbuch

Willkommen bei **MoonEvents**, Ihrem Werkzeug zur Planung von Mondbeobachtungen. Dieses Programm hilft Ihnen, den perfekten Zeitpunkt zu finden, um spezielle Lichteffekte auf dem Mond (wie Krateraufgänge oder Schattenwürfe) zu beobachten.

## Erste Schritte

Nach dem Starten der Anwendung sehen Sie das Hauptfenster mit verschiedenen Reitern (Tabs). Sie können zwischen diesen Reitern wechseln, um Ihre Beobachtung zu konfigurieren.

### 1. Orte (Standortwahl)

Damit die Berechnungen korrekt sind, muss das Programm wissen, von wo aus Sie beobachten.

*   **Liste:** Links sehen Sie Ihre gespeicherten Orte.
*   **Neuen Ort anlegen:**
    1.  Geben Sie rechts Namen, Koordinaten (Breite/Länge in Dezimalgrad), Höhe (in Metern) und den UTC-Offset (Zeitzone, z.B. 1 für MEZ, 2 für MESZ) ein.
    2.  Klicken Sie auf **"Neu"**.
*   **Aktiv setzen:** Wählen Sie einen Ort in der Liste aus und klicken Sie auf **"Aktiv setzen"**. Der aktive Ort wird unten fett angezeigt und für alle Berechnungen verwendet.
*   **Bearbeiten:** Wählen Sie einen Ort aus, ändern Sie die Werte rechts und speichern Sie ihn als neuen Ort (oder löschen Sie den alten).

### 2. Ereigniswahl

Hier bestimmen Sie, *was* Sie beobachten möchten.

*   **Liste:** Eine Liste aller verfügbaren Mondereignisse (z.B. Krater, Gebirge, spezielle Lichtstrahlen). Hinter dem Namen wird das ungefähre Mondalter in Tagen angezeigt (z.B. "Tag 10.5"), was einen Hinweis auf die benötigte Mondphase gibt.
*   **Auswahl:** Setzen Sie Häkchen bei den Ereignissen, die Sie interessieren.
*   **Buttons:** Nutzen Sie "Alle auswählen" oder "Alle abwählen" für eine schnelle Selektion.

### 3. Berechnung

Das Herzstück der Anwendung. Hier planen Sie den Zeitraum.

*   **Zeitraum:** Wählen Sie das **Start-** und **Enddatum** für Ihre Planung.
*   **Nur gut sichtbare anzeigen:** Wenn aktiviert, werden Ereignisse, die zur fraglichen Zeit nicht sichtbar sind (z.B. weil der Mond unter dem Horizont steht oder es Tag ist), ausgeblendet.
*   **Berechnen:** Startet den Suchlauf. Das Programm prüft für jedes gewählte Ereignis, wann im gewählten Zeitraum die Beleuchtung optimal ist.
*   **Ergebnistabelle:**
    *   **Ereignis:** Name des Objekts.
    *   **Start / Ende:** Beginn und Ende des Zeitfensters, in dem der Lichteffekt sichtbar ist.
    *   **Optimum:** Der *beste sichtbare* Zeitpunkt für Ihren Standort (siehe unten "Erklärung der Berechnung").
    *   **Theor. Optimum:** Der *geometrisch* perfekte Zeitpunkt (unabhängig von Sichtbarkeit).
    *   **Status:** "Gut beobachtbar" (Grün) oder ein Grund für schlechte Sichtbarkeit (Rot, z.B. "Mond unter Horizont").
*   **Detail-Ansicht:** Ein **Doppelklick** auf eine Zeile öffnet ein Fenster mit weiteren Details:
    *   Genaue Zeiten für Start, Optimum, theor. Optimum und Ende.
    *   Positionsdaten (Breite/Länge) und Colongitude.
    *   Aktuelle Mondphase und Mondalter.
    *   Vollständige Beschreibungstexte.
*   **PDF Export:** Speichert die aktuelle Liste als PDF-Datei. In der PDF werden Zeiten, zu denen das Ereignis tatsächlich sichtbar ist (Mond über Horizont, Sonne unter Horizont), **grün** hervorgehoben.

### 4. Karte

Dieser Reiter visualisiert die Lage der *ausgewählten* Ereignisse auf einer schematischen Mondkarte.

*   **Darstellung:** Die ausgewählten Ereignisse werden als Punkte auf der Karte markiert.
*   **Filter "Nur beobachtbare anzeigen":** Über dem Kartenbild befindet sich eine Checkbox. Diese wird aktiviert, sobald eine Berechnung durchgeführt wurde. Wenn Sie den Haken setzen, werden auf der Karte nur jene Ereignisse angezeigt, die im berechneten Zeitraum tatsächlich sichtbar sind. Dies hilft bei der schnellen Orientierung für die kommende Beobachtungsnacht.

### 5. Info

Hier finden Sie Versionsnummer und Kontaktinformationen.

---

## Hintergrund zur Berechnung

Um die Ergebnisse besser zu verstehen, hier eine Erklärung der Begriffe:

### Theor. Optimum (Theoretisches Optimum)
Dies ist der Zeitpunkt, an dem die Sonne in exakt dem Winkel zum Mondkrater steht, der den gewünschten Lichteffekt erzeugt (basierend auf der "Colongitude"). Dieser Zeitpunkt ist rein geometrisch und berücksichtigt **nicht**, ob es Nacht ist oder der Mond an Ihrem Standort überhaupt am Himmel steht.

### Optimum (Beobachtungs-Optimum)
Das Programm versucht, einen *real beobachtbaren* Zeitpunkt zu finden.
1.  Wenn das **Theor. Optimum** gut sichtbar ist (Nacht, Mond über Horizont), sind "Optimum" und "Theor. Optimum" identisch.
2.  Ist das **Theor. Optimum** *nicht* sichtbar (z.B. weil der Mond gerade untergegangen ist), sucht das Programm im Zeitraum um das Ereignis herum (Standard: +/- 1 Stunde), ob der Mond vorher oder nachher aufgeht/sichtbar wird.
3.  Findet es einen sichtbaren Moment, wird dieser als **Optimum** angezeigt (Status: "Verschoben").
4.  Ist im gesamten Zeitfenster keine Beobachtung möglich, bleibt das Datum unverändert, aber der Status zeigt "Nicht sichtbar" an.

### Sichtbarkeitskriterien
Ein Ereignis gilt als **sichtbar**, wenn:
*   Die **Sonne** unter dem Horizont steht (Höhe < 0°).
*   Der **Mond** mehr als 5° über dem Horizont steht.
