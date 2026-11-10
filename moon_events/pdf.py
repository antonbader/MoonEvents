# moon_events/pdf.py
from datetime import datetime
from fpdf import FPDF


def _sanitize_latin1(text: str) -> str:
    """
    Bereinigt Unicode-Sonderzeichen und ersetzt typografische Zeichen
    durch Latin-1-kompatible Äquivalente für FPDF.
    """
    if not text:
        return ""
    replacements = {
        "α": "alpha",
        "β": "beta",
        "γ": "gamma",
        "δ": "delta",
        "–": "-",
        "—": "-",
        "„": '"',
        "“": '"',
        "”": '"',
        "’": "'",
        "‘": "'",
        "‚": "'",
        "…": "...",
        "•": "*",
        "′": "'",
        "″": '"',
        "≈": "~",
        "±": "+/-",
        "≤": "<=",
        "≥": ">=",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')


def get_text_lines(pdf, text: str, width: float, family='Arial', style='', size=7.5):
    """
    Berechnet die exakte Zeilenaufteilung unter Berücksichtigung von Leerzeichen,
    Bindestrichen und Schrägstrichen, sodass kein Text über die Spaltenbreite hinausgeht.
    """
    pdf.set_font(family, style, size)
    avail_w = max(5.0, width - 2 * pdf.c_margin)
    paragraphs = text.replace('\r', '').split('\n')
    all_lines = []

    for para in paragraphs:
        if not para:
            all_lines.append('')
            continue
        words = para.split(' ')
        curr = ''
        for w in words:
            test = (curr + ' ' + w).strip()
            if pdf.get_string_width(test) <= avail_w:
                curr = test
            else:
                # Prüfen ob ein Trennzeichen (- oder /) eine saubere Trennung erlaubt
                if '-' in w and len(w) > 3:
                    parts = w.split('-')
                    temp_curr = curr
                    for idx, part in enumerate(parts):
                        chunk = (part + '-') if idx < len(parts) - 1 else part
                        test_chunk = (temp_curr + ' ' + chunk).strip() if temp_curr else chunk
                        if pdf.get_string_width(test_chunk) <= avail_w:
                            temp_curr = test_chunk
                        else:
                            if temp_curr:
                                all_lines.append(temp_curr)
                            temp_curr = chunk
                    curr = temp_curr
                elif '/' in w and len(w) > 3:
                    parts = w.split('/')
                    temp_curr = curr
                    for idx, part in enumerate(parts):
                        chunk = (part + '/') if idx < len(parts) - 1 else part
                        test_chunk = (temp_curr + ' ' + chunk).strip() if temp_curr else chunk
                        if pdf.get_string_width(test_chunk) <= avail_w:
                            temp_curr = test_chunk
                        else:
                            if temp_curr:
                                all_lines.append(temp_curr)
                            temp_curr = chunk
                    curr = temp_curr
                else:
                    if curr:
                        all_lines.append(curr)
                    curr = w
        if curr:
            all_lines.append(curr)

    # Letzter Sicherheits-Check gegen extrem lange Einzelwörter ohne Trennzeichen
    final_lines = []
    for l in all_lines:
        if pdf.get_string_width(l) > avail_w:
            sub = pdf.multi_cell(width, 4, l, split_only=True)
            final_lines.extend(sub)
        else:
            final_lines.append(l)
    return final_lines or ['']


class PDFReport(FPDF):
    """
    Modernes, übersichtliches PDF-Layout für lunare Beobachtungspläne.
    """
    def __init__(
        self,
        version,
        calc_date,
        location_name="",
        date_range_str="",
        tz_name="",
        total_events=0,
        visible_events=0,
        orientation='L',
        unit='mm',
        format='A4',
    ):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.version = version
        self.calc_date = calc_date
        self.location_name = _sanitize_latin1(location_name)
        self.date_range_str = _sanitize_latin1(date_range_str)
        self.tz_name = _sanitize_latin1(tz_name)
        self.total_events = total_events
        self.visible_events = visible_events
        self.alias_nb_pages()

    def header(self):
        page_w = self.w - self.l_margin - self.r_margin

        if self.page_no() == 1:
            # Header Title Bereich (Seite 1)
            self.set_y(10)
            self.set_font('Arial', 'B', 15)
            self.set_text_color(15, 23, 42)  # Slate 900
            self.cell(100, 7, "MoonEvents", 0, 0, 'L')

            # Rechter Header-Text: Erstellungsdatum
            self.set_font('Arial', '', 8)
            self.set_text_color(100, 116, 139)  # Slate 500
            self.cell(page_w - 100, 7, f"Erstellt am: {self.calc_date}", 0, 1, 'R')

            # Untertitel
            self.set_font('Arial', '', 8.5)
            self.set_text_color(71, 85, 105)  # Slate 600
            self.cell(page_w, 4.5, "Beobachtungsplan - Lunare Clair-Obscur-Ereignisse & Schattenspiele", 0, 1, 'L')
            self.ln(2.5)

            # Metadata Info Card
            box_y = self.get_y()
            box_h = 15.0

            # Hintergrund der Infobox
            self.set_fill_color(248, 250, 252)  # Slate 50
            self.set_draw_color(203, 213, 225)  # Slate 300
            self.rect(self.l_margin, box_y, page_w, box_h, 'FD')

            # Akzent-Leiste links (Blau)
            self.set_fill_color(37, 99, 235)  # Blue 600
            self.rect(self.l_margin, box_y, 2.5, box_h, 'F')

            # 4 Spalten in der Info-Box
            col_w = (page_w - 6) / 4
            x_offset = self.l_margin + 5

            # Spalte 1: Standort
            self.set_xy(x_offset, box_y + 2.0)
            self.set_font('Arial', 'B', 6.5)
            self.set_text_color(100, 116, 139)
            self.cell(col_w, 3.5, "STANDORT", 0, 1, 'L')
            self.set_xy(x_offset, box_y + 6.5)
            self.set_font('Arial', 'B', 8.5)
            self.set_text_color(15, 23, 42)
            self.cell(col_w, 5, self.location_name, 0, 0, 'L')

            # Spalte 2: Zeitraum
            x_offset += col_w
            self.set_xy(x_offset, box_y + 2.0)
            self.set_font('Arial', 'B', 6.5)
            self.set_text_color(100, 116, 139)
            self.cell(col_w, 3.5, "ZEITRAUM", 0, 1, 'L')
            self.set_xy(x_offset, box_y + 6.5)
            self.set_font('Arial', 'B', 8.5)
            self.set_text_color(15, 23, 42)
            self.cell(col_w, 5, self.date_range_str, 0, 0, 'L')

            # Spalte 3: Zeitzone
            x_offset += col_w
            self.set_xy(x_offset, box_y + 2.0)
            self.set_font('Arial', 'B', 6.5)
            self.set_text_color(100, 116, 139)
            self.cell(col_w, 3.5, "ZEITZONE", 0, 1, 'L')
            self.set_xy(x_offset, box_y + 6.5)
            self.set_font('Arial', 'B', 8.5)
            self.set_text_color(15, 23, 42)
            self.cell(col_w, 5, self.tz_name, 0, 0, 'L')

            # Spalte 4: Übersicht
            x_offset += col_w
            self.set_xy(x_offset, box_y + 2.0)
            self.set_font('Arial', 'B', 6.5)
            self.set_text_color(100, 116, 139)
            self.cell(col_w, 3.5, "EREIGNISSE", 0, 1, 'L')
            self.set_xy(x_offset, box_y + 6.5)
            self.set_font('Arial', 'B', 8.5)
            self.set_text_color(15, 23, 42)
            t_total = f"{self.total_events} gesamt  "
            self.cell(self.get_string_width(t_total), 5, t_total, 0, 0, 'L')
            self.set_text_color(21, 128, 61)  # Emerald 700
            self.cell(col_w, 5, f"({self.visible_events} sichtbar)", 0, 0, 'L')

            self.set_y(box_y + box_h + 3.5)
        else:
            # Kompakter Header für Folgeseiten
            self.set_y(8)
            self.set_font('Arial', 'B', 8)
            self.set_text_color(30, 41, 59)
            self.cell(60, 5, "MoonEvents - Beobachtungsplan", 0, 0, 'L')

            self.set_font('Arial', '', 7.5)
            self.set_text_color(71, 85, 105)
            self.cell(page_w - 120, 5, f"{self.location_name} | {self.date_range_str} ({self.tz_name})", 0, 0, 'C')

            self.set_font('Arial', '', 7.5)
            self.set_text_color(100, 116, 139)
            self.cell(60, 5, f"Seite {self.page_no()} von {{nb}}", 0, 1, 'R')

            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.3)
            self.line(self.l_margin, 13.5, self.l_margin + page_w, 13.5)
            self.set_y(15.5)

    def footer(self):
        self.set_y(-12)
        page_w = self.w - self.l_margin - self.r_margin

        # Dezente Trennlinie über der Fußzeile
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.l_margin + page_w, self.get_y())
        self.ln(1)

        self.set_font('Arial', '', 7.5)
        self.set_text_color(100, 116, 139)

        # Links: Software & Datum
        left_str = f"MoonEvents v{self.version}  |  Berechnet: {self.calc_date}"
        self.cell(90, 6, left_str, 0, 0, 'L')

        # Mitte: Webseite
        self.cell(page_w - 150, 6, "https://www.anton-bader.de", 0, 0, 'C')

        # Rechts: Seitenzahl
        self.cell(60, 6, f"Seite {self.page_no()} von {{nb}}", 0, 0, 'R')


def create_pdf(filename, results, location_name, offset, version_str, start_date, end_date, tz_label=None):
    calc_date_str = datetime.now().strftime("%d.%m.%Y")
    s_str = start_date.strftime("%d.%m.%Y")
    e_str = end_date.strftime("%d.%m.%Y")
    date_range_str = f"{s_str} bis {e_str}"

    if tz_label:
        tz_name = tz_label
    elif offset == 1:
        tz_name = "MEZ/MESZ"
    elif offset >= 0:
        tz_name = f"UTC+{offset}"
    else:
        tz_name = f"UTC{offset}"

    visible_count = sum(1 for r in results if r.get('visible'))

    pdf = PDFReport(
        version=version_str,
        calc_date=calc_date_str,
        location_name=location_name,
        date_range_str=date_range_str,
        tz_name=tz_name,
        total_events=len(results),
        visible_events=visible_count,
        orientation='L',
        unit='mm',
        format='A4',
    )
    pdf.set_auto_page_break(False)
    pdf.add_page()

    w_event = 44
    w_start = 25
    w_optimum = 25
    w_theo = 25
    w_end = 25
    w_status = 40
    w_diff = 22
    total_w = pdf.w - pdf.l_margin - pdf.r_margin
    w_desc = total_w - (w_event + w_start + w_optimum + w_theo + w_end + w_status + w_diff)

    def print_table_header():
        h_head = 7.5
        pdf.set_font("Arial", 'B', 8)
        pdf.set_fill_color(30, 41, 59)   # Dunkles Schieferblau #1E293B
        pdf.set_text_color(255, 255, 255)
        pdf.set_draw_color(30, 41, 59)

        x = pdf.l_margin
        y = pdf.get_y()

        cols = [
            (w_event, "Ereignis", 'L'),
            (w_start, "Start", 'C'),
            (w_optimum, "Optimum", 'C'),
            (w_theo, "Theor. Opt.", 'C'),
            (w_end, "Ende", 'C'),
            (w_status, "Sichtbarkeit", 'L'),
            (w_diff, "Schwierigkeit", 'C'),
            (w_desc, "Beschreibung", 'L'),
        ]

        for w_col, title, align in cols:
            pdf.rect(x, y, w_col, h_head, 'F')
            pdf.set_xy(x, y + 1.2)
            pdf.cell(w_col, h_head - 2.4, title, 0, 0, align)
            x += w_col

        pdf.set_y(y + h_head)

    print_table_header()

    if not results:
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 5)
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(total_w, 10, "Keine Ereignisse für den gewählten Zeitraum und Filter gefunden.", border=1, align='C')
        pdf.output(filename)
        return

    PAGE_HEIGHT_LIMIT = 191.0
    line_height = 3.8
    padding_y = 2.4

    for idx, row in enumerate(results):
        evt_name = _sanitize_latin1(row['event']['name'])
        start_str = row['start_local'].strftime("%d.%m.%Y %H:%M")
        peak_str = row['peak_local'].strftime("%d.%m.%Y %H:%M")
        theo_str = row['theo_peak_local'].strftime("%d.%m.%Y %H:%M")
        end_str = row['end_local'].strftime("%d.%m.%Y %H:%M")

        status = row['status_text']
        if row['visible']:
            status += f" (Alt: {row['moon_alt']:.1f}°)"
        desc = row['event'].get('desc', '')
        difficulty = row['event'].get('difficulty', '-')

        evt_name = _sanitize_latin1(evt_name)
        desc = _sanitize_latin1(desc)
        status = _sanitize_latin1(status)
        difficulty = _sanitize_latin1(difficulty)

        lines_event = get_text_lines(pdf, evt_name, w_event, 'Arial', 'B', 8)
        lines_status = get_text_lines(pdf, status, w_status, 'Arial', '', 7.5)
        lines_desc = get_text_lines(pdf, desc, w_desc, 'Arial', '', 7.5)

        max_lines = max(len(lines_event), len(lines_status), len(lines_desc), 1)
        row_height = max_lines * line_height + padding_y

        if pdf.get_y() + row_height > PAGE_HEIGHT_LIMIT:
            pdf.add_page()
            print_table_header()

        y_row = pdf.get_y()
        x_start = pdf.l_margin

        # Alternierender Zebra-Hintergrund
        if idx % 2 == 1:
            pdf.set_fill_color(248, 250, 252)  # #F8FAFC
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.rect(x_start, y_row, total_w, row_height, 'F')

        # Dezente Zell-Rahmen in Hellgrau
        pdf.set_draw_color(226, 232, 240)  # #E2E8F0
        pdf.set_line_width(0.2)

        cur_x = x_start
        for w_col in [w_event, w_start, w_optimum, w_theo, w_end, w_status, w_diff, w_desc]:
            pdf.rect(cur_x, y_row, w_col, row_height, 'D')
            cur_x += w_col

        # 1. Ereignis (mehrzeilig umgebrochen)
        cur_x = x_start
        pdf.set_xy(cur_x, y_row + 1.2)
        pdf.set_font("Arial", 'B', 8)
        pdf.set_text_color(15, 23, 42)
        pdf.multi_cell(w_event, line_height, "\n".join(lines_event), border=0, align='L')

        # 2. Start (vertikal zentriert)
        cur_x += w_event
        pdf.set_xy(cur_x, y_row + (row_height - line_height) / 2)
        if row['vis_start']:
            pdf.set_font("Arial", 'B', 7.5)
            pdf.set_text_color(21, 128, 61)  # Emerald 700 (Sichtbar)
        else:
            pdf.set_font("Arial", '', 7.5)
            pdf.set_text_color(100, 116, 139) # Slate 500 (Nicht sichtbar)
        pdf.cell(w_start, line_height, start_str, border=0, align='C')

        # 3. Optimum (vertikal zentriert)
        cur_x += w_start
        pdf.set_xy(cur_x, y_row + (row_height - line_height) / 2)
        if row['vis_peak']:
            pdf.set_font("Arial", 'B', 7.5)
            pdf.set_text_color(21, 128, 61)
        else:
            pdf.set_font("Arial", '', 7.5)
            pdf.set_text_color(100, 116, 139)
        pdf.cell(w_optimum, line_height, peak_str, border=0, align='C')

        # 4. Theor. Opt. (vertikal zentriert)
        cur_x += w_optimum
        pdf.set_xy(cur_x, y_row + (row_height - line_height) / 2)
        if row['vis_peak_theo']:
            pdf.set_font("Arial", 'B', 7.5)
            pdf.set_text_color(21, 128, 61)
        else:
            pdf.set_font("Arial", '', 7.5)
            pdf.set_text_color(100, 116, 139)
        pdf.cell(w_theo, line_height, theo_str, border=0, align='C')

        # 5. Ende (vertikal zentriert)
        cur_x += w_theo
        pdf.set_xy(cur_x, y_row + (row_height - line_height) / 2)
        if row['vis_end']:
            pdf.set_font("Arial", 'B', 7.5)
            pdf.set_text_color(21, 128, 61)
        else:
            pdf.set_font("Arial", '', 7.5)
            pdf.set_text_color(100, 116, 139)
        pdf.cell(w_end, line_height, end_str, border=0, align='C')

        # 6. Sichtbarkeit (mehrzeilig umgebrochen)
        cur_x += w_end
        pdf.set_xy(cur_x, y_row + 1.2)
        pdf.set_font("Arial", '', 7.5)
        if row['visible']:
            pdf.set_text_color(21, 128, 61)
        else:
            pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(w_status, line_height, "\n".join(lines_status), border=0, align='L')

        # 7. Schwierigkeit (vertikal zentriert, farblich akzentuiert)
        cur_x += w_status
        pdf.set_xy(cur_x, y_row + (row_height - line_height) / 2)
        pdf.set_font("Arial", 'B', 7.5)
        if difficulty in ("Leicht", "Sehr Leicht"):
            pdf.set_text_color(21, 128, 61)
        elif difficulty == "Mittel":
            pdf.set_text_color(180, 83, 9)
        elif difficulty in ("Schwer", "Sehr Schwer"):
            pdf.set_text_color(185, 28, 28)
        else:
            pdf.set_text_color(100, 116, 139)
        pdf.cell(w_diff, line_height, difficulty, border=0, align='C')

        # 8. Beschreibung (mehrzeilig umgebrochen)
        cur_x += w_diff
        pdf.set_xy(cur_x, y_row + 1.2)
        pdf.set_font("Arial", '', 7.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(w_desc, line_height, "\n".join(lines_desc), border=0, align='L')

        pdf.set_y(y_row + row_height)

    pdf.output(filename)
