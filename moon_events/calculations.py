# mond_berechnung.py
import ephem
import math
from datetime import datetime, timedelta
from moon_events.calculation_logic import EphemCalculator

def get_colongitude_deg(date_obj):
    m = ephem.Moon()
    observer = ephem.Observer()
    observer.date = date_obj
    m.compute(observer)
    return math.degrees(m.colong)

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

def find_best_visible_moment(start_utc, end_utc, calculator: EphemCalculator):
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
        is_vis, _, m_alt, _ = calculator.get_observability(curr)
        
        if is_vis:
            if m_alt > max_alt:
                max_alt = m_alt
                best_time = curr
        
        curr += timedelta(minutes=5)
        
    return best_time, max_alt

def calculate_all_events(start_datetime_utc, end_datetime_utc, selected_events, location_data, calculator: EphemCalculator):
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
            vis_peak_theo, reason_peak, m_alt_peak, _ = calculator.get_observability(theo_peak_utc)
            
            # Initiale Werte
            final_peak_utc = theo_peak_utc
            final_status = reason_peak
            final_alt = m_alt_peak
            is_optimized = False
            
            # 4. Optimum anpassen (Nur wenn theoretischer Peak NICHT sichtbar ist)
            if not vis_peak_theo:
                best_alt_time, best_alt_val = find_best_visible_moment(start_utc, end_utc, calculator)
                
                if best_alt_time:
                    final_peak_utc = best_alt_time
                    final_alt = best_alt_val
                    final_status = "Optimum angepasst (Sichtbarkeit)"
                    is_optimized = True
            
            # 5. Einzelprüfungen
            vis_start, _, _, _ = calculator.get_observability(start_utc)
            vis_end, _, _, _ = calculator.get_observability(end_utc)
            vis_peak_final, _, _, _ = calculator.get_observability(final_peak_utc)
            
            # Lokalzeiten
            peak_local = final_peak_utc + timedelta(hours=offset)
            start_local = start_utc + timedelta(hours=offset)
            end_local = end_utc + timedelta(hours=offset)
            theo_peak_local = theo_peak_utc + timedelta(hours=offset)

            # Status Text
            if is_optimized:
                final_status = f"Verschoben ({reason_peak})"
            elif not vis_peak_final:
                final_status = reason_peak

            any_visible = vis_start or vis_peak_final or vis_end

            results.append({
                "event": ev,
                "peak_utc": final_peak_utc,
                "peak_local": peak_local,
                "start_local": start_local,
                "end_local": end_local,
                "theo_peak_utc": theo_peak_utc,
                "theo_peak_local": theo_peak_local,
                "vis_peak_theo": vis_peak_theo,
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

def calculate_moon_age_approx(colongitude):
    """
    Berechnet das ungefähre Mondalter (in Tagen seit Neumond) basierend auf der Colongitude.
    Formel: ((colong - 270) % 360) / 12.2
    """
    return ((colongitude - 270) % 360) / 12.2

def get_phase_description(age):
    """
    Gibt eine Textbeschreibung der Mondphase basierend auf dem Mondalter (Tage) zurück.
    """
    # Normalisierung falls age < 0 oder > 29.53 (sollte bei approx formel nicht passieren, aber sicher ist sicher)
    age = age % 29.53059

    if age < 1.0 or age > 28.5:
        return "Neumond"
    elif age < 13.5:
        return "Zunehmender Mond"
    elif age <= 16.0:
        return "Vollmond"
    else:
        return "Abnehmender Mond"
