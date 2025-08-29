import tkinter as tk
from tkinter import ttk
import threading
import time
from Module.App import App

try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.setup_splash()
        self.start_loading()

    def setup_splash(self):
        self.splash = tk.Toplevel()
        self.splash.overrideredirect(True)
        self.splash.configure(bg='#2C3E50')

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()

        width, height = 600, 350
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.splash.geometry(f'{width}x{height}+{x}+{y}')

        main_frame = tk.Frame(self.splash, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=30)

        title_label = tk.Label(
            main_frame,
            text="Image to PDF Converter",
            font=("Arial", 28, "bold"),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        title_label.pack(pady=(40, 10))

        subtitle_label = tk.Label(
            main_frame,
            text="Professional Grade Application",
            font=("Arial", 14),
            bg='#2C3E50',
            fg='#BDC3C7'
        )
        subtitle_label.pack(pady=(0, 30))

        dev_label = tk.Label(
            main_frame,
            text="Developed by Samarth Raut",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='#95A5A6'
        )
        dev_label.pack(pady=(0, 40))

        self.progress = ttk.Progressbar(
            main_frame,
            length=400,
            mode='determinate',
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress.pack(pady=(0, 20))

        self.status_label = tk.Label(
            main_frame,
            text="Initializing...",
            font=("Arial", 10),
            bg='#2C3E50',
            fg='#7F8C8D'
        )
        self.status_label.pack()

        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#34495E',
            background='#3498DB',
            lightcolor='#3498DB',
            darkcolor='#2980B9'
        )

    def start_loading(self):
        threading.Thread(target=self.loading_process, daemon=True).start()

    def loading_process(self):
        steps = [
            ("Initializing application...", 20),
            ("Loading modules...", 40),
            ("Setting up UI components...", 60),
            ("Configuring settings...", 80),
            ("Finalizing setup...", 100)
        ]

        for status, progress_val in steps:
            self.splash.after(0, lambda s=status,
                              p=progress_val: self.update_progress(s, p))
            time.sleep(0.8)

        self.splash.after(500, self.launch_main_app)

    def update_progress(self, status, value):
        self.status_label.config(text=status)
        self.progress['value'] = value
        self.splash.update()

    def launch_main_app(self):
        self.splash.destroy()
        self.root.destroy()

        # if DND_AVAILABLE:
        #     main_root = TkinterDnD.Tk()
        # else:
        #     main_root = tk.Tk()
        # app = App(main_root)
        # main_root.mainloop()
