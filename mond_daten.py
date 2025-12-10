# mond_daten.py

"""
Datenbank für lunare Clair-obscur-Ereignisse (Licht- und Schattenspiele).
Die Colongitude (Sonnenselenografische Länge) ist der entscheidende Faktor
für den Sonnenstand über dem Mondhorizont.

Kalibrierung: Stand 2025/2026 (Referenzwerte optimiert für realistische Sichtbarkeit)
"""

EREIGNISSE_DB = [
    # --- ZUNEHMENDER MOND (Tag 0 bis ca. 14) ---
    {
        "name": "Larrieus Staudamm", 
        "colong": 343.0, 
        "duration_min": 120,
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
        "colong": 356.0, 
        "duration_min": 90,
        "desc": "Ein schmaler Sonnenlichtstrahl fällt durch eine Lücke im westlichen Kraterwall von Barrow (Polregion).",
        "phase": "Zunehmend",
        "lat": 71.3, "lon": 10.0
    },
    {
        "name": "Lunar X (Werner X)", 
        "colong": 357.3, 
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
        "lat": 8.0, "lon": 1.5
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
        "duration_min": 60, # Sehr kurzlebig
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
        "lat": 12.0, "lon": 22.0
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
        "name": "Augen des Clavius", 
        "colong": 15.0, 
        "duration_min": 180,
        "desc": "Die kleinen Krater C und D im riesigen, dunklen Clavius fangen das erste Licht und wirken wie zwei Augen.",
        "phase": "Zunehmend",
        "lat": -58.4, "lon": -14.4
    },
    {
        "name": "Hesiodus-Strahl", 
        "colong": 16.0, 
        "duration_min": 75, 
        "desc": "Ein spektakulärer Lichtstrahl fällt durch eine Lücke im Wall von Pitatus in den noch dunklen Krater Hesiodus.",
        "phase": "Zunehmend",
        "lat": -29.4, "lon": -16.3
    },
    {
        "name": "Platos Haken", 
        "colong": 15.6, 
        "duration_min": 120,
        "desc": "Der Schatten des Kraterrandes bildet einen gekrümmten Haken auf dem glatten Boden von Plato.",
        "phase": "Zunehmend",
        "lat": 51.6, "lon": -9.3
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
        "name": "Goldener Henkel", 
        "colong": 34.8, 
        "duration_min": 600, 
        "desc": "Die Bergkette Montes Jura leuchtet als isolierter Bogen hoch über dem Terminator, während die Regenbogebucht noch im Schatten liegt.",
        "phase": "Zunehmend",
        "lat": 47.0, "lon": -34.0
    },
    {
        "name": "Mondjungfrau (Kap Heraclides)", 
        "colong": 35.0, 
        "duration_min": 300, 
        "desc": "Kap Heraclides am Ende des Jura-Gebirges sieht bei diesem Licht aus wie das Profil einer Frau mit wehenden Haaren.",
        "phase": "Zunehmend",
        "lat": 40.7, "lon": -33.2
    },
    {
        "name": "Kobra-Kopf (Vallis Schröteri)", 
        "colong": 58.0, 
        "duration_min": 240,
        "desc": "Das Aristarchus-Plateau und das breite Ende des Vallis Schröteri ähneln dem Kopf einer Kobra.",
        "phase": "Zunehmend",
        "lat": 26.0, "lon": -51.0
    },
    
    # --- ABNEHMENDER MOND (Tag 15 bis ca. 29) ---
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
        "name": "Arago-Lichtfleck", 
        "colong": 176.0, 
        "duration_min": 60, 
        "desc": "Ein kurzlebiger Lichteffekt an den Arago-Domen beim Sonnenuntergang.",
        "phase": "Abnehmend",
        "lat": 6.2, "lon": 21.4
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
        "name": "Inverser Goldener Henkel", 
        "colong": 216.0, 
        "duration_min": 420, 
        "desc": "Sonnenuntergang am Jura-Gebirge. Die Spitzen leuchten als letzte Strukturen über der Regenbogebucht in die Nacht hinein.",
        "phase": "Abnehmend",
        "lat": 47.0, "lon": -34.0
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