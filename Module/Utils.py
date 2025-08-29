import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class ImageUtils:
    SUPPORTED_FORMATS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif'
    }

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        return Path(file_path).suffix.lower() in ImageUtils.SUPPORTED_FORMATS

    @staticmethod
    def filter_image_files(file_paths: List[str]) -> List[str]:
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
        import re
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        if len(safe_name) > 200:
            name, ext = os.path.splitext(safe_name)
            safe_name = name[:200-len(ext)] + ext
        return safe_name


class PDFUtils:
    PAGE_SIZES = {
        'A4': (595, 842),
        'Letter': (612, 792),
        'Legal': (612, 1008),
        'A3': (842, 1191),
        'A5': (420, 595)
    }

    @staticmethod
    def get_page_size(size_name: str) -> Tuple[int, int]:
        return PDFUtils.PAGE_SIZES.get(size_name, PDFUtils.PAGE_SIZES['A4'])


class FileUtils:
    @staticmethod
    def ensure_directory(directory_path: str) -> bool:
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def get_unique_filename(file_path: str) -> str:
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
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
