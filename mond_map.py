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

        for event in self.current_events:
            lat = event.get('lat', 0)
            lon = event.get('lon', 0)

            # Orthographic Projection
            # x = R * cos(lat) * sin(lon)
            # y = R * sin(lat)
            # Note: Screen Y is inverted (down is positive).
            # North is Up (negative Y relative to center).
            # East is Right (positive X relative to center).

            rad_lat = math.radians(lat)
            rad_lon = math.radians(lon)

            # X coordinate on the sphere surface projected
            x_proj = math.cos(rad_lat) * math.sin(rad_lon)
            # Y coordinate (North is up)
            y_proj = math.sin(rad_lat)

            screen_x = cx + (x_proj * radius)
            screen_y = cy - (y_proj * radius) # Minus because screen Y grows downwards

            # Draw Marker
            r = 4 # Marker radius
            self.canvas.create_oval(screen_x - r, screen_y - r, screen_x + r, screen_y + r,
                                    fill='red', outline='white', width=2, tags="marker")

            # Draw Label
            self.canvas.create_text(screen_x + r + 4, screen_y, text=event['name'],
                                    anchor='w', fill='#FFFF00', font=('Arial', 10, 'bold'), tags="marker")
