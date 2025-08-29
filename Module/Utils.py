"""
Utility Functions for Image to PDF Converter
Common utilities and helper functions
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class ImageUtils:
    """Utility class for image operations"""

    SUPPORTED_FORMATS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif'
    }

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """Check if file is a supported image format"""
        return Path(file_path).suffix.lower() in ImageUtils.SUPPORTED_FORMATS

    @staticmethod
    def filter_image_files(file_paths: List[str]) -> List[str]:
        """Filter list to only include image files"""
        return [path for path in file_paths if ImageUtils.is_image_file(path)]

    @staticmethod
    def get_image_info(image_path: str) -> Optional[dict]:
        """Get basic image information"""
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                return {
                    'path': image_path,
                    'filename': os.path.basename(image_path),
                    'size': img.size,
                    'format': img.format,
                    'mode': img.mode,
                    'file_size': os.path.getsize(image_path)
                }
        except Exception:
            return None

    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Get safe filename for filesystem"""
        import re
        # Remove invalid characters
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        if len(safe_name) > 200:
            name, ext = os.path.splitext(safe_name)
            safe_name = name[:200-len(ext)] + ext
        return safe_name


class PDFUtils:
    """Utility class for PDF operations"""

    PAGE_SIZES = {
        'A4': (595, 842),
        'Letter': (612, 792),
        'Legal': (612, 1008),
        'A3': (842, 1191),
        'A5': (420, 595)
    }

    @staticmethod
    def get_page_size(size_name: str) -> Tuple[int, int]:
        """Get page size in points"""
        return PDFUtils.PAGE_SIZES.get(size_name, PDFUtils.PAGE_SIZES['A4'])

    @staticmethod
    def calculate_image_position(image_size: Tuple[int, int],
                                 page_size: Tuple[int, int],
                                 margin: int = 50) -> Tuple[int, int, int, int]:
        """Calculate image position on page with margin"""
        img_width, img_height = image_size
        page_width, page_height = page_size

        # Available space
        available_width = page_width - (2 * margin)
        available_height = page_height - (2 * margin)

        # Calculate scale to fit
        scale_x = available_width / img_width
        scale_y = available_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale

        # New dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Center position
        x = margin + (available_width - new_width) // 2
        y = margin + (available_height - new_height) // 2

        return x, y, new_width, new_height


class FileUtils:
    """Utility class for file operations"""

    @staticmethod
    def ensure_directory(directory_path: str) -> bool:
        """Ensure directory exists, create if it doesn't"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def get_unique_filename(file_path: str) -> str:
        """Get unique filename by adding number suffix if file exists"""
        if not os.path.exists(file_path):
            return file_path

        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)

        counter = 1
        while True:
            new_filename = f"{name}_{counter}{ext}"
            new_path = os.path.join(directory, new_filename)
            if not os.path.exists(new_path):
                return new_path
            counter += 1

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    @staticmethod
    def open_file_location(file_path: str) -> bool:
        """Open file location in system file manager"""
        try:
            if sys.platform == "win32":
                os.startfile(os.path.dirname(file_path))
            elif sys.platform == "darwin":  # macOS
                os.system(f'open "{os.path.dirname(file_path)}"')
            else:  # Linux
                os.system(f'xdg-open "{os.path.dirname(file_path)}"')
            return True
        except Exception:
            return False


class ConfigManager:
    """Simple configuration manager"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> dict:
        """Load configuration from file"""
        try:
            import json
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass

        # Default configuration
        return {
            "theme": "light",
            "quality": 95,
            "page_size": "A4",
            "watermark": {
                "enabled": False,
                "text": "Samarth Raut",
                "position": "bottom-right",
                "opacity": 0.7
            },
            "ui": {
                "thumbnail_size": [150, 150],
                "preview_size": [250, 250],
                "view_mode": "grid",
                "auto_save": False
            },
            "recent_files": [],
            "last_export_path": ""
        }

    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            import json
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception:
            return False

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value) -> bool:
        """Set configuration value"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        return self.save_config()

    def add_recent_file(self, file_path: str) -> bool:
        """Add file to recent files list"""
        recent = self.get("recent_files", [])

        # Remove if already exists
        if file_path in recent:
            recent.remove(file_path)

        # Add to beginning
        recent.insert(0, file_path)

        # Keep only last 10
        recent = recent[:10]

        return self.set("recent_files", recent)


class ColorUtils:
    """Utility class for color operations"""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    @staticmethod
    def adjust_brightness(hex_color: str, factor: float) -> str:
        """Adjust color brightness by factor (0.0 to 2.0)"""
        r, g, b = ColorUtils.hex_to_rgb(hex_color)

        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))

        return ColorUtils.rgb_to_hex((r, g, b))

    @staticmethod
    def blend_colors(color1: str, color2: str, ratio: float = 0.5) -> str:
        """Blend two colors with given ratio"""
        r1, g1, b1 = ColorUtils.hex_to_rgb(color1)
        r2, g2, b2 = ColorUtils.hex_to_rgb(color2)

        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)

        return ColorUtils.rgb_to_hex((r, g, b))


class ValidationUtils:
    """Utility class for input validation"""

    @staticmethod
    def is_valid_watermark_text(text: str) -> bool:
        """Check if watermark text is valid"""
        if not text or not text.strip():
            return False

        # Check length
        if len(text.strip()) > 100:
            return False

        # Check for invalid characters (basic check)
        invalid_chars = ['<', '>', '|', '\\0']
        return not any(char in text for char in invalid_chars)

    @staticmethod
    def is_valid_quality(quality: int) -> bool:
        """Check if quality value is valid"""
        return 1 <= quality <= 100

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe use"""
        import re
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        filename = filename.strip('. ')
        # Ensure not empty
        if not filename:
            filename = "untitled"
        return filename


# Global configuration instance
config_manager = ConfigManager()
