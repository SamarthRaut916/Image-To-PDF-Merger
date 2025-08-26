import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import time
from Module.App import App

class StartingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Exporter")
        self.root.geometry("400x300")

        label = tk.Label(self.root, text="Image to PDF Exporter", font=("Arial", 24))
        label.pack(pady=50)

        button = tk.Button(self.root, text="Open App", command=self.open_app)
        button.pack(pady=20)

    def open_app(self):
        self.root.destroy()
        root = TkinterDnD.Tk()
        app = App(root)
        root.mainloop() 
