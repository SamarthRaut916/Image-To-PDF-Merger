"""
Modern Starting Page with Beautiful UI
Welcome screen with modern design and smooth animations
"""

from Module.UI.icon_manager import icon_manager
from Module.UI.animation_manager import animation_manager
from Module.UI.theme_manager import theme_manager
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
except ImportError:
    Image = ImageTk = ImageDraw = ImageFont = None


class ModernStartingPage:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_ui()
        self.setup_animations()

    def setup_window(self):
        """Setup main window properties"""
        self.root.title("Image to PDF Converter - Welcome")
        self.root.geometry("1000x700")
        self.root.configure(bg=theme_manager.get_color("bg_primary"))

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")

        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Bind theme toggle
        self.root.bind("<Control-t>", self.toggle_theme)

    def create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_frame = tk.Frame(
            self.root, **theme_manager.get_frame_style("primary"))
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Left sidebar
        self.create_sidebar()

        # Main content area
        self.create_main_content()

        # Footer
        self.create_footer()

    def create_sidebar(self):
        """Create left sidebar with navigation"""
        colors = theme_manager.get_theme_colors()

        sidebar_frame = tk.Frame(self.main_frame,
                                 bg=colors["bg_secondary"],
                                 width=250)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
        sidebar_frame.grid_propagate(False)

        # Logo area
        logo_frame = tk.Frame(
            sidebar_frame, bg=colors["bg_secondary"], height=100)
        logo_frame.pack(fill="x", padx=20, pady=20)

        # Create app icon
        try:
            if icon_manager:
                icon_img = icon_manager.create_pdf_icon(
                    (48, 48), colors["primary"])
                if Image:
                    self.app_icon = ImageTk.PhotoImage(icon_img)
                    icon_label = tk.Label(logo_frame, image=self.app_icon,
                                          bg=colors["bg_secondary"])
                    icon_label.pack()
        except:
            pass

        # App name
        app_name = tk.Label(logo_frame, text="PDF Converter",
                            **theme_manager.get_label_style("title"),
                            bg=colors["bg_secondary"])
        app_name.pack(pady=(10, 0))

        # Navigation menu
        nav_frame = tk.Frame(sidebar_frame, bg=colors["bg_secondary"])
        nav_frame.pack(fill="both", expand=True, padx=20)

        # Menu items
        menu_items = [
            ("🏠 Home", self.show_home),
            ("📁 Convert Images", self.open_converter),
            ("⚙️ Settings", self.show_settings),
            ("❓ Help", self.show_help),
            ("🌙 Toggle Theme", self.toggle_theme)
        ]

        for text, command in menu_items:
            btn = tk.Button(nav_frame, text=text, command=command,
                            **theme_manager.get_button_style("secondary"),
                            anchor="w", pady=12, font=("Segoe UI", 11))
            btn.pack(fill="x", pady=2)

            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind("<Leave>", lambda e,
                     b=btn: self.on_button_hover(b, False))

    def create_main_content(self):
        """Create main content area"""
        colors = theme_manager.get_theme_colors()

        content_frame = tk.Frame(
            self.main_frame, **theme_manager.get_frame_style("primary"))
        content_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # Header
        header_frame = tk.Frame(
            content_frame, **theme_manager.get_frame_style("primary"))
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))

        # Welcome title
        welcome_title = tk.Label(header_frame, text="Welcome to Image to PDF Converter",
                                 **theme_manager.get_label_style("title"),
                                 font=("Segoe UI", 24, "bold"))
        welcome_title.pack(anchor="w")

        # Subtitle
        subtitle = tk.Label(header_frame,
                            text="Transform your images into professional PDF documents with ease",
                            **theme_manager.get_label_style("secondary"),
                            font=("Segoe UI", 14))
        subtitle.pack(anchor="w", pady=(5, 0))

        # Features grid
        features_frame = tk.Frame(
            content_frame, **theme_manager.get_frame_style("primary"))
        features_frame.grid(row=1, column=0, sticky="nsew")
        features_frame.grid_columnconfigure((0, 1, 2), weight=1)
        features_frame.grid_rowconfigure((0, 1), weight=1)

        # Create feature cards
        features = [
            {
                "title": "Batch Processing",
                "desc": "Convert multiple images at once with intelligent sorting and organization",
                "icon": "📁",
                "color": colors["primary"]
            },
            {
                "title": "Watermark Support",
                "desc": "Add custom watermarks to protect your documents and maintain branding",
                "icon": "🏷️",
                "color": colors["warning"]
            },
            {
                "title": "High Quality",
                "desc": "Maintain image quality with advanced compression and optimization",
                "icon": "⭐",
                "color": colors["success"]
            },
            {
                "title": "Drag & Drop",
                "desc": "Simply drag and drop your images for instant processing",
                "icon": "🎯",
                "color": colors["secondary"]
            },
            {
                "title": "Modern Interface",
                "desc": "Beautiful, responsive design with dark/light theme support",
                "icon": "🎨",
                "color": "#8b5cf6"
            },
            {
                "title": "Fast Export",
                "desc": "Quick PDF generation with customizable settings and preview",
                "icon": "⚡",
                "color": colors["danger"]
            }
        ]

        for i, feature in enumerate(features):
            row = i // 3
            col = i % 3
            self.create_feature_card(features_frame, feature, row, col)

        # Action buttons
        action_frame = tk.Frame(
            content_frame, **theme_manager.get_frame_style("primary"))
        action_frame.grid(row=2, column=0, sticky="ew", pady=(30, 0))

        # Primary action button
        start_btn = tk.Button(action_frame, text="🚀 Start Converting",
                              command=self.open_converter,
                              **theme_manager.get_button_style("primary"),
                              font=("Segoe UI", 14, "bold"),
                              pady=15, padx=30)
        start_btn.pack(side="left")

        # Secondary action button
        demo_btn = tk.Button(action_frame, text="📖 View Tutorial",
                             command=self.show_tutorial,
                             **theme_manager.get_button_style("secondary"),
                             font=("Segoe UI", 12),
                             pady=12, padx=25)
        demo_btn.pack(side="left", padx=(15, 0))

        # Add hover animations
        for btn in [start_btn, demo_btn]:
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind("<Leave>", lambda e,
                     b=btn: self.on_button_hover(b, False))

    def create_feature_card(self, parent, feature, row, col):
        """Create a feature card"""
        colors = theme_manager.get_theme_colors()

        # Card frame
        card = tk.Frame(parent, **theme_manager.get_frame_style("card"),
                        relief="solid", borderwidth=1)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Card content
        content = tk.Frame(card, **theme_manager.get_frame_style("secondary"))
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        icon_label = tk.Label(content, text=feature["icon"],
                              font=("Segoe UI", 32),
                              bg=colors["bg_secondary"],
                              fg=feature["color"])
        icon_label.pack(pady=(0, 10))

        # Title
        title_label = tk.Label(content, text=feature["title"],
                               **theme_manager.get_label_style("heading"),
                               bg=colors["bg_secondary"])
        title_label.pack()

        # Description
        desc_label = tk.Label(content, text=feature["desc"],
                              **theme_manager.get_label_style("secondary"),
                              bg=colors["bg_secondary"],
                              wraplength=200, justify="center")
        desc_label.pack(pady=(5, 0))

        # Add hover effect
        def on_card_enter(event):
            card.configure(
                highlightbackground=feature["color"], highlightthickness=2)
            if animation_manager:
                animation_manager.animate_scale(icon_label, 1.0, 1.1, 200)

        def on_card_leave(event):
            card.configure(
                highlightbackground=colors["border_light"], highlightthickness=1)
            if animation_manager:
                animation_manager.animate_scale(icon_label, 1.1, 1.0, 200)

        card.bind("<Enter>", on_card_enter)
        card.bind("<Leave>", on_card_leave)

        # Make card clickable
        for widget in [card, content, icon_label, title_label, desc_label]:
            widget.bind("<Button-1>", lambda e: self.open_converter())

    def create_footer(self):
        """Create footer with additional info"""
        colors = theme_manager.get_theme_colors()

        footer_frame = tk.Frame(self.main_frame,
                                bg=colors["bg_tertiary"],
                                height=60)
        footer_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        footer_frame.grid_propagate(False)

        # Footer content
        footer_content = tk.Frame(footer_frame, bg=colors["bg_tertiary"])
        footer_content.pack(expand=True, fill="both", padx=30, pady=15)

        # Left side - version info
        version_info = tk.Label(footer_content,
                                text="Version 2.0 Enhanced Edition • Built with ❤️ by Samarth Raut",
                                **theme_manager.get_label_style("secondary"),
                                bg=colors["bg_tertiary"],
                                font=("Segoe UI", 10))
        version_info.pack(side="left")

        # Right side - social links
        social_frame = tk.Frame(footer_content, bg=colors["bg_tertiary"])
        social_frame.pack(side="right")

        # Social buttons (simplified)
        social_buttons = ["📧", "🌐", "📱"]
        for emoji in social_buttons:
            btn = tk.Button(social_frame, text=emoji,
                            **theme_manager.get_button_style("secondary"),
                            width=3, height=1,
                            font=("Segoe UI", 12))
            btn.pack(side="right", padx=2)
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind("<Leave>", lambda e,
                     b=btn: self.on_button_hover(b, False))

    def setup_animations(self):
        """Setup initial animations"""
        if animation_manager:
            # Animate main content fade in
            self.root.after(
                100, lambda: animation_manager.animate_fade(self.main_frame))

    def on_button_hover(self, button, enter):
        """Handle button hover animation"""
        if animation_manager:
            animation_manager.animate_button_hover(button, enter)

    def toggle_theme(self, event=None):
        """Toggle between light and dark theme"""
        theme_manager.toggle_theme()
        self.refresh_ui()

        if animation_manager:
            animation_manager.animate_notification(
                self.root,
                f"Switched to {theme_manager.current_theme} theme",
                "success"
            )

    def refresh_ui(self):
        """Refresh UI with new theme"""
        # This would normally require recreating the UI
        # For now, just update the background
        self.root.configure(bg=theme_manager.get_color("bg_primary"))

    def open_converter(self):
        """Open the main converter application"""
        try:
            self.root.destroy()

            # Import the modern app
            from tkinterdnd2 import TkinterDnD
            from .ModernApp import ModernApp

            root = TkinterDnD.Tk()
            app = ModernApp(root)
            root.mainloop()
        except ImportError as e:
            if animation_manager:
                animation_manager.animate_notification(
                    self.root,
                    "Required dependencies not installed. Please install requirements.",
                    "error"
                )
        except Exception as e:
            if animation_manager:
                animation_manager.animate_notification(
                    self.root,
                    f"Error opening converter: {str(e)}",
                    "error"
                )

    def show_home(self):
        """Show home content"""
        if animation_manager:
            animation_manager.animate_notification(
                self.root, "Already on home page", "info")

    def show_settings(self):
        """Show settings dialog"""
        if animation_manager:
            animation_manager.animate_notification(
                self.root, "Settings panel coming soon!", "info")

    def show_help(self):
        """Show help dialog"""
        if animation_manager:
            animation_manager.animate_notification(
                self.root, "Help documentation coming soon!", "info")

    def show_tutorial(self):
        """Show tutorial"""
        if animation_manager:
            animation_manager.animate_notification(
                self.root, "Interactive tutorial coming soon!", "info")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernStartingPage(root)
    root.mainloop()
