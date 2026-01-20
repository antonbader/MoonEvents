
import ephem
import math

class EphemCalculator:
    def __init__(self, location_data):
        self.observer = ephem.Observer()
        self.observer.lat = str(location_data['lat'])
        self.observer.lon = str(location_data['lon'])
        self.observer.elevation = location_data['elevation']
        self.moon = ephem.Moon()
        self.sun = ephem.Sun()

    def get_observability(self, date_utc):
        """
        Prüft Sichtbarkeit.
        Return: (is_visible, reason, moon_alt, sun_alt)
        """
        self.observer.date = date_utc

        self.moon.compute(self.observer)
        self.sun.compute(self.observer)

        moon_alt_deg = math.degrees(self.moon.alt)
        sun_alt_deg = math.degrees(self.sun.alt)

        reasons = []
        is_good = True

        # Kriterien: Mond > 5° und Sonne < 0° (Exakt Sonnenuntergang)
        if moon_alt_deg < 5:
            is_good = False
            if moon_alt_deg < 0: reasons.append("Mond unter Horizont")
            else: reasons.append("Mond zu tief (<5°)")

        # HIER IST DIE WICHTIGE ÄNDERUNG: 0 statt -0.5 oder -6
        if sun_alt_deg > 0:
            is_good = False
            reasons.append("Taghimmel (Sonne > 0°)")

        status_text = "Gut beobachtbar" if is_good else ", ".join(reasons)
        return is_good, status_text, moon_alt_deg, sun_alt_deg
