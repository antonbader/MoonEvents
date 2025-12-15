# mond_daten.py

"""
Datenbank für lunare Clair-obscur-Ereignisse (Licht- und Schattenspiele).
Die Colongitude (Sonnenselenografische Länge) ist der entscheidende Faktor
für den Sonnenstand über dem Mondhorizont.

Kalibrierung: Stand 2025/2026 (Referenzwerte optimiert für realistische Sichtbarkeit)
Version: 2.3 - Schwierigkeit + Tipps integriert
"""

DB_VERSION = "2.3"

EREIGNISSE_DB = [
    # --- ZUNEHMENDER MOND (Tag 0 bis ca. 14) ---
    {
        "name": "Larrieus Staudamm", 
        "colong": 343.0, 
        "duration_min": 180,
        "desc": "Kleine, beleuchtete Erhebung im Krater Polybius K, die wie eine Staumauer wirkt (kurz vor Erstes Viertel).",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Kleine, aber markant durch die gerade Linie. Erfordert gutes Timing.",
        "lat": -24.5, "lon": 25.5
    },
    {
        "name": "Die Schnecke (Hyginus)", 
        "colong": 356.0, 
        "duration_min": 120,
        "desc": "Im Krater Hyginus und der Rima Hyginus. Schatten wirken beim Sonnenaufgang wie eine kriechende Schnecke.",
        "phase": "Zunehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Hyginus ist klein; die 'Schneckenform' erfordert ruhige Luft (Seeing).",
        "lat": 7.8, "lon": 6.3
    },
    {
        "name": "Barrow-Strahl", 
        "colong": 356.6, 
        "duration_min": 90,
        "desc": "Ein schmaler Sonnenlichtstrahl fällt durch eine Lücke im westlichen Kraterwall von Barrow (Polregion).",
        "phase": "Zunehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Sehr kurzes Zeitfenster (90 min) und ungünstige Lage am Pol (Libration beachten).",
        "lat": 71.3, "lon": 10.0
    },
    {
        "name": "Lunar X (Werner X)", 
        "colong": 357.3, # KORRIGIERT: Kalibriert auf 17:20 Uhr Peak (statt 356.8)
        "duration_min": 150,
        "desc": "Der Klassiker: Die Kraterränder von Blanchinus, La Caille und Purbach bilden ein leuchtendes 'X'.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Sehr bekannt, aber das Zeitfenster ist strikt (Peak ~1 Std). Leicht zu finden, wenn das Timing stimmt.",
        "lat": -25.5, "lon": 1.0
    },
    {
        "name": "Widder-Hufabdruck", 
        "colong": 358.0, 
        "duration_min": 180,
        "desc": "Westlich von Ukert bilden zwei kleine Krater und deren Schattenwurf einen Hufabdruck (nahe Lunar V).",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Nahe Lunar V, aber kleiner. Gute Optik nötig.",
        "lat": 7.7, "lon": 1.4
    },
    {
        "name": "Lunar V", 
        "colong": 358.5, 
        "duration_min": 150,
        "desc": "Oft gleichzeitig mit dem Lunar X sichtbar. Östlich des Kraters Ukert bilden beleuchtete Hügelkämme ein helles 'V'.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Etwas leichter/länger sichtbar als das X, markante Form.",
        "lat": 7.8, "lon": 1.3
    },
    {
        "name": "Lunar Alpha", 
        "colong": 359.0, 
        "duration_min": 120,
        "desc": "Zwischen den Kratern Davy Y und Davy A bilden Hügel und Schatten ein griechisches Alpha (α).",
        "phase": "Zunehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Das 'A' ist klein und erfordert höhere Vergrößerung.",
        "lat": -11.8, "lon": -8.1
    },
    {
        "name": "Gesicht in Albategnius", 
        "colong": 3.5, 
        "duration_min": 120,
        "desc": "Der Schatten des Zentralbergs im Krater Albategnius formt beim Sonnenaufgang ein markantes menschliches Profil.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Schattenspiel; erfordert etwas Fantasie ('Pareidolie').",
        "lat": -11.2, "lon": 4.0
    },
    {
        "name": "Maginus-Sonnenaufgangsstrahl", 
        "colong": 6.8, 
        "duration_min": 60,
        "desc": "Ein Sonnenstrahl durchbricht den Wall von Maginus und beleuchtet den Kraterboden. Ein flüchtiges Ereignis.",
        "phase": "Zunehmend",
        "difficulty": "Sehr Schwer",
        "difficulty_tip": "Extrem kurz (60 min) und tief im Süden.",
        "lat": -50.0, "lon": -6.0
    },
    {
        "name": "Der Kuss (Promontorium Acherusia)", 
        "colong": 11.0, 
        "duration_min": 120,
        "desc": "Am Kap Promontorium Acherusia (Rand des Mare Serenitatis). Schatten wirken wie zwei sich küssende Gesichter.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Hängt stark vom persönlichen Eindruck ab, die Kaps sind aber leicht zu finden.",
        "lat": 40.0, "lon": 22.0
    },
    {
        "name": "Langer Schatten des Eratosthenes", 
        "colong": 11.8, 
        "duration_min": 180,
        "desc": "Der tiefe Krater Eratosthenes wirft beim Sonnenaufgang einen extrem langen, spitzen Schatten in das Mare Imbrium.",
        "phase": "Zunehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Sehr auffällig, riesiger Schatten, langes Zeitfenster.",
        "lat": 14.5, "lon": -11.3
    },
    {
        "name": "Platos Nessie", 
        "colong": 13.5, 
        "duration_min": 90,
        "desc": "Ein länglicher Schatten der Kraterwand auf dem Boden von Plato erinnert an den Hals von Nessie.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Plato ist leicht zu finden, der Schattenhals braucht aber ruhige Luft.",
        "lat": 51.6, "lon": -9.3
    },
    {
        "name": "Platos Haken", 
        "colong": 14.2, 
        "duration_min": 120,
        "desc": "Der Schatten des Kraterrandes bildet einen gekrümmten Haken auf dem glatten Boden von Plato.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Ähnlich wie Nessie, gut beobachtbar.",
        "lat": 51.6, "lon": -9.3
    },
    {
        "name": "Augen des Clavius", 
        "colong": 15.0, 
        "duration_min": 180,
        "desc": "Die kleinen Krater C und D im riesigen, dunklen Clavius fangen das erste Licht und wirken wie zwei Augen.",
        "phase": "Zunehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Clavius ist riesig, die 'Augen' (Krater C & D) sind sehr kontrastreich.",
        "lat": -58.4, "lon": -14.4
    },
    {
        "name": "Hesiodus-Strahl", 
        "colong": 16.9, 
        "duration_min": 60,
        "desc": "Ein spektakulärer Lichtstrahl fällt durch eine Lücke im Wall von Pitatus in den noch dunklen Krater Hesiodus.",
        "phase": "Zunehmend",
        "difficulty": "Sehr Schwer",
        "difficulty_tip": "Der 'Heilige Gral'. Nur ca. 45-60 Min sichtbar, braucht Lücke im Kraterwall.",
        "lat": -29.4, "lon": -16.3
    },
    {
        "name": "Mond-Quincunx (Würfel-Fünf)", 
        "colong": 21.0, 
        "duration_min": 120,
        "desc": "Fünf beleuchtete Bergspitzen nördlich von Kopernikus, angeordnet wie die Zahl 5 auf einem Würfel.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Mustererkennung nötig, aber die Lichtpunkte sind hell.",
        "lat": 9.7, "lon": -20.0
    },
    {
        "name": "Tycho-Sonnenaufgang", 
        "colong": 27.0, 
        "duration_min": 240,
        "desc": "Der Zentralberg von Tycho fängt das erste Licht und leuchtet wie eine Leuchtturm im dunklen Kraterboden.",
        "phase": "Zunehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Tycho ist extrem hell und auffällig. Der Zentralberg leuchtet wie eine Nadel.",
        "lat": -43.3, "lon": -11.2
    },
    {
        "name": "Goldener Henkel", 
        "colong": 32.5, 
        "duration_min": 600,
        "desc": "Die Bergkette Montes Jura leuchtet als isolierter Bogen hoch über dem Terminator, während die Regenbogebucht noch im Schatten liegt.",
        "phase": "Zunehmend",
        "difficulty": "Sehr Leicht",
        "difficulty_tip": "Schon im Fernglas sichtbar. Sehr langes Zeitfenster.",
        "lat": 47.0, "lon": -34.0
    },
    {
        "name": "Mondjungfrau (Kap Heraclides)", 
        "colong": 32.5, 
        "duration_min": 300,
        "desc": "Kap Heraclides am Ende des Jura-Gebirges sieht bei diesem Licht aus wie das Profil einer Frau mit wehenden Haaren.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Profil ist gut erkennbar, wenn man weiß, wo man am Kap Heraclides schauen muss.",
        "lat": 40.7, "lon": -33.2
    },
    {
        "name": "Dorsum Oppel Lichtpunkte", 
        "colong": 43.0, 
        "duration_min": 180,
        "desc": "Eine Kette von Hügeln im Mare Crisium (Dorsum Oppel) leuchtet wie eine Perlenkette beim Sonnenaufgang.",
        "phase": "Zunehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Geringer Kontrast im Mare, schwer als 'Perlenkette' aufzulösen.",
        "lat": 28.0, "lon": 52.0
    },
    {
        "name": "Schröters Tal Sonnenaufgang", 
        "colong": 55.0, 
        "duration_min": 240,
        "desc": "Das gewundene Vallis Schröteri wird spektakulär beleuchtet, die Windungen und Terrassen treten plastisch hervor.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Tal ist groß, aber die Struktur im Inneren braucht gute Optik.",
        "lat": 26.2, "lon": -50.8
    },
    {
        "name": "Kobra-Kopf (Vallis Schröteri)", 
        "colong": 56.5, 
        "duration_min": 240,
        "desc": "Das Aristarchus-Plateau und das breite Ende des Vallis Schröteri ähneln dem Kopf einer Kobra.",
        "phase": "Zunehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Teil von Schröters Tal, markante Form.",
        "lat": 26.0, "lon": -51.0
    },
    {
        "name": "Aristarchus-Strahlen", 
        "colong": 57.0, 
        "duration_min": 360,
        "desc": "Der hellste Krater des Mondes zeigt seine spektakulären Strahlensysteme bei schrägem Lichteinfall besonders eindrucksvoll.",
        "phase": "Zunehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Hellster Fleck auf dem Mond, kaum zu übersehen.",
        "lat": 23.7, "lon": -47.4
    },
    
    # --- ABNEHMENDER MOND (Tag 15 bis ca. 29) ---
    {
        "name": "Messier-Zwillinge", 
        "colong": 95.0, 
        "duration_min": 180,
        "desc": "Die beiden ovalen Krater Messier und Messier A mit ihren asymmetrischen Strahlensystemen beim Sonnenuntergang.",
        "phase": "Abnehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Die 'Kometenschweif'-Form ist markant, Krater sind aber klein.",
        "lat": -1.9, "lon": 47.6
    },
    {
        "name": "Taruntius-Terrassierung", 
        "colong": 102.0, 
        "duration_min": 240,
        "desc": "Die konzentrische Terrassenstruktur im Krater Taruntius wird bei niedrigem Sonnenstand spektakulär sichtbar.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Konzentrische Ringe brauchen sehr flaches Licht und gutes Seeing.",
        "lat": 5.6, "lon": 46.5
    },
    {
        "name": "Liebespaar im Mond", 
        "colong": 117.6, 
        "duration_min": 150,
        "desc": "Promontorium Agarum im Mare Crisium. Beim abnehmenden Mond erzeugen Schatten zwei Gesichter.",
        "phase": "Abnehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Schattenspiel am Rand des Mare Crisium.",
        "lat": 14.0, "lon": 66.0
    },
    {
        "name": "O'Neills Brücke", 
        "colong": 124.0, 
        "duration_min": 120, 
        "desc": "Zwischen Kap Promontorium Olivium und Lavinium. Ein Schattenspiel täuschte früher Astronomen eine künstliche Brücke vor.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Eine Illusion, die oft schwer nachzuvollziehen ist. Historisch interessant.",
        "lat": 15.0, "lon": 58.0
    },
    {
        "name": "Proclus Asymmetrie", 
        "colong": 133.0, 
        "duration_min": 180,
        "desc": "Der junge Krater Proclus zeigt sein asymmetrisches Strahlensystem beim Sonnenuntergang besonders deutlich.",
        "phase": "Abnehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Sehr helles Strahlensystem, auffällige 'Sperrzone' im Muster.",
        "lat": 16.1, "lon": 46.8
    },
    {
        "name": "Atlas-Kratergruben", 
        "colong": 142.0, 
        "duration_min": 150,
        "desc": "Die mysteriösen dunklen Flecken im Kraterboden von Atlas werden bei schrägem Licht als Vertiefungen erkennbar.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Details im Kraterboden brauchen hohe Vergrößerung.",
        "lat": 46.7, "lon": 44.4
    },
    {
        "name": "Posidonius-Rillen-System", 
        "colong": 148.0, 
        "duration_min": 240,
        "desc": "Das komplexe System von Rimae Posidonius im Kraterboden zeigt sich bei Sonnenuntergang am besten.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Feines Rillensystem, braucht ruhige Luft.",
        "lat": 31.8, "lon": 29.9
    },
    {
        "name": "Linné-Rätsel", 
        "colong": 165.0, 
        "duration_min": 120,
        "desc": "Der kleine, helle Krater Linné im Mare Serenitatis zeigt bei diesem Lichtstand seine wahre Tiefe.",
        "phase": "Abnehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Als heller Fleck sehr leicht (Leicht), als Krater schwer aufzulösen (Schwer).",
        "lat": 27.7, "lon": 11.8
    },
    {
        "name": "Arago-Lichtfleck", 
        "colong": 176.0, 
        "duration_min": 60, 
        "desc": "Die Arago-Alpha- und Beta-Dome werfen beim Sonnenuntergang markante Schatten und zeigen einen kurzen Lichtblitz auf ihren Gipfeln.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Nur kurz sichtbar, Dome sind generell flache, schwierige Objekte.",
        "lat": 6.2, "lon": 21.4
    },
    {
        "name": "Triesnecker-Rillensystem", 
        "colong": 178.0, 
        "duration_min": 240,
        "desc": "Das verzweigte Rillensystem Rimae Triesnecker wird bei niedrigem Sonnenuntergang spektakulär sichtbar.",
        "phase": "Abnehmend",
        "difficulty": "Sehr Schwer",
        "difficulty_tip": "Visuell extrem schwierig, fotografisch einfacher.",
        "lat": 4.2, "lon": 3.6
    },
    {
        "name": "Gruithuisens Mondstadt", 
        "colong": 185.0, 
        "duration_min": 240, 
        "desc": "Fischgrätenartige Bergrücken nördlich von Schröter, die geometrisch wie eine Ruinenstadt wirken (beste Sicht bei Sonnenuntergang).",
        "phase": "Abnehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Die 'Fischgräten'-Struktur ist bei tiefem Sonnenstand gut plastisch zu sehen.",
        "lat": 36.0, "lon": -40.0
    },
    {
        "name": "Curtiss-Kreuz", 
        "colong": 193.5, 
        "duration_min": 120,
        "desc": "Die Wälle des kleinen Kraters Fra Mauro Zeta bilden beim abnehmenden Mond ein leuchtendes Kreuz.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Sehr klein, man muss genau wissen, wo man sucht.",
        "lat": -3.7, "lon": -17.0
    },
    {
        "name": "Pitatus Sunset Ray", 
        "colong": 194.0, 
        "duration_min": 60, 
        "desc": "Gegenstück zum Hesiodus-Strahl: Ein letzter Lichtstrahl beim Sonnenuntergang in Pitatus.",
        "phase": "Abnehmend",
        "difficulty": "Sehr Schwer",
        "difficulty_tip": "Gegenstück zum Hesiodus-Strahl. Sehr kurzes Fenster vor Sonnenuntergang.",
        "lat": -29.8, "lon": -13.5
    },
    {
        "name": "Gassendi-Rillenlabyrinth", 
        "colong": 200.0, 
        "duration_min": 240,
        "desc": "Das komplexe Rillensystem im Kraterboden von Gassendi zeigt sich bei Sonnenuntergang am eindrucksvollsten.",
        "phase": "Abnehmend",
        "difficulty": "Schwer",
        "difficulty_tip": "Gassendi ist groß ('Diamantring'), aber die Brüche im Boden sind fein.",
        "lat": -17.5, "lon": -40.1
    },
    {
        "name": "Tycho-Sonnenuntergang", 
        "colong": 207.0, 
        "duration_min": 240,
        "desc": "Der Zentralberg von Tycho fängt das letzte Licht und glüht wie eine Fackel im dunklen Kraterboden.",
        "phase": "Abnehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Wie beim Aufgang: Der Zentralberg glüht lange nach.",
        "lat": -43.3, "lon": -11.2
    },
    {
        "name": "Wargentin-Plateau", 
        "colong": 212.0, 
        "duration_min": 180,
        "desc": "Der einzigartige, bis zum Rand mit Lava gefüllte Krater Wargentin zeigt seine ebene Oberfläche im Kontrast zur Umgebung.",
        "phase": "Abnehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Auffällig, da es wie ein 'voller Teller' aussieht (inverser Krater).",
        "lat": -49.6, "lon": -60.2
    },
    {
        "name": "Inverser Goldener Henkel", 
        "colong": 217.0, # KORRIGIERT: War 319.5 (Falsch). Sunset = Sunrise (35) + 180 = ~215-218.
        "duration_min": 420, 
        "desc": "Sonnenuntergang am Jura-Gebirge. Die Spitzen leuchten als letzte Strukturen über der Regenbogebucht in die Nacht hinein.",
        "phase": "Abnehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Sehr ästhetisch, wenn das Jura-Gebirge noch im Licht schwebt.",
        "lat": 47.0, "lon": -34.0
    },
    {
        "name": "Mondjungfrau Abschied", 
        "colong": 218.0, # KORRIGIERT: War 319.5 (Falsch). Folgt dem Goldenen Henkel beim Untergang.
        "duration_min": 300,
        "desc": "Kap Heraclides beim Sonnenuntergang - das Profil der Mondjungfrau versinkt im Schatten.",
        "phase": "Abnehmend",
        "difficulty": "Mittel",
        "difficulty_tip": "Ähnlich wie am Morgen, Profil verschwindet langsam.",
        "lat": 40.7, "lon": -33.2
    },
    {
        "name": "Eratosthenes letzter Schatten", 
        "colong": 191.8, # KORRIGIERT: War 329.0 (Falsch). Sunrise (11.8) + 180 = 191.8.
        "duration_min": 180,
        "desc": "Der Krater Eratosthenes wirft beim Sonnenuntergang einen langen Schatten über das Mare Imbrium.",
        "phase": "Abnehmend",
        "difficulty": "Leicht",
        "difficulty_tip": "Sehr langes Zeitfenster, Schattenwurf ist dramatisch.",
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