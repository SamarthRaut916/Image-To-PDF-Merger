import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
from pathlib import Path
from Module.Splashscreen import SplashScreen

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
from Module.SimpleImageToPDF import SimpleImageToPDF


def main():
   
    

 

    root = tk.Tk()
    splash = SplashScreen(root)
    root.mainloop()


    root = tk.Tk()
    app = SimpleImageToPDF(root)



    root.mainloop()


if __name__ == "__main__":
    main()
