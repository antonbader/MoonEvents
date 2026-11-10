# mond_map.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import math


class MoonMap(ttk.Frame):
    def __init__(self, parent, image_path="moon_map.jpg", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_path = image_path
        self.original_image = None
        self.display_image = None
        self.photo_image = None

        self.lib_lat_deg = 0.0
        self.lib_lon_deg = 0.0

        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill='both', expand=True)

        self.load_image()
        self.canvas.bind("<Configure>", self.on_resize)

        # Store events to display
        self.current_events = []

    def set_libration(self, lib_lat_deg: float = 0.0, lib_lon_deg: float = 0.0):
        self.lib_lat_deg = float(lib_lat_deg)
        self.lib_lon_deg = float(lib_lon_deg)
        self.draw_events()

    def load_image(self):
        try:
            self.original_image = Image.open(self.image_path)
        except Exception as e:
            print(f"Error loading map image: {e}")
            self.original_image = Image.new('RGB', (800, 800), color='gray')
            draw = ImageDraw.Draw(self.original_image)
            draw.ellipse([50, 50, 750, 750], fill='lightgray', outline='white')

    def on_resize(self, event):
        if not self.original_image:
            return

        canvas_width = event.width
        canvas_height = event.height

        if canvas_width <= 1 or canvas_height <= 1:
            return

        img_w, img_h = self.original_image.size
        scale = min(canvas_width / img_w, canvas_height / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        self.display_image = self.original_image.resize((new_w, new_h), Image.Resampling.BILINEAR)
        self.photo_image = ImageTk.PhotoImage(self.display_image)

        x_pos = (canvas_width - new_w) // 2
        y_pos = (canvas_height - new_h) // 2

        self.canvas.delete("all")
        self.canvas.create_image(x_pos, y_pos, anchor='nw', image=self.photo_image)

        self.map_x_offset = x_pos
        self.map_y_offset = y_pos
        self.map_scale = new_w / img_w

        self.current_img_w = new_w
        self.current_img_h = new_h

        self.draw_events()

    def update_events(self, events):
        self.current_events = events
        self.draw_events()

    def draw_events(self):
        self.canvas.delete("marker")

        if not self.display_image:
            return

        cx = self.map_x_offset + self.current_img_w / 2
        cy = self.map_y_offset + self.current_img_h / 2
        radius = (min(self.current_img_w, self.current_img_h) / 2) * 0.98

        b_lib = math.radians(self.lib_lat_deg)
        l_lib = math.radians(self.lib_lon_deg)

        events_with_pos = []
        for event in self.current_events:
            lat = event.get('lat', 0.0)
            lon = event.get('lon', 0.0)

            rad_lat = math.radians(lat)
            rad_lon = math.radians(lon)

            # Sichtbarkeitsprüfung auf der Vorderseite unter Berücksichtigung der Libration (b_lib, l_lib)
            cos_c = (
                math.sin(rad_lat) * math.sin(b_lib)
                + math.cos(rad_lat) * math.cos(b_lib) * math.cos(rad_lon - l_lib)
            )
            if cos_c <= 0.0:
                continue

            # Orthografische Projektion mit Libration
            x_proj = math.cos(rad_lat) * math.sin(rad_lon - l_lib)
            y_proj = (
                math.sin(rad_lat) * math.cos(b_lib)
                - math.cos(rad_lat) * math.sin(b_lib) * math.cos(rad_lon - l_lib)
            )

            screen_x = cx + (x_proj * radius)
            screen_y = cy - (y_proj * radius)

            events_with_pos.append({
                'event': event,
                'x': screen_x,
                'y': screen_y
            })

        events_with_pos.sort(key=lambda item: item['y'])

        occupied_bboxes = []

        for item in events_with_pos:
            screen_x = item['x']
            screen_y = item['y']
            event_name = item['event']['name']

            r = 4
            self.canvas.create_oval(
                screen_x - r, screen_y - r, screen_x + r, screen_y + r,
                fill='red', outline='white', width=2, tags="marker"
            )

            label_x = screen_x + r + 4
            label_y = screen_y

            text_id = self.canvas.create_text(
                label_x, label_y, text=event_name,
                anchor='w', fill='#FFFF00', font=('Arial', 10, 'bold'), tags="marker"
            )

            bbox = self.canvas.bbox(text_id)
            if not bbox:
                continue

            shifts = 0
            max_shifts = 50
            step_y = (bbox[3] - bbox[1])
            if step_y < 5:
                step_y = 15

            has_collision = True
            while has_collision and shifts < max_shifts:
                has_collision = False
                current_bbox = self.canvas.bbox(text_id)

                for occ in occupied_bboxes:
                    if not (
                        current_bbox[2] < occ[0]
                        or current_bbox[0] > occ[2]
                        or current_bbox[3] < occ[1]
                        or current_bbox[1] > occ[3]
                    ):
                        has_collision = True
                        break

                if has_collision:
                    self.canvas.move(text_id, 0, step_y)
                    shifts += 1

            if shifts > 0:
                final_bbox = self.canvas.bbox(text_id)
                text_left_x = final_bbox[0]
                text_cent_y = (final_bbox[1] + final_bbox[3]) / 2

                line_id = self.canvas.create_line(
                    screen_x, screen_y, text_left_x, text_cent_y,
                    fill='white', width=1, tags="marker"
                )
                self.canvas.tag_lower(line_id, text_id)

            occupied_bboxes.append(self.canvas.bbox(text_id))
