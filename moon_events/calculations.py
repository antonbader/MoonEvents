# mond_berechnung.py
import ephem
import math
from datetime import datetime, timedelta, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

from moon_events.calculation_logic import EphemCalculator


def get_colongitude_and_subsolar_lat(date_obj):
    m = ephem.Moon()
    m.compute(date_obj)
    return math.degrees(m.colong), math.degrees(m.subsolar_lat)


def get_colongitude_deg(date_obj):
    colong, _ = get_colongitude_and_subsolar_lat(date_obj)
    return colong


def get_effective_target_colong(target_colong_ref, event_lat, event_lon, subsolar_lat_deg):
    """
    Berechnet die um die subsolare Breite b0 korrigierte Ziel-Colongitude C0*(b0),
    sodass am Krater (event_lat, event_lon) exakt dieselbe lokale Sonnenhöhe h_sun
    erreicht wird wie beim Referenzwert target_colong_ref für b0 = 0°.
    """
    phi = math.radians(event_lat)
    alpha_ref = math.radians(target_colong_ref + event_lon)
    b0 = math.radians(subsolar_lat_deg)

    cos_b0 = math.cos(b0)
    if abs(cos_b0) < 1e-9:
        return target_colong_ref % 360.0

    # Bedingung: sin(phi)*sin(b0) + cos(phi)*cos(b0)*sin(alpha*) = cos(phi)*sin(alpha_ref)
    rhs = (math.sin(alpha_ref) - math.tan(phi) * math.sin(b0)) / cos_b0
    rhs = max(-1.0, min(1.0, rhs))
    asin_deg = math.degrees(math.asin(rhs))

    # Gleicher Quadrant (Sonnenaufgang vs. Sonnenuntergang) wie alpha_ref
    if math.cos(alpha_ref) >= 0.0:
        alpha_star_deg = asin_deg
    else:
        alpha_star_deg = 180.0 - asin_deg

    return (alpha_star_deg - event_lon) % 360.0


def find_next_event_peak(start_date, target_colong, event_lat=0.0, event_lon=0.0):
    """
    Findet den nächsten Beleuchtungs-Peak (Theoretisches Optimum) unter
    Berücksichtigung der 2D-Sonnenhöhe (inkl. subsolarer Breite b0).
    """
    current_date = ephem.Date(start_date)
    current_col, current_b0 = get_colongitude_and_subsolar_lat(current_date)
    eff_target = get_effective_target_colong(target_colong, event_lat, event_lon, current_b0)

    diff = (eff_target - current_col) % 360.0
    days_to_add = diff / 12.19075
    search_date = ephem.Date(current_date + days_to_add)

    for _ in range(6):
        val, b0_val = get_colongitude_and_subsolar_lat(search_date)
        eff_target = get_effective_target_colong(target_colong, event_lat, event_lon, b0_val)
        delta = eff_target - val
        if delta > 180.0:
            delta -= 360.0
        elif delta < -180.0:
            delta += 360.0
        if abs(delta) < 0.0005:
            break
        search_date = ephem.Date(search_date + (delta / 12.19075))

    # Nur dann auf den nächsten Monat springen, wenn der gefundene Peak echt vor current_date liegt
    # (Toleranz 1e-4 Tage ~ 8.6 Sekunden verhindert Fehlsprünge bei Start direkt am Peak)
    if search_date < current_date - 1e-4:
        search_date = ephem.Date(search_date + 29.530589)
        for _ in range(5):
            val, b0_val = get_colongitude_and_subsolar_lat(search_date)
            eff_target = get_effective_target_colong(target_colong, event_lat, event_lon, b0_val)
            delta = eff_target - val
            if delta > 180.0:
                delta -= 360.0
            elif delta < -180.0:
                delta += 360.0
            if abs(delta) < 0.0005:
                break
            search_date = ephem.Date(search_date + (delta / 12.19075))
    elif search_date < current_date:
        search_date = current_date

    return search_date.datetime()


def _is_eu_dst_utc(dt_utc: datetime) -> bool:
    """Fallback-Prüfung für europäische Sommerzeit (MESZ): Letzter Sonntag im März 01:00 UTC bis letzter Sonntag im Oktober 01:00 UTC."""
    year = dt_utc.year
    # Letzter Sonntag im März
    march_31 = datetime(year, 3, 31)
    dst_start = datetime(year, 3, 31 - ((march_31.weekday() + 1) % 7), 1, 0, 0)
    # Letzter Sonntag im Oktober
    oct_31 = datetime(year, 10, 31)
    dst_end = datetime(year, 10, 31 - ((oct_31.weekday() + 1) % 7), 1, 0, 0)
    return dst_start <= dt_utc < dst_end


def utc_to_local(dt_utc: datetime, location_data: dict) -> datetime:
    """Konvertiert naive UTC-datetime in lokale Ortszeit (inkl. automatischer Sommerzeit, falls aktiviert)."""
    auto_dst = location_data.get("auto_dst", True)
    offset = location_data.get("timezone_offset", 1)
    tz_name = location_data.get("timezone", "Europe/Berlin" if offset == 1 else None)

    if auto_dst and tz_name and ZoneInfo is not None:
        try:
            tz = ZoneInfo(tz_name)
            aware_utc = dt_utc.replace(tzinfo=timezone.utc)
            return aware_utc.astimezone(tz).replace(tzinfo=None)
        except Exception:
            pass

    if auto_dst and offset == 1:
        eff_offset = 2 if _is_eu_dst_utc(dt_utc) else 1
        return dt_utc + timedelta(hours=eff_offset)

    return dt_utc + timedelta(hours=offset)


def local_to_utc(dt_local: datetime, location_data: dict) -> datetime:
    """Konvertiert naive lokale Ortszeit in naive UTC-datetime."""
    auto_dst = location_data.get("auto_dst", True)
    offset = location_data.get("timezone_offset", 1)
    tz_name = location_data.get("timezone", "Europe/Berlin" if offset == 1 else None)

    if auto_dst and tz_name and ZoneInfo is not None:
        try:
            tz = ZoneInfo(tz_name)
            aware_local = dt_local.replace(tzinfo=tz)
            return aware_local.astimezone(timezone.utc).replace(tzinfo=None)
        except Exception:
            pass

    if auto_dst and offset == 1:
        approx_utc = dt_local - timedelta(hours=1)
        eff_offset = 2 if _is_eu_dst_utc(approx_utc) else 1
        return dt_local - timedelta(hours=eff_offset)

    return dt_local - timedelta(hours=offset)


def get_timezone_label(location_data: dict) -> str:
    offset = location_data.get("timezone_offset", 1)
    auto_dst = location_data.get("auto_dst", True)
    tz_name = location_data.get("timezone")
    if auto_dst and offset == 1 and (not tz_name or tz_name == "Europe/Berlin"):
        return "MEZ/MESZ (automatisch)"
    if auto_dst and tz_name:
        return f"{tz_name} (automatisch)"
    if offset >= 0:
        return f"UTC+{offset}"
    return f"UTC{offset}"


def find_best_visible_moment(start_utc, end_utc, calculator: EphemCalculator, theo_peak_utc=None):
    """
    Scannt den Zeitraum [start_utc, end_utc] nach dem besten Beobachtungsmoment.
    Berücksichtigt Mondhöhe, Dunkelheit des Himmels und zeitliche Nähe zum theoretischen Peak.
    Return: (best_time, best_moon_alt) oder (None, None)
    """
    best_time = None
    best_alt = -90.0
    best_score = -1e9

    if theo_peak_utc is None:
        theo_peak_utc = start_utc + (end_utc - start_utc) / 2
    half_span_sec = max(1.0, (end_utc - start_utc).total_seconds() / 2.0)

    curr = start_utc
    step = timedelta(minutes=2)
    while curr <= end_utc:
        is_vis, _, m_alt, s_alt = calculator.get_observability(curr)

        if is_vis:
            # Nähe zum theoretischen Peak (0 am Rand, 1 am Peak)
            dist_ratio = abs((curr - theo_peak_utc).total_seconds()) / half_span_sec
            proximity_bonus = max(0.0, 1.0 - dist_ratio) * 15.0
            # Dunkelheitsbonus zwischen bürgerlicher (-6°) und astronomischer Dämmerung (-18°)
            darkness_bonus = min(12.0, max(0.0, (-6.0 - s_alt)))
            score = m_alt + proximity_bonus + darkness_bonus

            if score > best_score:
                best_score = score
                best_alt = m_alt
                best_time = curr

        curr += step

    return best_time, best_alt


def calculate_all_events(start_datetime_utc, end_datetime_utc, selected_events, location_data, calculator: EphemCalculator):
    results = []

    for ev in selected_events:
        duration_min = ev.get('duration_min', 120)
        half_duration = timedelta(minutes=duration_min / 2.0)
        ev_lat = ev.get('lat', 0.0)
        ev_lon = ev.get('lon', 0.0)

        # Suche um half_duration vorverlegen, damit bereits laufende Ereignisse zu Beginn nicht verloren gehen
        current_search_start = start_datetime_utc - half_duration

        while True:
            # 1. Theoretischen Peak finden (inkl. 2D b0-Korrektur)
            theo_peak_utc = find_next_event_peak(
                current_search_start, ev['colong'], ev_lat, ev_lon
            )

            start_utc = theo_peak_utc - half_duration
            end_utc = theo_peak_utc + half_duration

            # Abbruch erst, wenn der Beginn des Ereignisfensters nach dem Ende des Suchzeitraums liegt
            if start_utc > end_datetime_utc:
                break

            # Falls das Ende des Ereignisses noch vor dem Suchbeginn liegt, weiter zum nächsten Monat
            if end_utc < start_datetime_utc:
                current_search_start = theo_peak_utc + timedelta(days=2)
                continue

            # 2. Sichtbarkeits-Check am theoretischen Peak
            vis_peak_theo, reason_peak, m_alt_peak, _ = calculator.get_observability(theo_peak_utc)

            final_peak_utc = theo_peak_utc
            final_status = reason_peak
            final_alt = m_alt_peak
            is_optimized = False

            # 3. Optimum im Ereignisfenster suchen (wenn theor. Peak unsichtbar ist oder Mond dort sehr tief steht)
            if not vis_peak_theo or m_alt_peak < 15.0:
                best_alt_time, best_alt_val = find_best_visible_moment(
                    start_utc, end_utc, calculator, theo_peak_utc=theo_peak_utc
                )

                if best_alt_time is not None:
                    if not vis_peak_theo:
                        final_peak_utc = best_alt_time
                        final_alt = best_alt_val
                        is_optimized = True
                    elif (best_alt_val - m_alt_peak) >= 8.0 and abs((best_alt_time - theo_peak_utc).total_seconds()) >= 300:
                        final_peak_utc = best_alt_time
                        final_alt = best_alt_val

            # 4. Einzelprüfungen & Libration (sowohl für Beobachtungs-Optimum als auch für theoretischen Peak)
            vis_start, _, _, _ = calculator.get_observability(start_utc)
            vis_end, _, _, _ = calculator.get_observability(end_utc)
            vis_peak_final, _, _, _ = calculator.get_observability(final_peak_utc)

            lib_info = calculator.get_libration_and_lighting(final_peak_utc, ev_lat, ev_lon)
            theo_lib_info = calculator.get_libration_and_lighting(theo_peak_utc, ev_lat, ev_lon)
            limb_ok = lib_info["center_dist_deg"] < 89.0

            if not limb_ok:
                vis_start = False
                vis_peak_final = False
                vis_end = False
                final_status = "Hinter Mondrand (Libration)"
            elif is_optimized:
                final_status = f"Randfenster sichtbar (Peak: {reason_peak})"
            elif not vis_peak_final:
                final_status = reason_peak

            any_visible = (vis_start or vis_peak_final or vis_end) and limb_ok

            # 5. Lokalzeiten (mit automatischer Sommerzeit MEZ/MESZ)
            peak_local = utc_to_local(final_peak_utc, location_data)
            start_local = utc_to_local(start_utc, location_data)
            end_local = utc_to_local(end_utc, location_data)
            theo_peak_local = utc_to_local(theo_peak_utc, location_data)

            # Exaktes Mondalter (Tage seit letztem Neumond)
            exact_age = calculate_moon_age_exact(final_peak_utc)

            results.append({
                "event": ev,
                "peak_utc": final_peak_utc,
                "peak_local": peak_local,
                "start_local": start_local,
                "end_local": end_local,
                "theo_peak_utc": theo_peak_utc,
                "theo_peak_local": theo_peak_local,
                "vis_peak_theo": vis_peak_theo and limb_ok,
                "location": location_data['name'],
                "vis_start": vis_start,
                "vis_peak": vis_peak_final,
                "vis_end": vis_end,
                "visible": any_visible,
                "status_text": final_status,
                "moon_alt": final_alt,
                "colong_actual": lib_info["colong"],
                "colong_theo": theo_lib_info["colong"],
                "subsolar_lat": lib_info["subsolar_lat"],
                "subsolar_lat_theo": theo_lib_info["subsolar_lat"],
                "solar_alt": lib_info["solar_alt"],
                "solar_alt_theo": theo_lib_info["solar_alt"],
                "lib_lat": lib_info["lib_lat"],
                "lib_lon": lib_info["lib_lon"],
                "center_dist_deg": lib_info["center_dist_deg"],
                "lib_status": lib_info["lib_status"],
                "moon_age_exact": exact_age,
            })

            current_search_start = theo_peak_utc + timedelta(days=2)

    results.sort(key=lambda x: x['peak_utc'])
    return results


def calculate_moon_age_exact(date_utc) -> float:
    """Berechnet das wahre synodische Mondalter in Tagen seit dem letzten Neumond."""
    d = ephem.Date(date_utc)
    prev_nm = ephem.previous_new_moon(d)
    return float(d - prev_nm)


def calculate_moon_age_approx(colongitude):
    """
    Berechnet das mittlere Mondalter (in Tagen seit Neumond) basierend auf der Colongitude.
    Formel: ((colong - 270) % 360) / 12.19075
    """
    return ((colongitude - 270.0) % 360.0) / 12.19075


def get_phase_description(age):
    """
    Gibt eine Textbeschreibung der Mondphase basierend auf dem Mondalter (Tage) zurück.
    """
    age = age % 29.53059

    if age < 1.0 or age > 28.5:
        return "Neumond"
    elif age < 6.4:
        return "Zunehmende Sichel"
    elif age < 8.4:
        return "Erstes Viertel"
    elif age < 13.8:
        return "Zunehmender Mond"
    elif age <= 15.8:
        return "Vollmond"
    elif age < 21.1:
        return "Abnehmender Mond"
    elif age < 23.1:
        return "Letztes Viertel"
    else:
        return "Abnehmende Sichel"
