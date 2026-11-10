import ephem
import math


class EphemCalculator:
    def __init__(self, location_data):
        self.observer = ephem.Observer()
        self.observer.lat = str(location_data['lat'])
        self.observer.lon = str(location_data['lon'])
        elev = float(location_data.get('elevation', 0.0))
        self.observer.elevation = elev
        # Barometrische Höhenformel für realistische atmosphärische Refraktion
        if 0.0 <= elev < 11000.0:
            self.observer.pressure = 1010.0 * ((1.0 - 0.0065 * elev / 288.15) ** 5.255)
        self.moon = ephem.Moon()
        self.sun = ephem.Sun()

    def get_observability(self, date_utc, min_moon_alt=5.0, max_sun_alt=-6.0):
        """
        Prüft die Standortsichtbarkeit (Mondhöhe, Sonnenhöhe/Dämmerung).
        Return: (is_visible, reason, moon_alt_deg, sun_alt_deg)
        """
        self.observer.date = date_utc

        self.moon.compute(self.observer)
        self.sun.compute(self.observer)

        moon_alt_deg = math.degrees(self.moon.alt)
        sun_alt_deg = math.degrees(self.sun.alt)

        reasons = []
        is_good = True

        # Kriterium 1: Mond mindestens 5° über dem Horizont
        if moon_alt_deg < min_moon_alt:
            is_good = False
            if moon_alt_deg < 0:
                reasons.append("Mond unter Horizont")
            else:
                reasons.append(f"Mond zu tief (<{min_moon_alt:g}°)")

        # Kriterium 2: Bürgerliche Dämmerung beendet (Sonne <= -6°)
        if sun_alt_deg > max_sun_alt:
            is_good = False
            if sun_alt_deg > 0:
                reasons.append("Taghimmel (Sonne > 0°)")
            else:
                reasons.append(f"Dämmerung (Sonne > {max_sun_alt:g}°)")

        status_text = "Gut beobachtbar" if is_good else ", ".join(reasons)
        return is_good, status_text, moon_alt_deg, sun_alt_deg

    def get_libration_and_lighting(self, date_utc, event_lat=0.0, event_lon=0.0):
        """
        Berechnet Libration (in Breite und Länge), subsolare Breite b0,
        lokale Sonnenhöhe über dem Mondkrater sowie den Sichtwinkel (Randabstand).
        """
        self.observer.date = date_utc
        self.moon.compute(self.observer)

        colong_deg = math.degrees(self.moon.colong)
        subsolar_lat_deg = math.degrees(self.moon.subsolar_lat)
        lib_lat_deg = math.degrees(self.moon.libration_lat)
        lib_lon_deg = math.degrees(self.moon.libration_long)

        phi = math.radians(event_lat)
        lam = math.radians(event_lon)
        b0 = math.radians(subsolar_lat_deg)
        c0 = math.radians(colong_deg)
        b_lib = math.radians(lib_lat_deg)
        l_lib = math.radians(lib_lon_deg)

        # 2D-Sonnenhöhe h_sun am Krater (phi, lam)
        sin_h_sun = (
            math.sin(phi) * math.sin(b0)
            + math.cos(phi) * math.cos(b0) * math.sin(c0 + lam)
        )
        sin_h_sun = max(-1.0, min(1.0, sin_h_sun))
        solar_alt_deg = math.degrees(math.asin(sin_h_sun))

        # Winkelabstand theta von der scheinbaren Mondscheibenmitte unter Berücksichtigung der Libration
        cos_theta = (
            math.sin(phi) * math.sin(b_lib)
            + math.cos(phi) * math.cos(b_lib) * math.cos(lam - l_lib)
        )
        cos_theta = max(-1.0, min(1.0, cos_theta))
        center_dist_deg = math.degrees(math.acos(cos_theta))

        # Vergleich mit Null-Libration (b=0, l=0)
        cos_theta_0 = max(-1.0, min(1.0, math.cos(phi) * math.cos(lam)))
        center_dist_0_deg = math.degrees(math.acos(cos_theta_0))
        lib_gain_deg = center_dist_0_deg - center_dist_deg  # positiv = näher zur Mitte gedreht

        if center_dist_deg >= 89.0:
            lib_status = "Hinter Mondrand (unsichtbar)"
        elif center_dist_deg >= 82.0:
            lib_status = f"Extrem randnah ({lib_gain_deg:+.1f}° Libration)"
        elif center_dist_0_deg >= 45.0:
            if lib_gain_deg >= 1.5:
                lib_status = f"Günstig (+{lib_gain_deg:.1f}° vom Rand)"
            elif lib_gain_deg <= -1.5:
                lib_status = f"Ungünstig ({lib_gain_deg:.1f}° zum Rand)"
            else:
                lib_status = "Neutral"
        else:
            lib_status = "Unkritisch (Zentralbereich)"

        return {
            "colong": colong_deg,
            "subsolar_lat": subsolar_lat_deg,
            "lib_lat": lib_lat_deg,
            "lib_lon": lib_lon_deg,
            "solar_alt": solar_alt_deg,
            "center_dist_deg": center_dist_deg,
            "foreshortening": max(0.0, cos_theta),
            "lib_gain_deg": lib_gain_deg,
            "lib_status": lib_status,
        }
