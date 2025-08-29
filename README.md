# Image to PDF Converter - Professional Edition

A clean, production-ready desktop application for converting images to PDF format with professional features.

## Features

- **Modern Splash Screen** - Professional loading experience
- **Drag & Drop Support** - Drop images directly into the application (when tkinterdnd2 is available)
- **Image Selection** - Browse and select multiple images at once
- **Live Preview** - See selected images with thumbnails
- **Watermark Support** - Add custom watermarks to your PDFs
- **Multiple Formats** - Supports PNG, JPG, JPEG, GIF, BMP, TIFF
- **Production Ready** - Clean code, no debug prints, optimized performance

## Requirements

- Python 3.7+
- Pillow (PIL)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```cmd
python app.py
```

### Application Flow:
1. **Splash Screen** - Shows loading progress
2. **Main Application** - Three-panel interface:
   - **Left Panel**: Import and view image thumbnails
   - **Center Panel**: Quick add button
   - **Right Panel**: Selected images preview and PDF settings

### Features:
- Import images using the "Import Images" button
- Check/uncheck images to include/exclude from PDF
- Add custom watermark text
- Save selected images as PDF

## File Structure

```
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── Module/
│   ├── Splashscreen.py   # Professional splash screen
│   ├── App.py           # Main application logic
│   └── Utils.py         # Utility functions
└── README.md            # This file
```

## Technical Details

- **Framework**: Tkinter (built-in Python GUI)
- **Image Processing**: Pillow (PIL)
- **Architecture**: Modular design with clean separation
- **Compatibility**: Windows, macOS, Linux

## Developer

Developed by **Samarth Raut**

## License

This project is for demonstration and educational purposes.
