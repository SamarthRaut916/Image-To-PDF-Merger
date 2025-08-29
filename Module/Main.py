import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import time


from Module.App import App
from Module.startingpage import StartingPage
from Module.Splashscreen import SplashScreen
def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.configure(background='#3498db')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = 800
        height = 400
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        label = tk.Label(self.root, text="Image to PDF Exporter", font=("Arial", 24), bg='#3498db', fg='white')
        label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        label = tk.Label(self.root, text="Developed by Samarth Raut \n email@gmail.com", font=("Arial", 16), bg='#3498db', fg='white')
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        progressbar = tk.Canvas(self.root, width=width-100, height=20, bg='#3498db', highlightthickness=0)
        progressbar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        progressbar.create_rectangle(0, 0, 0, 20, fill='white')

        for i in range(700):
            progressbar.delete("all")
            progressbar.create_rectangle(0, 0, i, 20, fill='white')
            self.root.update()
            time.sleep(0.00515)

        self.root.destroy()
        root = tk.Tk()
        app = StartingPage(root)

        app.open_app()
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreen(root)


