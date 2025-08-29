"""
Modern Splash Screen with Animations
Beautiful loading screen with gradient background and smooth animations
"""

import math
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import threading
from .UI.theme_manager import theme_manager
from .UI.animation_manager import animation_manager
from .UI.icon_manager import icon_manager


class ModernSplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Splash screen dimensions
        self.width = 900
        self.height = 500

        # Center the splash screen
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')

        # Configure for modern look
        self.setup_ui()
        self.create_gradient_background()
        self.create_content()
        self.start_animations()

    def setup_ui(self):
        """Setup the UI components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#1e293b')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for gradient background
        self.canvas = tk.Canvas(self.main_frame, width=self.width, height=self.height,
                                highlightthickness=0, relief='flat')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def create_gradient_background(self):
        """Create a gradient background"""
        # Create gradient effect using rectangles
        colors = ['#0f172a', '#1e293b', '#334155', '#475569']

        # Vertical gradient
        for i in range(self.height):
            ratio = i / self.height

            # Interpolate between colors
            if ratio < 0.33:
                # Between color 0 and 1
                local_ratio = ratio / 0.33
                r1, g1, b1 = int(colors[0][1:3], 16), int(
                    colors[0][3:5], 16), int(colors[0][5:7], 16)
                r2, g2, b2 = int(colors[1][1:3], 16), int(
                    colors[1][3:5], 16), int(colors[1][5:7], 16)
            elif ratio < 0.66:
                # Between color 1 and 2
                local_ratio = (ratio - 0.33) / 0.33
                r1, g1, b1 = int(colors[1][1:3], 16), int(
                    colors[1][3:5], 16), int(colors[1][5:7], 16)
                r2, g2, b2 = int(colors[2][1:3], 16), int(
                    colors[2][3:5], 16), int(colors[2][5:7], 16)
            else:
                # Between color 2 and 3
                local_ratio = (ratio - 0.66) / 0.34
                r1, g1, b1 = int(colors[2][1:3], 16), int(
                    colors[2][3:5], 16), int(colors[2][5:7], 16)
                r2, g2, b2 = int(colors[3][1:3], 16), int(
                    colors[3][3:5], 16), int(colors[3][5:7], 16)

            # Interpolate RGB values
            r = int(r1 + (r2 - r1) * local_ratio)
            g = int(g1 + (g2 - g1) * local_ratio)
            b = int(b1 + (b2 - b1) * local_ratio)

            color = f'#{r:02x}{g:02x}{b:02x}'

            # Draw gradient line (draw every 2 pixels for performance)
            if i % 2 == 0:
                self.canvas.create_line(
                    0, i, self.width, i, fill=color, width=2)

    def create_content(self):
        """Create splash screen content"""
        # App icon (create a modern PDF icon)
        try:
            icon_img = icon_manager.create_pdf_icon((80, 80), "#3b82f6")
            self.app_icon = ImageTk.PhotoImage(icon_img)

            # App icon with glow effect
            icon_x = self.width // 2
            icon_y = 120

            # Glow effect (multiple circles with decreasing opacity)
            for radius in range(50, 10, -5):
                opacity = int(255 * (10 / (60 - radius)))
                glow_color = f'#3b82f6'
                self.canvas.create_oval(icon_x - radius, icon_y - radius,
                                        icon_x + radius, icon_y + radius,
                                        outline=glow_color, width=1, tags="glow")

            self.canvas.create_image(
                icon_x, icon_y, image=self.app_icon, tags="icon")
        except Exception as e:
            print(f"Error creating icon: {e}")

        # App title
        self.canvas.create_text(self.width // 2, 220, text="Image to PDF Converter",
                                font=("Segoe UI", 28, "bold"), fill="#f8fafc",
                                tags="title")

        # Subtitle with animation
        self.canvas.create_text(self.width // 2, 260, text="Professional • Modern • Fast",
                                font=("Segoe UI", 14), fill="#cbd5e1",
                                tags="subtitle")

        # Developer info
        self.canvas.create_text(self.width // 2, 320, text="Developed by Samarth Raut",
                                font=("Segoe UI", 12), fill="#94a3b8",
                                tags="developer")

        # Progress bar background
        progress_y = 380
        progress_width = 400
        progress_height = 8
        progress_x = (self.width - progress_width) // 2

        # Progress bar background
        self.canvas.create_rounded_rectangle(
            progress_x, progress_y, progress_x + progress_width, progress_y + progress_height,
            radius=4, fill="#334155", outline="", tags="progress_bg"
        )

        # Progress bar (will be animated)
        self.progress_bar = self.canvas.create_rounded_rectangle(
            progress_x, progress_y, progress_x, progress_y + progress_height,
            radius=4, fill="#3b82f6", outline="", tags="progress"
        )

        # Loading text
        self.loading_text = self.canvas.create_text(self.width // 2, 420, text="Loading...",
                                                    font=("Segoe UI", 11), fill="#94a3b8",
                                                    tags="loading")

        # Version info
        self.canvas.create_text(self.width // 2, 460, text="Version 2.0 • Enhanced Edition",
                                font=("Segoe UI", 10), fill="#64748b",
                                tags="version")

    def start_animations(self):
        """Start loading animations"""
        # Animate title fade in
        self.animate_fade_in("title", delay=300)

        # Animate subtitle fade in
        self.animate_fade_in("subtitle", delay=600)

        # Animate developer info
        self.animate_fade_in("developer", delay=900)

        # Animate version info
        self.animate_fade_in("version", delay=1200)

        # Start progress bar animation
        self.animate_progress_bar()

        # Start icon glow animation
        self.animate_icon_glow()

        # Start loading text animation
        self.animate_loading_text()

    def animate_fade_in(self, tag, delay=0):
        """Animate element fade in"""
        def fade_in():
            # Simple fade in by changing text color
            items = self.canvas.find_withtag(tag)
            if items:
                # This is a simplified fade - in a real implementation you'd
                # gradually change the alpha or use more sophisticated methods
                pass

        if delay > 0:
            self.root.after(delay, fade_in)
        else:
            fade_in()

    def animate_progress_bar(self):
        """Animate the progress bar"""
        progress_width = 400
        progress_x = (self.width - progress_width) // 2
        progress_y = 380
        progress_height = 8

        steps = 100
        step_duration = 30  # milliseconds

        def update_progress(step):
            if step <= steps:
                current_width = (progress_width * step) // steps

                # Update progress bar
                self.canvas.coords(self.progress_bar,
                                   progress_x, progress_y,
                                   progress_x + current_width, progress_y + progress_height)

                # Continue animation
                self.root.after(
                    step_duration, lambda: update_progress(step + 1))
            else:
                # Animation complete, close splash screen
                self.close_splash()

        update_progress(0)

    def animate_icon_glow(self):
        """Animate icon glow effect"""
        def pulse_glow():
            # Simple glow animation by modifying the glow elements
            glow_items = self.canvas.find_withtag("glow")

            # This would be enhanced with actual opacity changes in a real implementation
            self.root.after(1000, pulse_glow)

        pulse_glow()

    def animate_loading_text(self):
        """Animate loading text with dots"""
        loading_states = ["Loading", "Loading.", "Loading..", "Loading..."]
        current_state = 0

        def update_loading_text():
            nonlocal current_state

            self.canvas.itemconfig(
                self.loading_text, text=loading_states[current_state])
            current_state = (current_state + 1) % len(loading_states)

            self.root.after(500, update_loading_text)

        update_loading_text()

    def close_splash(self):
        """Close splash screen and show main app"""
        def fade_out():
            # Simple fade out effect
            self.root.after(500, self.show_main_app)

        fade_out()

    def show_main_app(self):
        """Show the main application"""
        self.root.destroy()

        # Import and show the main app
        from .startingpage import ModernStartingPage

        root = tk.Tk()
        app = ModernStartingPage(root)
        root.mainloop()


# Add rounded rectangle method to Canvas
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
    """Create a rounded rectangle on canvas"""
    points = []

    # Top left
    points.extend([x1 + radius, y1])
    points.extend([x2 - radius, y1])

    # Top right arc
    for i in range(90, -1, -1):
        x = x2 - radius + radius * math.cos(math.radians(i))
        y = y1 + radius - radius * math.sin(math.radians(i))
        points.extend([x, y])

    # Right side
    points.extend([x2, y1 + radius])
    points.extend([x2, y2 - radius])

    # Bottom right arc
    for i in range(0, 91):
        x = x2 - radius + radius * math.cos(math.radians(i))
        y = y2 - radius + radius * math.sin(math.radians(i))
        points.extend([x, y])

    # Bottom side
    points.extend([x2 - radius, y2])
    points.extend([x1 + radius, y2])

    # Bottom left arc
    for i in range(90, 181):
        x = x1 + radius + radius * math.cos(math.radians(i))
        y = y2 - radius + radius * math.sin(math.radians(i))
        points.extend([x, y])

    # Left side
    points.extend([x1, y2 - radius])
    points.extend([x1, y1 + radius])

    # Top left arc
    for i in range(180, 271):
        x = x1 + radius + radius * math.cos(math.radians(i))
        y = y1 + radius + radius * math.sin(math.radians(i))
        points.extend([x, y])

    return self.create_polygon(points, smooth=True, **kwargs)


# Add method to Canvas class
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle
