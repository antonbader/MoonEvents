# mond_pdf.py
from fpdf import FPDF
from datetime import datetime
import math

class PDFReport(FPDF):
    def __init__(self, version, calc_date, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.version = version
        self.calc_date = calc_date

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'MoonEvents - Beobachtungsplan', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        footer_text = (f"MoonEvents v{self.version} | "
                       f"Berechnet: {self.calc_date} | "
                       f"https://www.anton-bader.de | "
                       f"Seite {self.page_no()}")
        self.cell(0, 10, footer_text, 0, 0, 'C')

    def get_lines_count(self, text, width):
        if not text: return 1
        text_width = self.get_string_width(text)
        if text_width < width: return 1
        words = text.split()
        current_line_len = 0
        lines = 1
        space_width = self.get_string_width(' ')
        for word in words:
            word_width = self.get_string_width(word)
            if current_line_len + word_width > width:
                lines += 1
                current_line_len = word_width
            else:
                current_line_len += word_width + space_width
        return lines

def create_pdf(filename, results, location_name, offset, version_str, start_date, end_date):
    calc_date_str = datetime.now().strftime("%d.%m.%Y")
    pdf = PDFReport(version=version_str, calc_date=calc_date_str, orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(False)
    pdf.add_page()
    
    w_event = 45
    w_start = 35 
    w_optimum = 35 
    w_end = 35 
    w_status = 40
    w_desc = 85 
    
    def print_table_header():
        pdf.set_font("Arial", 'B', 9)
        pdf.set_fill_color(220, 220, 220)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w_event, 8, "Ereignis", 1, 0, 'L', True)
        pdf.cell(w_start, 8, "Start", 1, 0, 'L', True)
        pdf.cell(w_optimum, 8, "Optimum", 1, 0, 'L', True)
        pdf.cell(w_end, 8, "Ende", 1, 0, 'L', True)
        pdf.cell(w_status, 8, "Sichtbarkeit", 1, 0, 'L', True)
        pdf.cell(w_desc, 8, "Beschreibung", 1, 1, 'L', True)
        pdf.ln()

    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    tz_name = "MEZ" if offset == 1 else f"UTC+{offset}"
    s_str = start_date.strftime("%d.%m.%Y")
    e_str = end_date.strftime("%d.%m.%Y")
    
    pdf.cell(0, 5, f"Ort: {location_name}", 0, 1)
    pdf.cell(0, 5, f"Zeitzone: {tz_name}", 0, 1)
    pdf.cell(0, 5, f"Berechnungszeitraum: {s_str} bis {e_str}", 0, 1)
    pdf.ln(5)
    
    print_table_header()
    pdf.set_font("Arial", size=9)
    PAGE_HEIGHT_LIMIT = 190 
    
    for row in results:
        pdf.set_text_color(0, 0, 0)
        evt_name = row['event']['name']
        
        start_str = row['start_local'].strftime("%d.%m.%Y %H:%M")
        peak_str = row['peak_local'].strftime("%d.%m.%Y %H:%M")
        end_str = row['end_local'].strftime("%d.%m.%Y %H:%M")
        
        status = row['status_text']
        if row['visible']:
            status += f" (Alt: {row['moon_alt']:.1f}°)"
        desc = row['event']['desc']
        
        try:
            evt_name = evt_name.encode('latin-1', 'replace').decode('latin-1')
            desc = desc.encode('latin-1', 'replace').decode('latin-1')
            status = status.encode('latin-1', 'replace').decode('latin-1')
        except: pass

        lines_desc = pdf.get_lines_count(desc, w_desc - 2)
        lines_status = pdf.get_lines_count(status, w_status - 2)
        line_height_base = 5
        max_lines = max(lines_desc, lines_status)
        row_height = (max_lines * line_height_base) + 2
        
        if pdf.get_y() + row_height > PAGE_HEIGHT_LIMIT:
            pdf.add_page()
            print_table_header()
            pdf.set_font("Arial", size=9) 
            pdf.set_text_color(0, 0, 0)

        y_start = pdf.get_y()
        x_start = pdf.get_x()
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(x_start, y_start)
        pdf.cell(w_event, row_height, evt_name, 1, 0, 'L')
        
        if row['vis_start']: pdf.set_text_color(0, 128, 0)
        else: pdf.set_text_color(0, 0, 0)
        pdf.set_xy(x_start + w_event, y_start)
        pdf.set_font("Arial", size=8)
        pdf.cell(w_start, row_height, start_str, 1, 0, 'L')
        
        if row['vis_peak']: pdf.set_text_color(0, 128, 0)
        else: pdf.set_text_color(0, 0, 0)
        pdf.set_xy(x_start + w_event + w_start, y_start)
        pdf.cell(w_optimum, row_height, peak_str, 1, 0, 'L')
        
        if row['vis_end']: pdf.set_text_color(0, 128, 0)
        else: pdf.set_text_color(0, 0, 0)
        pdf.set_xy(x_start + w_event + w_start + w_optimum, y_start)
        pdf.cell(w_end, row_height, end_str, 1, 0, 'L')
        pdf.set_font("Arial", size=9)
        
        if not row['visible']: pdf.set_text_color(100, 100, 100)
        else: pdf.set_text_color(0, 0, 0)
        
        pdf.set_xy(x_start + w_event + w_start + w_optimum + w_end, y_start)
        pdf.cell(w_status, row_height, "", 1) 
        pdf.set_xy(x_start + w_event + w_start + w_optimum + w_end, y_start)
        pdf.multi_cell(w_status, line_height_base, status, border=0, align='L')
        
        pdf.set_xy(x_start + w_event + w_start + w_optimum + w_end + w_status, y_start)
        pdf.cell(w_desc, row_height, "", 1)
        pdf.set_xy(x_start + w_event + w_start + w_optimum + w_end + w_status, y_start)
        pdf.multi_cell(w_desc, line_height_base, desc, border=0, align='L')
        
        pdf.set_y(y_start + row_height)

    pdf.output(filename)