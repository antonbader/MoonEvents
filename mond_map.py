# mond_map.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math

class MoonMap(ttk.Frame):
    def __init__(self, parent, image_path="moon_map.jpg", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_path = image_path
        self.original_image = None
        self.display_image = None
        self.photo_image = None

        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill='both', expand=True)

        self.load_image()
        self.canvas.bind("<Configure>", self.on_resize)

        # Store events to display
        self.current_events = []

    def load_image(self):
        try:
            self.original_image = Image.open(self.image_path)
        except Exception as e:
            print(f"Error loading map image: {e}")
            # Create a placeholder if image fails
            self.original_image = Image.new('RGB', (800, 800), color='gray')
            draw = ImageDraw.Draw(self.original_image)
            draw.ellipse([50, 50, 750, 750], fill='lightgray', outline='white')

    def on_resize(self, event):
        if not self.original_image:
            return

        # Resize image to fit canvas while maintaining aspect ratio
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

        # Center image
        x_pos = (canvas_width - new_w) // 2
        y_pos = (canvas_height - new_h) // 2

        self.canvas.delete("all")
        self.canvas.create_image(x_pos, y_pos, anchor='nw', image=self.photo_image)

        # Store offset and scale for plotting
        self.map_x_offset = x_pos
        self.map_y_offset = y_pos
        self.map_scale = new_w / img_w # Scale relative to original image dimensions?
        # Actually, projection is simpler if we treat new_w/new_h as the disc diameter
        # But image might have margins. Assuming crop is tight on the moon disc.
        # The downloaded image is usually a square or close to it with the moon centered.
        # Let's assume the moon disc fills the image (or close to it).

        self.current_img_w = new_w
        self.current_img_h = new_h

        # Redraw events
        self.draw_events()

    def update_events(self, events):
        self.current_events = events
        self.draw_events()

    def draw_events(self):
        # Clear existing markers (tagged with 'marker')
        self.canvas.delete("marker")

        if not self.display_image:
            return

        # Assuming the moon is a circle centered in the image
        # Center of the displayed image
        cx = self.map_x_offset + self.current_img_w / 2
        cy = self.map_y_offset + self.current_img_h / 2

        # Radius: half of width (approx). Adjust if image has black borders.
        # The downloaded LRO image usually has some black space.
        # Let's assume the moon diameter is approx 95% of image width for safety,
        # or just use width/2 if it's tight.
        # For the Wikipedia LRO image, it is quite tight.
        radius = (min(self.current_img_w, self.current_img_h) / 2) * 0.98

        # Calculate positions first
        events_with_pos = []
        for event in self.current_events:
            lat = event.get('lat', 0)
            lon = event.get('lon', 0)

            # Orthographic Projection
            rad_lat = math.radians(lat)
            rad_lon = math.radians(lon)

            # X coordinate on the sphere surface projected
            x_proj = math.cos(rad_lat) * math.sin(rad_lon)
            # Y coordinate (North is up)
            y_proj = math.sin(rad_lat)

            screen_x = cx + (x_proj * radius)
            screen_y = cy - (y_proj * radius) # Minus because screen Y grows downwards

            events_with_pos.append({
                'event': event,
                'x': screen_x,
                'y': screen_y
            })

        # Sort by Y to process top-down (helps with stacking)
        events_with_pos.sort(key=lambda item: item['y'])

        occupied_bboxes = []

        for item in events_with_pos:
            screen_x = item['x']
            screen_y = item['y']
            event_name = item['event']['name']

            # Draw Marker
            r = 4 # Marker radius
            self.canvas.create_oval(screen_x - r, screen_y - r, screen_x + r, screen_y + r,
                                    fill='red', outline='white', width=2, tags="marker")

            # Draw Label - Initial Position
            label_x = screen_x + r + 4
            label_y = screen_y

            text_id = self.canvas.create_text(label_x, label_y, text=event_name,
                                    anchor='w', fill='#FFFF00', font=('Arial', 10, 'bold'), tags="marker")

            # Collision Detection and Adjustment
            bbox = self.canvas.bbox(text_id) # (x1, y1, x2, y2)

            if not bbox:
                continue

            shifts = 0
            max_shifts = 50
            # Height of text (approximate step)
            step_y = (bbox[3] - bbox[1])
            if step_y < 5: step_y = 15 # Fallback

            has_collision = True
            while has_collision and shifts < max_shifts:
                has_collision = False
                current_bbox = self.canvas.bbox(text_id)

                # Check against all occupied bboxes
                for occ in occupied_bboxes:
                    # Overlap logic
                    if not (current_bbox[2] < occ[0] or \
                            current_bbox[0] > occ[2] or \
                            current_bbox[3] < occ[1] or \
                            current_bbox[1] > occ[3]):
                        has_collision = True
                        break

                if has_collision:
                    # Move down
                    self.canvas.move(text_id, 0, step_y)
                    shifts += 1

            # If we shifted, draw a line from marker to text
            if shifts > 0:
                final_bbox = self.canvas.bbox(text_id)
                text_left_x = final_bbox[0]
                text_cent_y = (final_bbox[1] + final_bbox[3]) / 2

                # Draw connecting line
                line_id = self.canvas.create_line(screen_x, screen_y, text_left_x, text_cent_y,
                                        fill='white', width=1, tags="marker")
                # Lower line so text is on top
                self.canvas.tag_lower(line_id, text_id)

            occupied_bboxes.append(self.canvas.bbox(text_id))
