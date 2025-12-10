import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime, time, timedelta
import configparser
import webbrowser
import os

import mond_daten
import mond_storage
import mond_berechnung
import mond_pdf
import mond_map

class MondApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MoonEvents - Mondereignis-Rechner")
        self.geometry("1400x850")

        self.app_data = mond_storage.load_data()
        self.events_db = mond_daten.EREIGNISSE_DB
        self.version_info = self.load_config()
        self.var_show_only_visible = tk.BooleanVar(value=False)
        self.last_visible_event_names = set()

        self.create_widgets()

    def load_config(self):
        config = configparser.ConfigParser()
        defaults = {"version": "1.0", "date": "unknown"}
        if os.path.exists("info.conf"):
            try:
                config.read("info.conf")
                defaults["version"] = config["INFO"].get("version", "1.0")
                defaults["date"] = config["INFO"].get("date", "unknown")
            except: pass
        return defaults

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_locations = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_locations, text="Orte")
        self.setup_locations_tab()

        self.tab_events = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_events, text="Ereigniswahl")
        self.setup_events_tab()

        self.tab_calc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_calc, text="Berechnung")
        self.setup_calc_tab()

        self.tab_map = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_map, text="Karte")
        self.setup_map_tab()

        self.tab_info = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_info, text="Info")
        self.setup_info_tab()

    def on_closing(self):
        mond_storage.save_data(self.app_data)
        self.destroy()

    # --- TAB KARTE ---
    def setup_map_tab(self):
        # Control Frame
        ctrl_frame = ttk.Frame(self.tab_map)
        ctrl_frame.pack(fill='x', padx=5, pady=5)

        self.var_map_filter_visible = tk.BooleanVar(value=False)
        self.chk_map_visible = ttk.Checkbutton(ctrl_frame, text="Nur beobachtbare anzeigen (Berechnung erforderlich)",
                                               variable=self.var_map_filter_visible,
                                               command=self.update_map_filter,
                                               state='disabled')
        self.chk_map_visible.pack(side='left')

        self.map_widget = mond_map.MoonMap(self.tab_map)
        self.map_widget.pack(fill='both', expand=True)
        # Load initial selection
        self.update_map_selection()

        # Bind tab change to refresh map if needed (optional, but good practice)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

    def on_tab_changed(self, event):
        # Check if Map tab is selected
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Karte":
            self.update_map_selection()

    def update_map_filter(self):
        self.update_map_selection()

    def update_map_selection(self):
        sel_indices = self.app_data.get('selected_events_indices', [])
        selected_events = [self.events_db[i] for i in sel_indices if i < len(self.events_db)]

        # Filter logic
        if self.var_map_filter_visible.get():
            selected_events = [e for e in selected_events if e['name'] in self.last_visible_event_names]

        self.map_widget.update_events(selected_events)

    # --- TAB INFO ---
    def setup_info_tab(self):
        frame = ttk.Frame(self.tab_info)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        lbl_name = tk.Label(frame, text="MoonEvents", font=("Helvetica", 24, "bold"))
        lbl_name.pack(pady=(0, 5))
        lbl_sub = tk.Label(frame, text="Mondereignis-Rechner und Beobachtungsplaner", font=("Helvetica", 12))
        lbl_sub.pack(pady=(0, 30))
        v_text = f"Version: {self.version_info['version']}"
        lbl_ver = tk.Label(frame, text=v_text, font=("Helvetica", 10))
        lbl_ver.pack()
        d_text = f"Datum: {self.version_info['date']}"
        lbl_date = tk.Label(frame, text=d_text, font=("Helvetica", 10))
        lbl_date.pack(pady=(0, 30))
        lbl_email = tk.Label(frame, text="info@anton-bader.de", font=("Helvetica", 10))
        lbl_email.pack()
        link_text = "https://www.anton-bader.de"
        lbl_link = tk.Label(frame, text=link_text, font=("Helvetica", 10, "underline"), fg="blue", cursor="hand2")
        lbl_link.pack(pady=(5, 0))
        lbl_link.bind("<Button-1>", lambda e: webbrowser.open(link_text))

    # --- TAB 1: ORTE ---
    def setup_locations_tab(self):
        frame = ttk.Frame(self.tab_locations)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        list_frame = ttk.LabelFrame(frame, text="Gespeicherte Orte")
        list_frame.pack(side='left', fill='y', padx=5)
        self.loc_listbox = tk.Listbox(list_frame, width=30)
        self.loc_listbox.pack(fill='y', expand=True, padx=5, pady=5)
        self.loc_listbox.bind('<<ListboxSelect>>', self.on_location_select)
        detail_frame = ttk.LabelFrame(frame, text="Ort bearbeiten")
        detail_frame.pack(side='right', fill='both', expand=True, padx=5)
        fields = [("Name:", "entry_name"), ("Breite:", "entry_lat"),
                  ("Länge:", "entry_lon"), ("Höhe (m):", "entry_elev"),
                  ("UTC Offset:", "entry_offset")]
        for i, (txt, var) in enumerate(fields):
            ttk.Label(detail_frame, text=txt).grid(row=i, column=0, sticky='w', padx=5)
            e = ttk.Entry(detail_frame); e.grid(row=i, column=1, sticky='ew', padx=5)
            setattr(self, var, e)
        btn_frame = ttk.Frame(detail_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Neu", command=self.add_location).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Löschen", command=self.delete_location).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Aktiv setzen", command=self.set_active_location).pack(side='left', padx=2)
        self.lbl_active_loc = ttk.Label(detail_frame, text="Aktiver Ort: -", font=('Arial', 10, 'bold'))
        self.lbl_active_loc.grid(row=6, column=0, columnspan=2, pady=10)
        self.refresh_loc_list()

    def refresh_loc_list(self):
        self.loc_listbox.delete(0, tk.END)
        for loc in self.app_data['locations']: self.loc_listbox.insert(tk.END, loc['name'])
        idx = self.app_data.get('selected_location_index', 0)
        if 0 <= idx < len(self.app_data['locations']):
            self.lbl_active_loc.config(text=f"Aktiver Ort: {self.app_data['locations'][idx]['name']}")
    def on_location_select(self, event):
        sel = self.loc_listbox.curselection()
        if not sel: return
        loc = self.app_data['locations'][sel[0]]
        self.entry_name.delete(0, tk.END); self.entry_name.insert(0, loc['name'])
        self.entry_lat.delete(0, tk.END); self.entry_lat.insert(0, str(loc['lat']))
        self.entry_lon.delete(0, tk.END); self.entry_lon.insert(0, str(loc['lon']))
        self.entry_elev.delete(0, tk.END); self.entry_elev.insert(0, str(loc['elevation']))
        self.entry_offset.delete(0, tk.END); self.entry_offset.insert(0, str(loc.get('timezone_offset', 1)))
    def add_location(self):
        try:
            new_loc = {"name": self.entry_name.get(), "lat": float(self.entry_lat.get()),
                       "lon": float(self.entry_lon.get()), "elevation": float(self.entry_elev.get()),
                       "timezone_offset": int(self.entry_offset.get())}
            self.app_data['locations'].append(new_loc)
            self.refresh_loc_list()
            mond_storage.save_data(self.app_data)
        except: messagebox.showerror("Fehler", "Eingabe prüfen.")
    def delete_location(self):
        sel = self.loc_listbox.curselection()
        if not sel or len(self.app_data['locations']) <= 1: return
        del self.app_data['locations'][sel[0]]
        self.app_data['selected_location_index'] = 0
        self.refresh_loc_list()
        mond_storage.save_data(self.app_data)
    def set_active_location(self):
        sel = self.loc_listbox.curselection()
        if not sel: return
        self.app_data['selected_location_index'] = sel[0]
        self.refresh_loc_list()
        mond_storage.save_data(self.app_data)

    # --- TAB 2: EREIGNISSE ---
    def setup_events_tab(self):
        lbl = ttk.Label(self.tab_events, text="Ereignisse auswählen:")
        lbl.pack(pady=5)

        btn_frame = ttk.Frame(self.tab_events)
        btn_frame.pack(pady=(0, 5))
        ttk.Button(btn_frame, text="Alle auswählen", command=self.select_all_events).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Alle abwählen", command=self.deselect_all_events).pack(side='left', padx=5)

        canvas = tk.Canvas(self.tab_events)
        scrollbar = ttk.Scrollbar(self.tab_events, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.event_vars = []
        sel_indices = self.app_data.get('selected_events_indices', [])
        for i, event in enumerate(self.events_db):
            var = tk.BooleanVar(value=(i in sel_indices))

            # Mondalter berechnen und Text anpassen
            moon_age = mond_berechnung.calculate_moon_age_approx(event.get('colong', 0))
            display_text = f"{event['name']} (Tag {moon_age:.1f})"

            chk = ttk.Checkbutton(scroll_frame, text=display_text, variable=var, command=self.save_event_selection)

            # Grid-Layout: 2 Spalten
            row = i // 2
            col = i % 2
            chk.grid(row=row, column=col, sticky='w', padx=20, pady=2)

            self.event_vars.append(var)
    def save_event_selection(self):
        self.app_data['selected_events_indices'] = [i for i, var in enumerate(self.event_vars) if var.get()]
        mond_storage.save_data(self.app_data)
        # Update map if it exists
        if hasattr(self, 'map_widget'):
            self.update_map_selection()

    def select_all_events(self):
        for var in self.event_vars:
            var.set(True)
        self.save_event_selection()

    def deselect_all_events(self):
        for var in self.event_vars:
            var.set(False)
        self.save_event_selection()

    # --- TAB 3: BERECHNUNG ---
    def setup_calc_tab(self):
        top_frame = ttk.Frame(self.tab_calc)
        top_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(top_frame, text="Start:").pack(side='left')
        self.date_entry_start = DateEntry(top_frame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='dd.mm.yyyy')
        self.date_entry_start.pack(side='left', padx=5)
        ttk.Label(top_frame, text="Ende:").pack(side='left', padx=(10,0))
        self.date_entry_end = DateEntry(top_frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='dd.mm.yyyy')
        next_month = datetime.now() + timedelta(days=30)
        self.date_entry_end.set_date(next_month)
        self.date_entry_end.pack(side='left', padx=5)
        chk_filter = ttk.Checkbutton(top_frame, text="Nur gut sichtbare anzeigen", variable=self.var_show_only_visible)
        chk_filter.pack(side='left', padx=20)
        ttk.Button(top_frame, text="Berechnen", command=self.run_calculation).pack(side='left', padx=10)
        ttk.Button(top_frame, text="PDF Export", command=self.export_pdf).pack(side='right')

        tree_frame = ttk.Frame(self.tab_calc)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        cols = ('Ereignis', 'Start', 'Optimum', 'TheorOpt', 'Ende', 'Status', 'Beschreibung')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.heading('Ereignis', text='Ereignis')
        self.tree.heading('Start', text='Start')
        self.tree.heading('Optimum', text='Optimum')
        self.tree.heading('TheorOpt', text='Theor. Optimum')
        self.tree.heading('Ende', text='Ende')
        self.tree.heading('Status', text='Sichtbarkeit')
        self.tree.heading('Beschreibung', text='Beschreibung')

        self.tree.column('Ereignis', width=140)
        self.tree.column('Start', width=130)
        self.tree.column('Optimum', width=130)
        self.tree.column('TheorOpt', width=130)
        self.tree.column('Ende', width=130)
        self.tree.column('Status', width=180)
        self.tree.column('Beschreibung', width=300)

        self.tree.tag_configure('good', foreground='green')
        self.tree.tag_configure('bad', foreground='red')

        self.current_results = []
        self.filtered_results = []

    def run_calculation(self):
        loc_idx = self.app_data.get('selected_location_index', 0)
        if loc_idx >= len(self.app_data['locations']): loc_idx = 0
        location = self.app_data['locations'][loc_idx]
        sel_indices = self.app_data.get('selected_events_indices', [])
        selected_events = [self.events_db[i] for i in sel_indices if i < len(self.events_db)]
        if not selected_events:
            messagebox.showinfo("Info", "Keine Ereignisse gewählt.")
            return
        d_start = self.date_entry_start.get_date()
        d_end = self.date_entry_end.get_date()
        if d_end < d_start:
            messagebox.showwarning("Fehler", "Enddatum liegt vor Startdatum!")
            return
        offset = location.get('timezone_offset', 1)
        start_dt_local = datetime.combine(d_start, time(0,0,0))
        start_dt_utc = start_dt_local - mond_berechnung.timedelta(hours=offset)
        end_dt_local = datetime.combine(d_end, time(23,59,59))
        end_dt_utc = end_dt_local - mond_berechnung.timedelta(hours=offset)
        self.config(cursor="watch")
        self.update()
        try:
            raw_results = mond_berechnung.calculate_all_events(
                start_dt_utc, end_dt_utc, selected_events, location
            )
            self.current_results = raw_results

            # Update Map Filter Data
            self.last_visible_event_names = {res['event']['name'] for res in raw_results if res['visible']}
            if hasattr(self, 'chk_map_visible'):
                self.chk_map_visible.config(state='normal')

            self.update_tree_display()
        finally:
            self.config(cursor="")

    def update_tree_display(self):
        self.tree.delete(*self.tree.get_children())
        self.filtered_results = []
        filter_active = self.var_show_only_visible.get()

        for row in self.current_results:
            if filter_active and not row['visible']:
                continue
            self.filtered_results.append(row)

            s_str = row['start_local'].strftime("%d.%m.%Y %H:%M")
            p_str = row['peak_local'].strftime("%d.%m.%Y %H:%M")
            tp_str = row['theo_peak_local'].strftime("%d.%m.%Y %H:%M")
            e_str = row['end_local'].strftime("%d.%m.%Y %H:%M")

            status_text = row['status_text']
            full_desc = row['event']['desc']
            short_desc = (full_desc[:60] + '..') if len(full_desc) > 60 else full_desc

            row_tag = 'good' if row['visible'] else 'bad'
            self.tree.insert('', tk.END, values=(
                row['event']['name'], s_str, p_str, tp_str, e_str, status_text, short_desc
            ), tags=(row_tag,))

    def export_pdf(self):
        if not self.filtered_results:
            messagebox.showinfo("Info", "Keine Daten (Filter prüfen).")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if filename:
            loc_idx = self.app_data.get('selected_location_index', 0)
            loc = self.app_data['locations'][loc_idx]
            current_version = self.version_info.get('version', '1.0')
            d_start = self.date_entry_start.get_date()
            d_end = self.date_entry_end.get_date()
            mond_pdf.create_pdf(
                filename, self.filtered_results, loc['name'], loc.get('timezone_offset', 1),
                current_version, d_start, d_end
            )
            messagebox.showinfo("Erfolg", "PDF gespeichert.")
