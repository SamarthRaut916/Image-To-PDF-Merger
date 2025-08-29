"""
Modern Theme Manager for Image to PDF Converter
Provides light and dark themes with smooth transitions
"""


class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                # Main colors
                "bg_primary": "#ffffff",
                "bg_secondary": "#f8fafc",
                "bg_tertiary": "#f1f5f9",
                "bg_accent": "#e2e8f0",

                # Text colors
                "text_primary": "#1e293b",
                "text_secondary": "#64748b",
                "text_muted": "#94a3b8",

                # Action colors
                "primary": "#2563eb",
                "primary_hover": "#1d4ed8",
                "secondary": "#64748b",
                "secondary_hover": "#475569",
                "success": "#10b981",
                "success_hover": "#059669",
                "warning": "#f59e0b",
                "warning_hover": "#d97706",
                "danger": "#ef4444",
                "danger_hover": "#dc2626",

                # Border colors
                "border_light": "#e2e8f0",
                "border_medium": "#cbd5e1",
                "border_dark": "#94a3b8",

                # Special
                "shadow": "rgba(0, 0, 0, 0.1)",
                "shadow_hover": "rgba(0, 0, 0, 0.15)",
                "overlay": "rgba(0, 0, 0, 0.5)",

                # Gradients
                "gradient_primary": "#2563eb to #3b82f6",
                "gradient_secondary": "#64748b to #475569",
            },

            "dark": {
                # Main colors
                "bg_primary": "#0f172a",
                "bg_secondary": "#1e293b",
                "bg_tertiary": "#334155",
                "bg_accent": "#475569",

                # Text colors
                "text_primary": "#f8fafc",
                "text_secondary": "#cbd5e1",
                "text_muted": "#94a3b8",

                # Action colors
                "primary": "#3b82f6",
                "primary_hover": "#2563eb",
                "secondary": "#64748b",
                "secondary_hover": "#475569",
                "success": "#10b981",
                "success_hover": "#059669",
                "warning": "#f59e0b",
                "warning_hover": "#d97706",
                "danger": "#ef4444",
                "danger_hover": "#dc2626",

                # Border colors
                "border_light": "#334155",
                "border_medium": "#475569",
                "border_dark": "#64748b",

                # Special
                "shadow": "rgba(0, 0, 0, 0.3)",
                "shadow_hover": "rgba(0, 0, 0, 0.4)",
                "overlay": "rgba(0, 0, 0, 0.7)",

                # Gradients
                "gradient_primary": "#3b82f6 to #2563eb",
                "gradient_secondary": "#64748b to #475569",
            }
        }

        # Animation settings
        self.animation_duration = 200  # milliseconds
        self.easing = "ease-in-out"

    def get_color(self, color_name):
        """Get color value for current theme"""
        return self.themes[self.current_theme].get(color_name, "#000000")

    def get_theme_colors(self):
        """Get all colors for current theme"""
        return self.themes[self.current_theme].copy()

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        return self.current_theme

    def set_theme(self, theme_name):
        """Set specific theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False

    def is_dark_theme(self):
        """Check if current theme is dark"""
        return self.current_theme == "dark"

    def get_button_style(self, variant="primary", state="normal"):
        """Get button styling for current theme"""
        colors = self.get_theme_colors()

        styles = {
            "primary": {
                "normal": {
                    "bg": colors["primary"],
                    "fg": "#ffffff",
                    "border": colors["primary"],
                    "activebackground": colors["primary_hover"],
                    "relief": "flat",
                    "borderwidth": 0,
                    "cursor": "hand2"
                },
                "hover": {
                    "bg": colors["primary_hover"],
                }
            },
            "secondary": {
                "normal": {
                    "bg": colors["bg_secondary"],
                    "fg": colors["text_primary"],
                    "border": colors["border_medium"],
                    "activebackground": colors["bg_tertiary"],
                    "relief": "solid",
                    "borderwidth": 1,
                    "cursor": "hand2"
                }
            },
            "success": {
                "normal": {
                    "bg": colors["success"],
                    "fg": "#ffffff",
                    "border": colors["success"],
                    "activebackground": colors["success_hover"],
                    "relief": "flat",
                    "borderwidth": 0,
                    "cursor": "hand2"
                }
            },
            "danger": {
                "normal": {
                    "bg": colors["danger"],
                    "fg": "#ffffff",
                    "border": colors["danger"],
                    "activebackground": colors["danger_hover"],
                    "relief": "flat",
                    "borderwidth": 0,
                    "cursor": "hand2"
                }
            }
        }

        return styles.get(variant, {}).get(state, styles["primary"]["normal"])

    def get_frame_style(self, variant="primary"):
        """Get frame styling for current theme"""
        colors = self.get_theme_colors()

        styles = {
            "primary": {
                "bg": colors["bg_primary"],
                "relief": "flat",
                "borderwidth": 0
            },
            "secondary": {
                "bg": colors["bg_secondary"],
                "relief": "flat",
                "borderwidth": 0
            },
            "card": {
                "bg": colors["bg_secondary"],
                "relief": "solid",
                "borderwidth": 1,
                "highlightbackground": colors["border_light"],
                "highlightthickness": 1
            }
        }

        return styles.get(variant, styles["primary"])

    def get_label_style(self, variant="primary"):
        """Get label styling for current theme"""
        colors = self.get_theme_colors()

        styles = {
            "primary": {
                "bg": colors["bg_primary"],
                "fg": colors["text_primary"],
                "font": ("Segoe UI", 10)
            },
            "secondary": {
                "bg": colors["bg_secondary"],
                "fg": colors["text_secondary"],
                "font": ("Segoe UI", 9)
            },
            "title": {
                "bg": colors["bg_primary"],
                "fg": colors["text_primary"],
                "font": ("Segoe UI", 14, "bold")
            },
            "heading": {
                "bg": colors["bg_primary"],
                "fg": colors["text_primary"],
                "font": ("Segoe UI", 12, "bold")
            }
        }

        return styles.get(variant, styles["primary"])

    def get_entry_style(self):
        """Get entry/input styling for current theme"""
        colors = self.get_theme_colors()

        return {
            "bg": colors["bg_primary"],
            "fg": colors["text_primary"],
            "insertbackground": colors["text_primary"],
            "selectbackground": colors["primary"],
            "selectforeground": "#ffffff",
            "relief": "solid",
            "borderwidth": 1,
            "highlightbackground": colors["border_medium"],
            "highlightcolor": colors["primary"],
            "highlightthickness": 1,
            "font": ("Segoe UI", 10)
        }

    def get_canvas_style(self):
        """Get canvas styling for current theme"""
        colors = self.get_theme_colors()

        return {
            "bg": colors["bg_secondary"],
            "highlightthickness": 0,
            "relief": "flat"
        }

    def get_scrollbar_style(self):
        """Get scrollbar styling for current theme"""
        colors = self.get_theme_colors()

        return {
            "bg": colors["bg_tertiary"],
            "troughcolor": colors["bg_secondary"],
            "activebackground": colors["border_dark"],
            "highlightthickness": 0,
            "relief": "flat",
            "borderwidth": 0,
            "width": 12
        }


# Global theme manager instance
theme_manager = ThemeManager()
