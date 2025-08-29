"""
Modern Animation System for Image to PDF Converter
Provides smooth animations and transitions
"""

import tkinter as tk
import threading
import time
import math


class AnimationManager:
    def __init__(self):
        self.active_animations = {}
        self.animation_id = 0

    def generate_animation_id(self):
        """Generate unique animation ID"""
        self.animation_id += 1
        return self.animation_id

    def ease_in_out_cubic(self, t):
        """Cubic ease-in-out easing function"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    def ease_out_bounce(self, t):
        """Bounce ease-out easing function"""
        n1 = 7.5625
        d1 = 2.75

        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            return n1 * (t - 1.5 / d1) * t + 0.75
        elif t < 2.5 / d1:
            return n1 * (t - 2.25 / d1) * t + 0.9375
        else:
            return n1 * (t - 2.625 / d1) * t + 0.984375

    def animate_fade(self, widget, start_alpha=0, end_alpha=1, duration=500, callback=None):
        """Animate widget fade in/out"""
        animation_id = self.generate_animation_id()
        steps = 30
        step_duration = duration / steps
        alpha_step = (end_alpha - start_alpha) / steps

        def animate_step(step):
            if animation_id not in self.active_animations:
                return

            if step <= steps:
                progress = step / steps
                eased_progress = self.ease_in_out_cubic(progress)
                current_alpha = start_alpha + \
                    (end_alpha - start_alpha) * eased_progress

                try:
                    # Simulate alpha by adjusting widget state
                    if hasattr(widget, 'config'):
                        if current_alpha < 0.1:
                            widget.config(state='disabled')
                        else:
                            widget.config(state='normal')
                except:
                    pass

                widget.after(int(step_duration),
                             lambda: animate_step(step + 1))
            else:
                self.active_animations.pop(animation_id, None)
                if callback:
                    callback()

        self.active_animations[animation_id] = True
        animate_step(0)
        return animation_id

    def animate_slide(self, widget, start_x=None, end_x=None, start_y=None, end_y=None,
                      duration=300, callback=None):
        """Animate widget sliding"""
        animation_id = self.generate_animation_id()
        steps = 30
        step_duration = duration / steps

        # Get current position if not specified
        if start_x is None:
            start_x = widget.winfo_x()
        if start_y is None:
            start_y = widget.winfo_y()
        if end_x is None:
            end_x = start_x
        if end_y is None:
            end_y = start_y

        x_step = (end_x - start_x) / steps
        y_step = (end_y - start_y) / steps

        def animate_step(step):
            if animation_id not in self.active_animations:
                return

            if step <= steps:
                progress = step / steps
                eased_progress = self.ease_in_out_cubic(progress)

                current_x = start_x + (end_x - start_x) * eased_progress
                current_y = start_y + (end_y - start_y) * eased_progress

                try:
                    widget.place(x=current_x, y=current_y)
                except:
                    pass

                widget.after(int(step_duration),
                             lambda: animate_step(step + 1))
            else:
                self.active_animations.pop(animation_id, None)
                if callback:
                    callback()

        self.active_animations[animation_id] = True
        animate_step(0)
        return animation_id

    def animate_scale(self, widget, start_scale=1.0, end_scale=1.2, duration=200, callback=None):
        """Animate widget scaling (simulated)"""
        animation_id = self.generate_animation_id()
        steps = 20
        step_duration = duration / steps

        original_font = None
        if hasattr(widget, 'cget'):
            try:
                original_font = widget.cget('font')
                if isinstance(original_font, str):
                    original_font = (original_font, 10)
                elif isinstance(original_font, tuple) and len(original_font) >= 2:
                    pass
                else:
                    original_font = ('Arial', 10)
            except:
                original_font = ('Arial', 10)

        def animate_step(step):
            if animation_id not in self.active_animations:
                return

            if step <= steps:
                progress = step / steps
                eased_progress = self.ease_out_bounce(progress)
                current_scale = start_scale + \
                    (end_scale - start_scale) * eased_progress

                try:
                    if original_font and hasattr(widget, 'config'):
                        new_size = int(original_font[1] * current_scale)
                        new_font = (original_font[0], new_size)
                        widget.config(font=new_font)
                except:
                    pass

                widget.after(int(step_duration),
                             lambda: animate_step(step + 1))
            else:
                # Reset to original
                try:
                    if original_font and hasattr(widget, 'config'):
                        widget.config(font=original_font)
                except:
                    pass

                self.active_animations.pop(animation_id, None)
                if callback:
                    callback()

        self.active_animations[animation_id] = True
        animate_step(0)
        return animation_id

    def animate_progress_bar(self, canvas, width, height, duration=1000, color="#2563eb"):
        """Animate a progress bar"""
        animation_id = self.generate_animation_id()
        steps = 60
        step_duration = duration / steps

        # Clear canvas
        canvas.delete("all")

        # Background
        canvas.create_rectangle(0, 0, width, height,
                                fill="#e2e8f0", outline="")

        def animate_step(step):
            if animation_id not in self.active_animations:
                return

            if step <= steps:
                progress = step / steps
                current_width = width * progress

                # Clear previous progress
                canvas.delete("progress")

                # Draw current progress
                canvas.create_rectangle(0, 0, current_width, height,
                                        fill=color, outline="", tags="progress")

                canvas.after(int(step_duration),
                             lambda: animate_step(step + 1))
            else:
                self.active_animations.pop(animation_id, None)

        self.active_animations[animation_id] = True
        animate_step(0)
        return animation_id

    def animate_button_hover(self, button, enter=True):
        """Animate button hover effect"""
        if enter:
            self.animate_scale(button, 1.0, 1.05, 150)
        else:
            self.animate_scale(button, 1.05, 1.0, 150)

    def animate_notification(self, parent, message, notification_type="info", duration=3000):
        """Show animated notification"""
        from .theme_manager import theme_manager

        colors = theme_manager.get_theme_colors()

        # Color based on type
        type_colors = {
            "info": colors["primary"],
            "success": colors["success"],
            "warning": colors["warning"],
            "error": colors["danger"]
        }

        bg_color = type_colors.get(notification_type, colors["primary"])

        # Create notification frame
        notification = tk.Frame(parent, bg=bg_color,
                                relief="solid", borderwidth=1)

        label = tk.Label(notification, text=message, bg=bg_color, fg="white",
                         font=("Segoe UI", 10), padx=20, pady=10)
        label.pack()

        # Position at top center
        notification.place(relx=0.5, y=-50, anchor="n")

        # Animate slide down
        def show_notification():
            self.animate_slide(notification, end_y=20, duration=300,
                               callback=lambda: hide_after_delay())

        def hide_after_delay():
            parent.after(duration, hide_notification)

        def hide_notification():
            self.animate_slide(notification, start_y=20, end_y=-50, duration=300,
                               callback=lambda: notification.destroy())

        show_notification()

    def stop_animation(self, animation_id):
        """Stop specific animation"""
        self.active_animations.pop(animation_id, None)

    def stop_all_animations(self):
        """Stop all active animations"""
        self.active_animations.clear()


# Global animation manager instance
animation_manager = AnimationManager()
