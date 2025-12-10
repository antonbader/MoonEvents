# mond_daten.py

"""
Datenbank für lunare Clair-obscur-Ereignisse (Licht- und Schattenspiele).
Die Colongitude (Sonnenselenografische Länge) ist der entscheidende Faktor
für den Sonnenstand über dem Mondhorizont.

Kalibrierung: Stand 2025/2026 (Referenzwerte optimiert für realistische Sichtbarkeit)
Version: 2.1 - Geodaten integriert & Sonnenuntergangs-Phasen korrigiert
"""

EREIGNISSE_DB = [
    # --- ZUNEHMENDER MOND (Tag 0 bis ca. 14) ---
    {
        "name": "Larrieus Staudamm", 
        "colong": 343.0, 
        "duration_min": 180,
        "desc": "Kleine, beleuchtete Erhebung im Krater Polybius K, die wie eine Staumauer wirkt (kurz vor Erstes Viertel).",
        "phase": "Zunehmend",
        "lat": -24.5, "lon": 25.5
    },
    {
        "name": "Die Schnecke (Hyginus)", 
        "colong": 356.0, 
        "duration_min": 120,
        "desc": "Im Krater Hyginus und der Rima Hyginus. Schatten wirken beim Sonnenaufgang wie eine kriechende Schnecke.",
        "phase": "Zunehmend",
        "lat": 7.8, "lon": 6.3
    },
    {
        "name": "Barrow-Strahl",
        "colong": 356.6, 
        "duration_min": 90,
        "desc": "Ein schmaler Sonnenlichtstrahl fällt durch eine Lücke im westlichen Kraterwall von Barrow (Polregion).",
        "phase": "Zunehmend",
        "lat": 71.3, "lon": 10.0
    },
    {
        "name": "Lunar X (Werner X)", 
        "colong": 357.3, # KORRIGIERT: Kalibriert auf 17:20 Uhr Peak (statt 356.8)
        "duration_min": 150, 
        "desc": "Der Klassiker: Die Kraterränder von Blanchinus, La Caille und Purbach bilden ein leuchtendes 'X'.",
        "phase": "Zunehmend",
        "lat": -25.5, "lon": 1.0
    },
    {
        "name": "Widder-Hufabdruck", 
        "colong": 358.0, 
        "duration_min": 180,
        "desc": "Westlich von Ukert bilden zwei kleine Krater und deren Schattenwurf einen Hufabdruck (nahe Lunar V).",
        "phase": "Zunehmend",
        "lat": 7.7, "lon": 1.4
    },
    {
        "name": "Lunar V", 
        "colong": 358.5, 
        "duration_min": 150,
        "desc": "Oft gleichzeitig mit dem Lunar X sichtbar. Östlich des Kraters Ukert bilden beleuchtete Hügelkämme ein helles 'V'.",
        "phase": "Zunehmend",
        "lat": 7.8, "lon": 1.3
    },
    {
        "name": "Lunar Alpha", 
        "colong": 359.0, 
        "duration_min": 120,
        "desc": "Zwischen den Kratern Davy Y und Davy A bilden Hügel und Schatten ein griechisches Alpha (α).",
        "phase": "Zunehmend",
        "lat": -11.8, "lon": -8.1
    },
    {
        "name": "Gesicht in Albategnius", 
        "colong": 3.5, 
        "duration_min": 120, 
        "desc": "Der Schatten des Zentralbergs im Krater Albategnius formt beim Sonnenaufgang ein markantes menschliches Profil.",
        "phase": "Zunehmend",
        "lat": -11.2, "lon": 4.0
    },
    {
        "name": "Maginus-Sonnenaufgangsstrahl", 
        "colong": 6.8, 
        "duration_min": 60,
        "desc": "Ein Sonnenstrahl durchbricht den Wall von Maginus und beleuchtet den Kraterboden. Ein flüchtiges Ereignis.",
        "phase": "Zunehmend",
        "lat": -50.0, "lon": -6.0
    },
    {
        "name": "Der Kuss (Promontorium Acherusia)", 
        "colong": 11.0, 
        "duration_min": 120,
        "desc": "Am Kap Promontorium Acherusia (Rand des Mare Serenitatis). Schatten wirken wie zwei sich küssende Gesichter.",
        "phase": "Zunehmend",
        "lat": 40.0, "lon": 22.0
    },
    {
        "name": "Langer Schatten des Eratosthenes", 
        "colong": 11.8, 
        "duration_min": 180,
        "desc": "Der tiefe Krater Eratosthenes wirft beim Sonnenaufgang einen extrem langen, spitzen Schatten in das Mare Imbrium.",
        "phase": "Zunehmend",
        "lat": 14.5, "lon": -11.3
    },
    {
        "name": "Platos Nessie", 
        "colong": 13.5, 
        "duration_min": 90, 
        "desc": "Ein länglicher Schatten der Kraterwand auf dem Boden von Plato erinnert an den Hals von Nessie.",
        "phase": "Zunehmend",
        "lat": 51.6, "lon": -9.3
    },
    {
        "name": "Platos Haken", 
        "colong": 14.2, 
        "duration_min": 120,
        "desc": "Der Schatten des Kraterrandes bildet einen gekrümmten Haken auf dem glatten Boden von Plato.",
        "phase": "Zunehmend",
        "lat": 51.6, "lon": -9.3
    },
    {
        "name": "Augen des Clavius", 
        "colong": 15.0, 
        "duration_min": 180,
        "desc": "Die kleinen Krater C und D im riesigen, dunklen Clavius fangen das erste Licht und wirken wie zwei Augen.",
        "phase": "Zunehmend",
        "lat": -58.4, "lon": -14.4
    },
    {
        "name": "Hesiodus-Strahl", 
        "colong": 16.9, 
        "duration_min": 60, 
        "desc": "Ein spektakulärer Lichtstrahl fällt durch eine Lücke im Wall von Pitatus in den noch dunklen Krater Hesiodus.",
        "phase": "Zunehmend",
        "lat": -29.4, "lon": -16.3
    },
    {
        "name": "Mond-Quincunx (Würfel-Fünf)", 
        "colong": 21.0, 
        "duration_min": 120,
        "desc": "Fünf beleuchtete Bergspitzen nördlich von Kopernikus, angeordnet wie die Zahl 5 auf einem Würfel.",
        "phase": "Zunehmend",
        "lat": 9.7, "lon": -20.0
    },
    {
        "name": "Tycho-Sonnenaufgang", 
        "colong": 27.0, 
        "duration_min": 240,
        "desc": "Der Zentralberg von Tycho fängt das erste Licht und leuchtet wie eine Leuchtturm im dunklen Kraterboden.",
        "phase": "Zunehmend",
        "lat": -43.3, "lon": -11.2
    },
    {
        "name": "Goldener Henkel", 
        "colong": 32.5, 
        "duration_min": 600, 
        "desc": "Die Bergkette Montes Jura leuchtet als isolierter Bogen hoch über dem Terminator, während die Regenbogebucht noch im Schatten liegt.",
        "phase": "Zunehmend",
        "lat": 47.0, "lon": -34.0
    },
    {
        "name": "Mondjungfrau (Kap Heraclides)", 
        "colong": 32.5, 
        "duration_min": 300, 
        "desc": "Kap Heraclides am Ende des Jura-Gebirges sieht bei diesem Licht aus wie das Profil einer Frau mit wehenden Haaren.",
        "phase": "Zunehmend",
        "lat": 40.7, "lon": -33.2
    },
    {
        "name": "Dorsum Oppel Lichtpunkte", 
        "colong": 43.0, 
        "duration_min": 180,
        "desc": "Eine Kette von Hügeln im Mare Crisium (Dorsum Oppel) leuchtet wie eine Perlenkette beim Sonnenaufgang.",
        "phase": "Zunehmend",
        "lat": 28.0, "lon": 52.0
    },
    {
        "name": "Schröters Tal Sonnenaufgang", 
        "colong": 55.0, 
        "duration_min": 240,
        "desc": "Das gewundene Vallis Schröteri wird spektakulär beleuchtet, die Windungen und Terrassen treten plastisch hervor.",
        "phase": "Zunehmend",
        "lat": 26.2, "lon": -50.8
    },
    {
        "name": "Kobra-Kopf (Vallis Schröteri)", 
        "colong": 56.5, 
        "duration_min": 240,
        "desc": "Das Aristarchus-Plateau und das breite Ende des Vallis Schröteri ähneln dem Kopf einer Kobra.",
        "phase": "Zunehmend",
        "lat": 26.0, "lon": -51.0
    },
    {
        "name": "Aristarchus-Strahlen", 
        "colong": 57.0, 
        "duration_min": 360,
        "desc": "Der hellste Krater des Mondes zeigt seine spektakulären Strahlensysteme bei schrägem Lichteinfall besonders eindrucksvoll.",
        "phase": "Zunehmend",
        "lat": 23.7, "lon": -47.4
    },
    
    # --- ABNEHMENDER MOND (Tag 15 bis ca. 29) ---
    {
        "name": "Messier-Zwillinge", 
        "colong": 95.0, 
        "duration_min": 180,
        "desc": "Die beiden ovalen Krater Messier und Messier A mit ihren asymmetrischen Strahlensystemen beim Sonnenuntergang.",
        "phase": "Abnehmend",
        "lat": -1.9, "lon": 47.6
    },
    {
        "name": "Taruntius-Terrassierung", 
        "colong": 102.0, 
        "duration_min": 240,
        "desc": "Die konzentrische Terrassenstruktur im Krater Taruntius wird bei niedrigem Sonnenstand spektakulär sichtbar.",
        "phase": "Abnehmend",
        "lat": 5.6, "lon": 46.5
    },
    {
        "name": "Liebespaar im Mond", 
        "colong": 117.6, 
        "duration_min": 150,
        "desc": "Promontorium Agarum im Mare Crisium. Beim abnehmenden Mond erzeugen Schatten zwei Gesichter.",
        "phase": "Abnehmend",
        "lat": 14.0, "lon": 66.0
    },
    {
        "name": "O'Neills Brücke", 
        "colong": 124.0, 
        "duration_min": 120, 
        "desc": "Zwischen Kap Promontorium Olivium und Lavinium. Ein Schattenspiel täuschte früher Astronomen eine künstliche Brücke vor.",
        "phase": "Abnehmend",
        "lat": 15.0, "lon": 58.0
    },
    {
        "name": "Proclus Asymmetrie", 
        "colong": 133.0, 
        "duration_min": 180,
        "desc": "Der junge Krater Proclus zeigt sein asymmetrisches Strahlensystem beim Sonnenuntergang besonders deutlich.",
        "phase": "Abnehmend",
        "lat": 16.1, "lon": 46.8
    },
    {
        "name": "Atlas-Kratergruben", 
        "colong": 142.0, 
        "duration_min": 150,
        "desc": "Die mysteriösen dunklen Flecken im Kraterboden von Atlas werden bei schrägem Licht als Vertiefungen erkennbar.",
        "phase": "Abnehmend",
        "lat": 46.7, "lon": 44.4
    },
    {
        "name": "Posidonius-Rillen-System", 
        "colong": 148.0, 
        "duration_min": 240,
        "desc": "Das komplexe System von Rimae Posidonius im Kraterboden zeigt sich bei Sonnenuntergang am besten.",
        "phase": "Abnehmend",
        "lat": 31.8, "lon": 29.9
    },
    {
        "name": "Linné-Rätsel", 
        "colong": 165.0, 
        "duration_min": 120,
        "desc": "Der kleine, helle Krater Linné im Mare Serenitatis zeigt bei diesem Lichtstand seine wahre Tiefe.",
        "phase": "Abnehmend",
        "lat": 27.7, "lon": 11.8
    },
    {
        "name": "Arago-Lichtfleck", 
        "colong": 176.0, 
        "duration_min": 60, 
        "desc": "Die Arago-Alpha- und Beta-Dome werfen beim Sonnenuntergang markante Schatten und zeigen einen kurzen Lichtblitz auf ihren Gipfeln.",
        "phase": "Abnehmend",
        "lat": 6.2, "lon": 21.4
    },
    {
        "name": "Triesnecker-Rillensystem", 
        "colong": 178.0, 
        "duration_min": 240,
        "desc": "Das verzweigte Rillensystem Rimae Triesnecker wird bei niedrigem Sonnenuntergang spektakulär sichtbar.",
        "phase": "Abnehmend",
        "lat": 4.2, "lon": 3.6
    },
    {
        "name": "Gruithuisens Mondstadt", 
        "colong": 185.0, 
        "duration_min": 240, 
        "desc": "Fischgrätenartige Bergrücken nördlich von Schröter, die geometrisch wie eine Ruinenstadt wirken (beste Sicht bei Sonnenuntergang).",
        "phase": "Abnehmend",
        "lat": 36.0, "lon": -40.0
    },
    {
        "name": "Curtiss-Kreuz", 
        "colong": 193.5, 
        "duration_min": 120,
        "desc": "Die Wälle des kleinen Kraters Fra Mauro Zeta bilden beim abnehmenden Mond ein leuchtendes Kreuz.",
        "phase": "Abnehmend",
        "lat": -3.7, "lon": -17.0
    },
    {
        "name": "Pitatus Sunset Ray", 
        "colong": 194.0, 
        "duration_min": 60, 
        "desc": "Gegenstück zum Hesiodus-Strahl: Ein letzter Lichtstrahl beim Sonnenuntergang in Pitatus.",
        "phase": "Abnehmend",
        "lat": -29.8, "lon": -13.5
    },
    {
        "name": "Gassendi-Rillenlabyrinth", 
        "colong": 200.0, 
        "duration_min": 240,
        "desc": "Das komplexe Rillensystem im Kraterboden von Gassendi zeigt sich bei Sonnenuntergang am eindrucksvollsten.",
        "phase": "Abnehmend",
        "lat": -17.5, "lon": -40.1
    },
    {
        "name": "Tycho-Sonnenuntergang", 
        "colong": 207.0, 
        "duration_min": 240,
        "desc": "Der Zentralberg von Tycho fängt das letzte Licht und glüht wie eine Fackel im dunklen Kraterboden.",
        "phase": "Abnehmend",
        "lat": -43.3, "lon": -11.2
    },
    {
        "name": "Wargentin-Plateau", 
        "colong": 212.0, 
        "duration_min": 180,
        "desc": "Der einzigartige, bis zum Rand mit Lava gefüllte Krater Wargentin zeigt seine ebene Oberfläche im Kontrast zur Umgebung.",
        "phase": "Abnehmend",
        "lat": -49.6, "lon": -60.2
    },
    {
        "name": "Inverser Goldener Henkel", 
        "colong": 217.0, # KORRIGIERT: War 319.5 (Falsch). Sunset = Sunrise (35) + 180 = ~215-218.
        "duration_min": 420, 
        "desc": "Sonnenuntergang am Jura-Gebirge. Die Spitzen leuchten als letzte Strukturen über der Regenbogebucht in die Nacht hinein.",
        "phase": "Abnehmend",
        "lat": 47.0, "lon": -34.0
    },
    {
        "name": "Mondjungfrau Abschied", 
        "colong": 218.0, # KORRIGIERT: War 319.5 (Falsch). Folgt dem Goldenen Henkel beim Untergang.
        "duration_min": 300,
        "desc": "Kap Heraclides beim Sonnenuntergang - das Profil der Mondjungfrau versinkt im Schatten.",
        "phase": "Abnehmend",
        "lat": 40.7, "lon": -33.2
    },
    {
        "name": "Eratosthenes letzter Schatten", 
        "colong": 191.8, # KORRIGIERT: War 329.0 (Falsch). Sunrise (11.8) + 180 = 191.8.
        "duration_min": 180,
        "desc": "Der Krater Eratosthenes wirft beim Sonnenuntergang einen langen Schatten über das Mare Imbrium.",
        "phase": "Abnehmend",
        "lat": 14.5, "lon": -11.3
    }
]

def get_default_location():
    return {
        "name": "Günzburg",
        "lat": 48.45,
        "lon": 10.27,
        "elevation": 440,
        "timezone_offset": 1 
    }