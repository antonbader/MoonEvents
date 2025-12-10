# mond_berechnung.py
import ephem
import math
from datetime import datetime, timedelta

def get_colongitude_deg(date_obj):
    m = ephem.Moon()
    observer = ephem.Observer()
    observer.date = date_obj
    m.compute(observer)
    return math.degrees(m.colong)

def get_observability(date_utc, location_data):
    """
    Prüft Sichtbarkeit.
    Return: (is_visible, reason, moon_alt, sun_alt)
    """
    observer = ephem.Observer()
    observer.lat = str(location_data['lat'])
    observer.lon = str(location_data['lon'])
    observer.elevation = location_data['elevation']
    observer.date = date_utc
    
    moon = ephem.Moon()
    sun = ephem.Sun()
    moon.compute(observer)
    sun.compute(observer)
    
    moon_alt_deg = math.degrees(moon.alt)
    sun_alt_deg = math.degrees(sun.alt)
    
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

def find_next_event_peak(start_date, target_colong):
    """Findet den nächsten Colongitude-Peak (Theoretisches Optimum)."""
    current_date = ephem.Date(start_date)
    current_col = get_colongitude_deg(current_date)
    diff = target_colong - current_col
    if diff < 0: diff += 360
    
    days_to_add = diff / 12.2
    search_date = ephem.Date(current_date + days_to_add)
    
    for _ in range(5):
        val = get_colongitude_deg(search_date)
        delta = target_colong - val
        if delta > 180: delta -= 360
        if delta < -180: delta += 360
        if abs(delta) < 0.001: break
        search_date = ephem.Date(search_date + (delta / 12.19))
    
    if search_date < current_date:
        search_date = ephem.Date(search_date + 29.53059)
        for _ in range(3):
            val = get_colongitude_deg(search_date)
            delta = target_colong - val
            if delta > 180: delta -= 360
            if delta < -180: delta += 360
            search_date = ephem.Date(search_date + (delta / 12.19))

    return search_date.datetime()

def find_best_visible_moment(start_utc, end_utc, location_data):
    """
    Scannt den Zeitraum [start_utc, end_utc] nach dem besten Beobachtungsmoment.
    Bestimmt den Zeitpunkt mit der höchsten Mondhöhe innerhalb der Sichtbarkeit.
    Return: (best_time, max_alt) oder (None, None)
    """
    best_time = None
    max_alt = -90.0
    
    # Wir scannen in 5-Minuten-Schritten
    curr = start_utc
    while curr <= end_utc:
        is_vis, _, m_alt, _ = get_observability(curr, location_data)
        
        if is_vis:
            if m_alt > max_alt:
                max_alt = m_alt
                best_time = curr
        
        curr += timedelta(minutes=5)
        
    return best_time, max_alt

def calculate_all_events(start_datetime_utc, end_datetime_utc, selected_events, location_data):
    results = []
    offset = location_data.get("timezone_offset", 1)
    
    for ev in selected_events:
        current_search_start = start_datetime_utc
        
        while True:
            # 1. Theoretischen Peak finden
            theo_peak_utc = find_next_event_peak(current_search_start, ev['colong'])
            
            if theo_peak_utc > end_datetime_utc:
                break
                
            # 2. Zeitfenster bestimmen
            duration_min = ev.get('duration_min', 120)
            half_duration = timedelta(minutes=duration_min / 2)
            start_utc = theo_peak_utc - half_duration
            end_utc = theo_peak_utc + half_duration
            
            # 3. Sichtbarkeits-Check
            vis_peak_theo, reason_peak, m_alt_peak, _ = get_observability(theo_peak_utc, location_data)
            
            # Initiale Werte
            final_peak_utc = theo_peak_utc
            final_status = reason_peak
            final_alt = m_alt_peak
            is_optimized = False
            
            # 4. Optimum anpassen (Nur wenn theoretischer Peak NICHT sichtbar ist)
            if not vis_peak_theo:
                best_alt_time, best_alt_val = find_best_visible_moment(start_utc, end_utc, location_data)
                
                if best_alt_time:
                    final_peak_utc = best_alt_time
                    final_alt = best_alt_val
                    final_status = "Optimum angepasst (Sichtbarkeit)"
                    is_optimized = True
            
            # 5. Einzelprüfungen
            vis_start, _, _, _ = get_observability(start_utc, location_data)
            vis_end, _, _, _ = get_observability(end_utc, location_data)
            vis_peak_final, _, _, _ = get_observability(final_peak_utc, location_data)
            
            # Status Text
            if is_optimized:
                theo_local = theo_peak_utc + timedelta(hours=offset)
                theo_str = theo_local.strftime('%H:%M')
                final_status = f"Verschoben (Theo: {theo_str}, Alt: {final_alt:.1f}°)"
            elif not vis_peak_final:
                final_status = reason_peak

            # Lokalzeiten
            peak_local = final_peak_utc + timedelta(hours=offset)
            start_local = start_utc + timedelta(hours=offset)
            end_local = end_utc + timedelta(hours=offset)
            
            any_visible = vis_start or vis_peak_final or vis_end

            results.append({
                "event": ev,
                "peak_utc": final_peak_utc,
                "peak_local": peak_local,
                "start_local": start_local,
                "end_local": end_local,
                "location": location_data['name'],
                "vis_start": vis_start,
                "vis_peak": vis_peak_final,
                "vis_end": vis_end,
                "visible": any_visible,
                "status_text": final_status,
                "moon_alt": final_alt
            })
            
            current_search_start = theo_peak_utc + timedelta(days=2)
            
    results.sort(key=lambda x: x['peak_local'])
    return results