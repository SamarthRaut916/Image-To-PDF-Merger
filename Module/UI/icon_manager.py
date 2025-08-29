"""
Modern Icon Manager for Image to PDF Converter
Creates SVG-based icons programmatically for a modern look
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64


class IconManager:
    def __init__(self):
        self.icon_size = (24, 24)
        self.large_icon_size = (48, 48)
        self.color_primary = "#2563eb"
        self.color_secondary = "#64748b"
        self.color_success = "#10b981"
        self.color_danger = "#ef4444"
        self.color_warning = "#f59e0b"

    def create_add_icon(self, size=(24, 24), color="#2563eb"):
        """Create a modern add/plus icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = size[0] // 2, size[1] // 2
        thickness = max(2, size[0] // 12)
        length = size[0] // 3

        # Draw plus sign
        draw.rectangle([center_x - thickness//2, center_y - length,
                       center_x + thickness//2, center_y + length], fill=color)
        draw.rectangle([center_x - length, center_y - thickness//2,
                       center_x + length, center_y + thickness//2], fill=color)

        # Draw circle border
        border_width = 2
        draw.ellipse([border_width, border_width, size[0]-border_width, size[1]-border_width],
                     outline=color, width=border_width)

        return img

    def create_folder_icon(self, size=(24, 24), color="#2563eb"):
        """Create a modern folder icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Main folder body
        folder_rect = [2, size[1]//3, size[0]-2, size[1]-2]
        draw.rounded_rectangle(folder_rect, radius=2, fill=color, width=0)

        # Folder tab
        tab_rect = [2, size[1]//4, size[0]//2, size[1]//3 + 2]
        draw.rounded_rectangle(tab_rect, radius=2, fill=color, width=0)

        return img

    def create_pdf_icon(self, size=(24, 24), color="#ef4444"):
        """Create a modern PDF icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Document body
        doc_rect = [3, 2, size[0]-3, size[1]-2]
        draw.rounded_rectangle(doc_rect, radius=2, fill=color, width=0)

        # PDF text (simplified)
        try:
            font = ImageFont.truetype("arial.ttf", max(8, size[0]//4))
        except:
            font = ImageFont.load_default()

        text = "PDF"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2

        draw.text((text_x, text_y), text, fill="white", font=font)

        return img

    def create_image_icon(self, size=(24, 24), color="#10b981"):
        """Create a modern image icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Image frame
        frame_rect = [2, 2, size[0]-2, size[1]-2]
        draw.rounded_rectangle(frame_rect, radius=2, outline=color, width=2)

        # Mountain shape (simple triangle)
        mountain_points = [
            (size[0]//4, size[1]*3//4),
            (size[0]//2, size[1]//2),
            (size[0]*3//4, size[1]*3//4)
        ]
        draw.polygon(mountain_points, fill=color)

        # Sun (circle)
        sun_radius = size[0]//8
        sun_center = (size[0]*3//4, size[1]//3)
        sun_bbox = [
            sun_center[0] - sun_radius, sun_center[1] - sun_radius,
            sun_center[0] + sun_radius, sun_center[1] + sun_radius
        ]
        draw.ellipse(sun_bbox, fill=color)

        return img

    def create_settings_icon(self, size=(24, 24), color="#64748b"):
        """Create a modern settings/gear icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = size[0] // 2, size[1] // 2
        outer_radius = size[0] // 3
        inner_radius = size[0] // 6

        # Draw gear teeth (simplified as circle with notches)
        draw.ellipse([center_x - outer_radius, center_y - outer_radius,
                     center_x + outer_radius, center_y + outer_radius], fill=color)

        # Inner circle (hole)
        draw.ellipse([center_x - inner_radius, center_y - inner_radius,
                     center_x + inner_radius, center_y + inner_radius], fill=(0, 0, 0, 0))

        return img

    def create_watermark_icon(self, size=(24, 24), color="#f59e0b"):
        """Create a watermark icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Water drop shape
        center_x, center_y = size[0] // 2, size[1] // 2

        # Drop body (ellipse)
        drop_rect = [center_x - size[0]//4, center_y - size[1]//4,
                     center_x + size[0]//4, center_y + size[1]//3]
        draw.ellipse(drop_rect, fill=color)

        # Drop tip (triangle)
        tip_points = [
            (center_x, center_y - size[1]//3),
            (center_x - size[0]//6, center_y - size[1]//4),
            (center_x + size[0]//6, center_y - size[1]//4)
        ]
        draw.polygon(tip_points, fill=color)

        return img

    def create_save_icon(self, size=(24, 24), color="#10b981"):
        """Create a modern save icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Disk outline
        disk_rect = [2, 2, size[0]-2, size[1]-2]
        draw.rounded_rectangle(disk_rect, radius=2, outline=color, width=2)

        # Save slot
        slot_rect = [size[0]//4, 3, size[0]*3//4, size[1]//3]
        draw.rectangle(slot_rect, fill=color)

        # Bottom section
        bottom_rect = [4, size[1]*2//3, size[0]-4, size[1]-4]
        draw.rectangle(bottom_rect, fill=color)

        return img

    def create_theme_icon(self, size=(24, 24), color="#8b5cf6"):
        """Create a theme toggle icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = size[0] // 2, size[1] // 2
        radius = size[0] // 3

        # Half moon shape for theme toggle
        # Full circle
        circle_bbox = [center_x - radius, center_y - radius,
                       center_x + radius, center_y + radius]
        draw.ellipse(circle_bbox, fill=color)

        # Cut out part to make crescent
        cut_bbox = [center_x - radius//2, center_y - radius,
                    center_x + radius, center_y + radius]
        draw.ellipse(cut_bbox, fill=(0, 0, 0, 0))

        return img

    def create_delete_icon(self, size=(24, 24), color="#ef4444"):
        """Create a delete/trash icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Trash can body
        body_rect = [size[0]//4, size[1]//3, size[0]*3//4, size[1]-3]
        draw.rounded_rectangle(body_rect, radius=2, outline=color, width=2)

        # Trash can lid
        lid_rect = [size[0]//5, size[1]//4, size[0]*4//5, size[1]//3]
        draw.rectangle(lid_rect, fill=color)

        # Handle
        handle_rect = [size[0]*2//5, size[1]//6, size[0]*3//5, size[1]//4]
        draw.rounded_rectangle(handle_rect, radius=1, outline=color, width=1)

        return img

    def create_preview_icon(self, size=(24, 24), color="#6366f1"):
        """Create a preview/eye icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = size[0] // 2, size[1] // 2

        # Eye outline (ellipse)
        eye_rect = [3, center_y - size[1]//4, size[0]-3, center_y + size[1]//4]
        draw.ellipse(eye_rect, outline=color, width=2)

        # Pupil
        pupil_radius = size[0] // 8
        pupil_rect = [center_x - pupil_radius, center_y - pupil_radius,
                      center_x + pupil_radius, center_y + pupil_radius]
        draw.ellipse(pupil_rect, fill=color)

        return img

    def get_icon(self, icon_name, size=(24, 24), color=None):
        """Get icon by name"""
        if color is None:
            color = self.color_primary

        icon_methods = {
            'add': self.create_add_icon,
            'folder': self.create_folder_icon,
            'pdf': self.create_pdf_icon,
            'image': self.create_image_icon,
            'settings': self.create_settings_icon,
            'watermark': self.create_watermark_icon,
            'save': self.create_save_icon,
            'theme': self.create_theme_icon,
            'delete': self.create_delete_icon,
            'preview': self.create_preview_icon
        }

        if icon_name in icon_methods:
            return icon_methods[icon_name](size, color)
        else:
            # Return a default icon
            return self.create_add_icon(size, color)


# Global icon manager instance
icon_manager = IconManager()
