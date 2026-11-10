# MoonEvents - Benutzerhandbuch

**Version:** 1.1.0  
**Datenbank-Version:** 3.1 (Stand: 10.11.2026)  
**Autor:** Anton Bader ([https://www.anton-bader.de](https://www.anton-bader.de))  
**Lizenz:** GNU General Public License v3.0  

---

## Inhaltsverzeichnis

1. [Einführung](#1-einführung)
2. [Erste Schritte & Programmoberfläche](#2-erste-schritte--programmoberfläche)
3. [Tab: Orte (Standortverwaltung)](#3-tab-orte-standortverwaltung)
4. [Tab: Ereignisse (Ereignisauswahl)](#4-tab-ereignisse-ereignisauswahl)
5. [Tab: Berechnung (Planung & Analyse)](#5-tab-berechnung-planung--analyse)
   - [Ergebnistabelle](#ergebnistabelle)
   - [Erweiterte Detail-Ansicht](#erweiterte-detail-ansicht)
   - [PDF-Export für den Feldeinsatz](#pdf-export-für-den-feldeinsatz)
6. [Tab: Karte (Visualisierung & Libration)](#6-tab-karte-visualisierung--libration)
7. [Tab: Info](#7-tab-info)
8. [Astronomische & Mathematische Grundlagen](#8-astronomische--mathematische-grundlagen)
   - [2D-sphärische Beleuchtungsberechnung](#2d-sphärische-beleuchtungsberechnung)
   - [Optische Libration und Randeffekt](#optische-libration-und-randeffekt)
   - [Reale Standortsichtbarkeit](#reale-standortsichtbarkeit)
   - [Intelligente Beobachtungsoptimierung](#intelligente-beobachtungsoptimierung)
   - [Wahres synodisches Mondalter](#wahres-synodisches-mondalter)
9. [Häufige Fragen & Troubleshooting (FAQ)](#9-häufige-fragen--troubleshooting-faq)

---

## 1. Einführung

Willkommen bei **MoonEvents**, Ihrem Werkzeug zur professionellen Vorausberechnung und Beobachtungsplanung lunarer Lichteffekte. 

Auf der Mondoberfläche entstehen durch den wandernden Terminator (die Tag-Nacht-Grenze) faszinierende Licht- und Schattenspiele, sogenannte **Clair-obscur-Phänomene**. Berühmte Beispiele sind der *Goldene Henkel* im Juragebirge, das *Lunar X* im Kraterdreieck Blanchinus-La Caille-Purbach oder schmale Lichtstrahlen, die durch Kraterwälle auf tiefliegende Ebenen fallen (z. B. der *Barrow-Strahl* oder *Hesiodus-Strahl*).

Da diese Phänomene oft nur für wenige Stunden oder gar Minuten sichtbar sind, erfordert ihre erfolgreiche Beobachtung oder fotografische Dokumentation eine exakte Vorausberechnung. **MoonEvents** berechnet nicht nur das geometrische Optimum der Beleuchtung, sondern prüft für Ihren genauen Standort, ob der Mond am Himmel steht, die Sonne bereits untergegangen ist und wie sich die Mondlibration auf die Sichtbarkeit auswirkt.

---

## 2. Erste Schritte & Programmoberfläche

Nach dem Start von MoonEvents öffnet sich das Hauptfenster. Die Navigation erfolgt über fünf thematische Reiter (Tabs):

1. **Orte:** Verwalten und Aktivieren Ihrer Beobachtungsstandorte.
2. **Ereignisse:** Durchsuchen und Auswählen der gewünschten Mondphänomene.
3. **Berechnung:** Festlegen des Zeitraums, Durchführen des Suchlaufs, Betrachten der Ergebnisse und PDF-Export.
4. **Karte:** Visualisierung der Ereignisse auf der Mondoberfläche inklusive Libration.
5. **Info:** Programminformationen, Versionsnummern und Kontakt.

Alle Einstellungen (gespeicherte Standorte, aktiver Standort und ausgewählte Ereignisse) werden automatisch in der Konfigurationsdatei `mond_einstellungen.json` im Programmverzeichnis gesichert.

---

## 3. Tab: Orte (Standortverwaltung)

Die genaue geografische Position des Beobachters ist entscheidend, um Auf- und Untergangszeiten von Mond und Sonne sowie deren genaue Höhen über dem Horizont zu ermitteln.

### Oberfläche
* **Gespeicherte Orte (linke Liste):** Zeigt alle hinterlegten Standorte an.
* **Ort bearbeiten (rechte Eingabemaske):** Ermöglicht die Eingabe und Modifikation von Standortdaten.

### Felder eines Standorts
* **Name:** Ein frei wählbarer Name (z. B. „Sternwarte München“, „Garten“, „Tiefenbach“).
* **Breite:** Geografische Breite in Dezimalgrad (z. B. `48.137` für 48,137° Nord; südliche Breiten mit Minuszeichen).
* **Länge:** Geografische Länge in Dezimalgrad (z. B. `11.575` für 11,575° Ost; westliche Längen mit Minuszeichen).
* **Höhe (m):** Geländehöhe über Normalnull in Metern. Diese Höhe wird über die barometrische Höhenformel verwendet, um den mittleren Luftdruck und damit die atmosphärische Refraktion am Horizont präzise zu korrigieren.
* **UTC Offset (Winter):** Basis-Zeitzonenverschiebung in Stunden relativ zur koordinierten Weltzeit (für Deutschland/Österreich/Schweiz: `1` für MEZ).
* **Checkbox „Sommerzeit automatisch berücksichtigen (MEZ/MESZ)“:** Ist diese Option aktiv (Standard), ermittelt MoonEvents für jedes Berechnungsdatum automatisch, ob die mitteleuropäische Sommerzeit (MESZ, UTC+2) oder Normalzeit (MEZ, UTC+1) gilt. Manuelle Zeitanpassungen entfallen.

### Aktionen
* **Neu:** Speichert die aktuellen Eingaben als neuen Eintrag in der Liste.
* **Speichern:** Aktualisiert den in der Liste markierten Ort mit den geänderten Eingabefeldern.
* **Löschen:** Entfernt den in der Liste markierten Ort.
* **Aktiv setzen:** Übernimmt den markierten Ort (inklusive etwaiger Änderungen in den Eingabefeldern) als Berechnungsbasis für alle nachfolgenden Suchen. Der derzeit aktive Ort wird unterhalb der Buttons dauerhaft fett angezeigt.

---

## 4. Tab: Ereignisse (Ereignisauswahl)

In diesem Reiter legen Sie fest, welche Mondphänomene in die Berechnung einbezogen werden sollen.

### Datenbank v3.1
Die integrierte Datenbank umfasst **42 verifizierte Clair-obscur-Ereignisse**, die anhand moderner digitaler Mondatlanten und Ephemeriden exakt kalibriert wurden.

### Merkmale der Anzeige
* **Mondalter:** Hinter jedem Ereignisnamen wird in Klammern das mittlere Mondalter in Tagen angezeigt (z. B. `Lunar X (ca. Tag 6.8)`). Dies gibt sofort Aufschluss darüber, in welcher Mondphase das Ereignis auftritt (z. B. Tag 0–14 zunehmender Mond, Tag 15–29 abnehmender Mond).
* **Häkchen:** Markieren Sie die Checkboxen jener Objekte, die Sie beobachten möchten.
* **Schnellauswahl:**
  * **Alle auswählen:** Aktiviert alle 42 Ereignisse mit einem Klick.
  * **Alle abwählen:** Deaktiviert alle Auswahlen, um gezielt nur einzelne Objekte zu selektieren.

Ihre Auswahl wird unmittelbar gespeichert und bleibt beim nächsten Programmstart erhalten.

---

## 5. Tab: Berechnung (Planung & Analyse)

Dieser Reiter bildet das Herzstück der Anwendung. Hier führen Sie die eigentliche Ephemeridenberechnung durch.

### Steuerungsleiste
1. **Start & Ende:** Wählen Sie über das Kalender-Widget das Start- und Enddatum des Suchzeitraums. Standardmäßig ist ein Zeitfenster von 30 Tagen ab dem aktuellen Datum vorgegeben.
2. **Checkbox „Nur gut sichtbare anzeigen“:**  
   Filtert die angezeigte Tabelle in Echtzeit. Ist der Haken gesetzt, werden alle Zeilen ausgeblendet, bei denen das Phänomen von Ihrem Standort aus nicht beobachtbar ist (z. B. am Taghimmel oder unter dem Horizont). Dies spart Zeit bei umfangreichen Suchläufen.
3. **Button „Berechnen“:**  
   Startet den numerischen Suchlauf. Für jedes gewählte Ereignis tastet MoonEvents das Zeitintervall lückenlos ab und löst über das Newton-Verfahren die exakten Zeitpunkte für Beginn, Maximum und Ende der optimalen Beleuchtung.
4. **Button „PDF Export“:**  
   Erzeugt einen druckfertigen DIN-A4-Beobachtungsplan im Querformat.

---

### Ergebnistabelle

Die berechneten Ereignisse werden chronologisch nach Beobachtungszeitpunkt sortiert dargestellt:

| Spalte | Bedeutung |
| :--- | :--- |
| **Ereignis** | Name des Mondphänomens. |
| **Start** | Beginn des Beleuchtungsfensters (Lokalzeit). Ab hier wird das Merkmal sichtbar. |
| **Optimum** | Der **beste sichtbare Zeitpunkt** an Ihrem Standort (siehe [Beobachtungsoptimierung](#intelligente-beobachtungsoptimierung)). |
| **Theor. Optimum** | Der rein geometrisch perfekte Zeitpunkt des Lichteinfalls (unabhängig von Tag/Nacht oder Horizont). |
| **Ende** | Ende des Beleuchtungsfensters (Lokalzeit). Das Phänomen löst sich auf. |
| **Sichtbarkeit** | Statusmeldung zur Beobachtbarkeit (z. B. *Gut beobachtbar*, *Randfenster sichtbar* oder Ausschlussgründe). |
| **Schwierigkeit** | Einstufung der Beobachtung: **Leicht**, **Mittel** oder **Schwer**. |
| **Beschreibung** | Kurzbeschreibung des visuellen Effekts. |

#### Farbliche Kennzeichnung
* **Grüne Schrift:** Das Ereignis ist im angegebenen Zeitraum an Ihrem Standort **gut beobachtbar** (Mond über Horizont, Dämmerung beendet).
* **Rote Schrift:** Das Ereignis ist an Ihrem Standort zur fraglichen Zeit **nicht oder nur eingeschränkt beobachtbar** (z. B. Mond noch unter dem Horizont, Taghimmel, Dämmerung oder Verdeckung durch Libration).

---

### Erweiterte Detail-Ansicht

Ein **Doppelklick** auf eine beliebige Zeile der Ergebnistabelle öffnet ein detailliertes Analysefenster mit allen relevanten astronomischen Parametern:

* **Lokale Zeitangaben:** Exakte Start-, Optimum-, Theor.-Optimum- und Endzeitpunkte.
* **Colongitude (Aktuell / Referenz):**
  Zeigt die aktuelle sonnenselenografische Colongitude am Beobachtungs-Optimum (sowie bei Abweichung zusätzlich am theoretischen Peak) und den kalibrierten Referenzwert bei subsolarer Breite $b_0 = 0^\circ$.
* **Subsolare Breite ($b_0$):**
  Der aktuelle selenografische Breitengrad der Sonne. Weicht $b_0$ von 0° ab, verschiebt sich die Colongitude für das Ereignis geometrisch korrekt.
* **Lokale Sonnenhöhe am Krater:**
  Der effektive Höhenwinkel der Sonne über dem Horizont des Zielkraters (am Beobachtungs-Optimum sowie ggf. am theoretischen Peak; bei Clair-obscur-Effekten typischerweise streifend zwischen $-1^\circ$ und $+4^\circ$).
* **Selenografische Position:**
  Exakte selenografische Koordinaten (Breite und Länge) des Zielobjekts auf dem Mond.
* **Optische Libration (Breite / Länge):**
  Die aktuellen optischen Librationswerte des Mondes ($b$ und $l$).
* **Randabstand & Bewertung:**
  Scheinbarer Winkelabstand von der Scheibenmitte (in Grad) und Beurteilung der Beobachtbarkeit (z. B. *Libration günstig*, *Kritisch nah am Rand* oder *Hinter Mondrand verdeckt*).
* **Mondphase & wahres synodisches Alter:**
  Exaktes Alter des Mondes seit dem tatsächlichen vorherigen Neumond in Tagen (z. B. *Zunehmender Mond (Tag 8.4)*).
* **Ereignisfenster-Dauer:**
  Gesamtdauer des Beleuchtungsfensters in Minuten.
* **Ausführliche Beschreibung:** Volltextbeschreibung des Phänomens.
* **Schwierigkeit & Beobachtungstipps:**
  Konkrete Empfehlungen zur Instrumentenwahl (z. B. Fernglas, 80-mm-Refraktor oder Teleskope ab 150 mm Öffnung), notwendigen Vergrößerungen, Kontrastverhältnissen und Hinweisen auf erforderliche Luftruhe (Seeing).

---

### PDF-Export für den Feldeinsatz

Über die Schaltfläche **„PDF Export“** können Sie Ihre Berechnungen als professionelles Dokument im DIN-A4-Querformat speichern:

* **Modernes & klares Tabellenlayout:** Gestaltet im dunklen Schieferblau (`#1E293B`) mit dezenten, hellgrauen Zellbegrenzungen und alternierender Zebra-Schattierung für ermüdungsfreies Ablesen bei Nacht.
* **Strukturierte Metadaten-Infobox:** Seite 1 enthält eine übersichtliche Kopfkarte mit *Standort*, *Berechnungszeitraum*, *Zeitzone* sowie einer statistischen Gesamt- und Sichtbarkeitsübersicht (sichtbare Phänomene grün hervorgehoben).
* **Automatischer, spaltengenauer Zeilenumbruch:** Alle Spalten – insbesondere auch längere Ereignisnamen (z. B. *„Der Kuss (Promontorium Acherusia)“* oder *„Maginus-Sonnenaufgangsstrahl“*), Sichtbarkeitskriterien und Beschreibungen – werden dynamisch umbrochen, sodass kein Text über Spaltenbegrenzungen hinausragt. Die Zeilenhöhe passt sich flexibel an den längsten Spalteninhalt an.
* **Farbcodierte Zeitfelder & Status:** Zeitpunkte, zu denen das Phänomen von Ihrem Standort aus tatsächlich sichtbar ist (Mond $\ge 5^\circ$, Sonne $\le -6^\circ$), sind in kräftigem Smaragdgrün hervorgehoben; nicht sichtbare Zeiten werden in dezentem Grau dargestellt.
* **Farblich akzentuierte Schwierigkeitsgrade:** Übersichtliche visuelle Unterscheidung nach Beobachtungsanforderung (*Leicht / Sehr Leicht* in Grün, *Mittel* in Bernstein/Orange, *Schwer / Sehr Schwer* in Rot).
* **Mondhöhe:** Bei sichtbaren Ereignissen wird die genaue Höhe des Mondes über dem Horizont beim Optimum in Grad ausgewiesen (z. B. `Gut beobachtbar (Alt: 42.3°)`).
* **Kopf- und Fußzeilen:** Folgeseiten besitzen eine kompakte Kopfzeile mit Standort, Zeitraum und Zeitzone; die Fußzeile weist das Erstellungsdatum, Webadresse und eine genaue Paginierung (`Seite X von Y`) aus.
* **Automatische Zeichensatzbereinigung:** Sonderzeichen (z. B. griechische Buchstaben $\alpha, \beta, \gamma, \delta$, typografische Anführungszeichen, Gedankenstriche und mathematische Symbole) werden zuverlässig aufbereitet.

---

## 6. Tab: Karte (Visualisierung & Libration)

Die Kartenansicht dient der schnellen räumlichen Orientierung auf der Mondoberfläche.

### Features der Mondkarte
* **Orthografische 2D-Projektion:**  
  Die Mondkarte stellt die erdzugewandte Hemisphäre des Mondes dar. Alle in Tab 2 ausgewählten Ereignisse werden als rote Punkte mit gelber Beschriftung eingezeichnet.
* **Kollisionsvermeidung für Beschriftungen:**  
  Liegen mehrere Krater eng beieinander, verschiebt ein intelligenter Layout-Algorithmus die Textlabels automatisch vertikal und zieht weiße Verbindungslinien zum jeweiligen Kraterpunkt.
* **Dynamische Librationskorrektur:**  
  Sobald Sie eine Berechnung durchgeführt haben, ermittelt MoonEvents die optische Libration für das erste beobachtbare Ereignis – oder dynamisch für jedes Ereignis, das Sie in der Ergebnistabelle anklicken. Die Kartenbeschriftung oben rechts zeigt z. B.:
  `Libration (Goldener Henkel, 15.03. 21:30): Breiten-Lib. +4.2°, Längen-Lib. -3.1°`
  Die orthografische Projektion passt sich an diese Libration an: Kraterpunkte wandern entsprechend der tatsächlichen perspektivischen Verkippung des Mondes zur Erde hin oder weg.
* **Checkbox „Nur beobachtbare anzeigen“:**  
  Wird nach einer Berechnung freigeschaltet. Wenn aktiviert, zeigt die Karte ausschließlich jene Objekte, die im gewählten Zeitraum tatsächlich am Nachthimmel Ihres Standorts sichtbar sind. Nicht sichtbare Objekte werden ausgeblendet.

---

## 7. Tab: Info

Hier finden Sie:
* Die aktuelle Versionsnummer des Programms (**1.1.0**).
* Das Release-Datum der aktuellen Fassung (**10.11.2026**).
* Die Version der integrierten Ereignisdatenbank (**Daten-Version: 3.1**).
* Entwickler- und Support-Kontaktdaten ([info@anton-bader.de](mailto:info@anton-bader.de)) sowie einen anklickbaren Weblink zu [https://www.anton-bader.de](https://www.anton-bader.de).

---

## 8. Astronomische & Mathematische Grundlagen

Für astronomisch interessierte Beobachter erläutert dieser Abschnitt die mathematischen Modelle hinter den Berechnungen.

### 2D-sphärische Beleuchtungsberechnung

In vielen einfachen Mondtabellen wird der Zeitpunkt eines Lichteffekts allein über eine feste **Sonnenselenografische Colongitude** ($\text{Colong}$) definiert:

$$\text{Colong} = (90^\circ - L_{sun}) \pmod{360^\circ}$$

wobei $L_{sun}$ die selenografische Länge des Subsolarpunkts ist. Diese 1D-Näherung nimmt jedoch an, dass die Sonne exakt über dem Mondäquator steht (subsolare Breite $b_0 = 0^\circ$).

In der Realität schwankt $b_0$ im Verlauf des drakonitischen Monats zwischen ca. $-1.6^\circ$ und $+1.6^\circ$. Bei hochbreitigen oder polnahen Kratern führt die Neigung der Mondachse dazu, dass die Sonne zu einem anderen Zeitpunkt den kritischen Aufgangswinkel erreicht. Bei Formationen wie dem *Lunar X* (Breite $-25^\circ$) oder dem polnahen *Barrow-Strahl* (Breite $+71.3^\circ$) bewirkt die Abweichung von $b_0$ eine zeitliche Verschiebung von **ca. 1,5 bis zu 9 Stunden**!

MoonEvents 1.1.0 berechnet für jedes Ereignis die Ziel-Sonnenhöhe $h_{target}$ über der sphärischen Höhenformel (wobei die hinterlegte Referenz-Colongitude als Kalibrierwert für $b_0 = 0^\circ$ definiert ist):

$$\sin(h_{sun}) = \sin(\phi) \sin(b_0) + \cos(\phi) \cos(b_0) \sin(\text{Colong} + \lambda)$$

*(mit Kraterbreite $\phi$ und Kraterlänge $\lambda$)*

Über eine inverse sphärische Funktion (`get_effective_target_colong`) wird die exakte dynamische Colongitude für die jeweilige Lunation gelöst, sodass der Lichteinfallswinkel immer präzise stimmt.

---

### Optische Libration und Randeffekt

Da die Mondbahn elliptisch ist (1. Keplersches Gesetz) und die Rotationsachse des Mondes um ca. $6.7^\circ$ gegen seine Bahnebene geneigt ist, führt der Mond von der Erde aus gesehen eine scheinbare Taumelbewegung aus – die **optische Libration**:
* **Libration in Länge ($l$):** Bis zu ca. $\pm 8^\circ$ in Ost-West-Richtung.
* **Libration in Breite ($b$):** Bis zu ca. $\pm 7^\circ$ in Nord-Süd-Richtung.

Für Objekte in der Nähe des Mondrandes (z. B. *Dorsum Oppel* im Mare Crisium) entscheidet die Libration darüber, ob eine Struktur gut einsehbar ist oder auf die Mondrückseite kippt. MoonEvents berechnet die Randdistanz $\Delta_{center}$:

$$\cos(\Delta_{center}) = \sin(\phi)\sin(b) + \cos(\phi)\cos(b)\cos(\lambda - l)$$

Liegt $\Delta_{center} \ge 89.0^\circ$, wird das Ereignis als *„Hinter Mondrand (Libration)“* deklariert und als unsichtbar gewertet.

---

### Reale Standortsichtbarkeit

Ein Ereignis wird nur dann als beobachtbar gewertet, wenn beide folgenden Bedingungen gleichzeitig erfüllt sind:

1. **Mondhöhe $\ge 5.0^\circ$:**  
   Bei weniger als 5° über dem Horizont verhindern Dunst, Gebäude und starke atmosphärische Turbulenz eine lohnende astronomische Beobachtung.
2. **Sonnenhöhe $\le -6.0^\circ$ (Ende der bürgerlichen Dämmerung):**  
   Erst wenn die Sonne mindestens 6° unter dem mathematischen Horizont steht, ist der Himmel ausreichend dunkel, um feine Kontraste auf dem Mond wahrzunehmen.

#### Atmosphärische Refraktion & Barometrische Höhe
Die scheinbare Hebung von Gestirnen nahe dem Horizont hängt vom Luftdruck ab. MoonEvents passt den Luftdruck $P$ im Berechnungsmodul `ephem` über die barometrische Höhenformel an die vom Benutzer angegebene Geländehöhe $h$ an:

$$P = 1010.0 \cdot \left(1.0 - \frac{0.0065 \cdot h}{288.15}\right)^{5.255} \quad [\text{hPa}]$$

---

### Intelligente Beobachtungsoptimierung

Tritt das geometrisch perfekte Beleuchtungsoptimum (*Theor. Optimum*) tagsüber, bei untergegangenem Mond oder bei sehr tiefem Mondstand ($< 15^\circ$) ein, prüft MoonEvents das gesamte Zeitfenster des Ereignisses ($\pm \text{halbe Dauer}$):

1. Es wird in präzisen Schritten von **2 Minuten** abgetastet, ob ein Teil des Zeitfensters in die Nacht fällt und der Mond über $5^\circ$ steht.
2. Werden mehrere sichtbare Momente gefunden, bewertet eine Scoring-Funktion den besten Kompromiss aus:
   * Geringstem Zeitabstand zum theoretischen Maximum.
   * Größter Dunkelheit (Sonnenstand möglichst tief unter $-6^\circ$).
   * Größter Mondhöhe über dem Horizont.
3. War das theoretische Maximum unsichtbar, wird der gefundene Zeitpunkt in der Tabelle als **Optimum** ausgewiesen und mit dem Status *„Randfenster sichtbar“* gekennzeichnet.

---

### Wahres synodisches Mondalter

Frühere Systeme schätzten das Mondalter oft grob über eine lineare Division der Colongitude ab ($\text{Tag} \approx \text{Colong} / 12.2$). Da die Mondbahn jedoch elliptisch ist, schwankt die Dauer einer Lunation zwischen 29,27 und 29,83 Tagen. 

MoonEvents bestimmt das wahre synodische Mondalter exakt, indem der genaue Ephemeriden-Zeitpunkt des unmittelbar vorausgegangenen Neumonds (`ephem.previous_new_moon`) von der Beobachtungszeit subtrahiert wird.

---

## 9. Häufige Fragen & Troubleshooting (FAQ)

### 1. Warum weichen manche Peak-Zeiten um mehrere Stunden von älteren Mondtabellen ab?
Ältere Verzeichnisse verwendeten meist eine statische 1D-Colongitude bei $b_0=0^\circ$. MoonEvents 1.1.0 berücksichtigt die reale subsolare Breite $b_0$. Für Krater abseits des Mondäquators ist die von MoonEvents berechnete Zeit der tatsächliche physikalische Moment, in dem die Referenz-Sonnenhöhe erreicht wird.

### 2. Was bedeutet der Status „Randfenster sichtbar“?
Das theoretische Maximum findet statt, während der Mond an Ihrem Standort noch unter dem Horizont steht oder die Sonne noch scheint. Doch vor Ende des Beleuchtungsfensters geht der Mond auf (oder es wird dunkel), sodass Sie das Phänomen noch in seiner Endphase beobachten können.

### 3. Warum wird ein Ereignis als „Hinter Mondrand (Libration)“ angezeigt?
Das Phänomen liegt geografisch nahe am Mondrand. Durch ungünstige optische Libration zum Ereigniszeitpunkt ist das Objekt auf die Mondrückseite rotiert und von der Erde aus nicht einsehbar.

### 4. Wo speichert MoonEvents meine Daten?
Alle Einstellungen werden in der Datei `mond_einstellungen.json` im Programmverzeichnis gespeichert. Wenn Sie die Anwendung als kompilierte `.exe` nutzen, wird diese Datei automatisch neben der ausführbaren Datei abgelegt.

### 5. Wie verhält sich das PDF bei langen Texten und Ereignisnamen?
Das PDF-Layout ist dynamisch aufgebaut: Wenn ein Ereignisname, ein Sichtbarkeitsstatus oder ein Beschreibungstext länger als die verfügbare Spaltenbreite ist, wird der Text automatisch an Wort-, Binde- oder Schrägstrichgrenzen in mehrere Zeilen umgebrochen. Die Zeilenhöhe passt sich dabei exakt an den Inhalt an, sodass benachbarte Zellen weder überdeckt noch abgeschnitten werden. Bei Überschreiten der Seitenhöhe wird automatisch eine Folgeseite mit kompakter Kopfzeile und wiederholtem Spaltenkopf erzeugt.
