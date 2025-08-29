"""
Modern Main Application for Image to PDF Converter
Enhanced with modern UI, animations, and better user experience
"""

from Module.UI.icon_manager import icon_manager
from Module.UI.animation_manager import animation_manager
from Module.UI.theme_manager import theme_manager
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import threading
from typing import List, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    from tkinterdnd2 import TkinterDnD, DND_FILES
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = ImageTk = ImageDraw = ImageFont = None
    TkinterDnD = DND_FILES = None


class ModernApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.init_variables()
        self.create_ui()
        self.setup_drag_drop()
        self.setup_bindings()

    def setup_window(self):
        """Setup main window properties"""
        self.root.title("Image to PDF Converter - Enhanced Edition")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Start maximized
        self.root.configure(bg=theme_manager.get_color("bg_primary"))

        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Window icon
        try:
            if icon_manager and PIL_AVAILABLE:
                icon_img = icon_manager.create_pdf_icon((32, 32))
                self.window_icon = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, self.window_icon)
        except:
            pass

    def init_variables(self):
        """Initialize application variables"""
        self.selected_images: List[str] = []
        self.image_thumbnails = []
        self.selected_image_vars = []
        self.right_panel_widgets = {}
        self.resized_images_for_pdf = {}

        # Tkinter variables
        self.image_count_var = tk.StringVar(value="No images selected")
        self.apply_watermark = tk.BooleanVar(value=False)
        self.watermark_text_var = tk.StringVar(value="Samarth Raut")
        self.current_view = tk.StringVar(value="grid")  # grid or list

        # Settings
        self.settings = {
            "thumbnail_size": (150, 150),
            "preview_size": (250, 250),
            "quality": 95,
            "auto_save": False,
            "default_watermark": "Samarth Raut"
        }

    def create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_container = tk.Frame(
            self.root, **theme_manager.get_frame_style("primary"))
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Create sections
        self.create_header()
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()

    def create_header(self):
        """Create application header"""
        colors = theme_manager.get_theme_colors()

        header_frame = tk.Frame(self.main_container,
                               bg=colors["bg_secondary"],
                               height=80)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # Left side - Logo and title
        left_frame = tk.Frame(header_frame, bg=colors["bg_secondary"])
        left_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # App icon
        try:
            if icon_manager and PIL_AVAILABLE:
                icon_img = icon_manager.create_pdf_icon(
                    (48, 48), colors["primary"])
                self.header_icon = ImageTk.PhotoImage(icon_img)
                icon_label = tk.Label(left_frame, image=self.header_icon,
                                    bg=colors["bg_secondary"])
                icon_label.pack(side="left", padx=(0, 15))
        except:
            pass

        # Title
        title_frame = tk.Frame(left_frame, bg=colors["bg_secondary"])
        title_frame.pack(side="left")

        title_label = tk.Label(title_frame, text="Image to PDF Converter",
                              **theme_manager.get_label_style("title"),
                              bg=colors["bg_secondary"],
                              font=("Segoe UI", 18, "bold"))
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(title_frame, text="Enhanced Edition v2.0",
                                 **theme_manager.get_label_style("secondary"),
                                 bg=colors["bg_secondary"],
                                 font=("Segoe UI", 11))
        subtitle_label.pack(anchor="w")

        # Center - Image counter
        center_frame = tk.Frame(header_frame, bg=colors["bg_secondary"])
        center_frame.grid(row=0, column=1, pady=15)

        self.counter_label = tk.Label(center_frame, textvariable=self.image_count_var,
                                     **theme_manager.get_label_style("heading"),
                                     bg=colors["bg_secondary"],
                                     font=("Segoe UI", 14, "bold"))
        self.counter_label.pack()

        # Right side - Theme toggle and settings
        right_frame = tk.Frame(header_frame, bg=colors["bg_secondary"])
        right_frame.grid(row=0, column=2, sticky="e", padx=20, pady=15)

        # Theme toggle button
        theme_btn = tk.Button(right_frame, text="🌙",
                             command=self.toggle_theme,
                             **theme_manager.get_button_style("secondary"),
                             font=("Segoe UI", 16), width=3)
        theme_btn.pack(side="right", padx=5)

        # Settings button
        settings_btn = tk.Button(right_frame, text="⚙️",
                                command=self.show_settings,
                                **theme_manager.get_button_style("secondary"),
                                font=("Segoe UI", 16), width=3)
        settings_btn.pack(side="right", padx=5)

        # Add hover effects
        for btn in [theme_btn, settings_btn]:
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind("<Leave>", lambda e,
                     b=btn: self.on_button_hover(b, False))

    def create_toolbar(self):
        """Create toolbar with action buttons"""
        colors = theme_manager.get_theme_colors()

        toolbar_frame = tk.Frame(self.main_container,
                                bg=colors["bg_tertiary"],
                                height=60)
        toolbar_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        toolbar_frame.grid_propagate(False)

        # Toolbar content
        toolbar_content = tk.Frame(toolbar_frame, bg=colors["bg_tertiary"])
        toolbar_content.pack(expand=True, fill="both", padx=20, pady=10)

        # Left side - Main actions
        left_toolbar = tk.Frame(toolbar_content, bg=colors["bg_tertiary"])
        left_toolbar.pack(side="left")

        # Import button
        import_btn = tk.Button(left_toolbar, text="📁 Import Images",
                              command=self.import_images,
                              **theme_manager.get_button_style("primary"),
                              font=("Segoe UI", 11, "bold"),
                              padx=20, pady=8)
        import_btn.pack(side="left", padx=(0, 10))

        # Clear all button
        clear_btn = tk.Button(left_toolbar, text="🗑️ Clear All",
                             command=self.clear_all_images,
                             **theme_manager.get_button_style("danger"),
                             font=("Segoe UI", 11),
                             padx=15, pady=8)
        clear_btn.pack(side="left", padx=5)

        # Right side - View controls and export
        right_toolbar = tk.Frame(toolbar_content, bg=colors["bg_tertiary"])
        right_toolbar.pack(side="right")

        # View toggle
        view_frame = tk.Frame(right_toolbar, bg=colors["bg_tertiary"])
        view_frame.pack(side="right", padx=10)

        tk.Label(view_frame, text="View:",
                **theme_manager.get_label_style("secondary"),
                bg=colors["bg_tertiary"]).pack(side="left", padx=(0, 5))

        grid_btn = tk.Button(view_frame, text="⊞",
                           command=lambda: self.set_view("grid"),
                           **theme_manager.get_button_style("secondary"),
                           font=("Segoe UI", 12), width=3)
        grid_btn.pack(side="left", padx=1)

        list_btn = tk.Button(view_frame, text="☰",
                           command=lambda: self.set_view("list"),
                           **theme_manager.get_button_style("secondary"),
                           font=("Segoe UI", 12), width=3)
        list_btn.pack(side="left", padx=1)

        # Export button
        export_btn = tk.Button(right_toolbar, text="💾 Export PDF",
                              command=self.export_pdf,
                              **theme_manager.get_button_style("success"),
                              font=("Segoe UI", 11, "bold"),
                              padx=20, pady=8)
        export_btn.pack(side="right", padx=10)

        # Add hover effects
        for btn in [import_btn, clear_btn, grid_btn, list_btn, export_btn]:
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_button_hover(b, False))
    
    def create_main_content(self):
        """Create main content area"""
        colors = theme_manager.get_theme_colors()
        
        content_frame = tk.Frame(self.main_container, **theme_manager.get_frame_style("primary"))
        content_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=0)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Image selection
        self.create_image_panel(content_frame)
        
        # Center divider
        divider = tk.Frame(content_frame, bg=colors["border_medium"], width=2)
        divider.grid(row=0, column=1, sticky="ns", padx=10)
        
        # Right panel - Preview and settings
        self.create_preview_panel(content_frame)
    
    def create_image_panel(self, parent):
        """Create left panel for image selection"""
        colors = theme_manager.get_theme_colors()
        
        # Panel header
        panel_frame = tk.Frame(parent, **theme_manager.get_frame_style("card"))
        panel_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        panel_frame.grid_columnconfigure(0, weight=1)
        panel_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = tk.Frame(panel_frame, bg=colors["bg_secondary"])
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        header_label = tk.Label(header, text="📷 Selected Images",
                               **theme_manager.get_label_style("heading"),
                               bg=colors["bg_secondary"],
                               font=("Segoe UI", 14, "bold"))
        header_label.pack(side="left")
        
        # Drop zone
        self.create_drop_zone(panel_frame)
        
        # Image container with scrollbar
        container_frame = tk.Frame(panel_frame, bg=colors["bg_secondary"])
        container_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas and scrollbar
        self.images_canvas = tk.Canvas(container_frame, **theme_manager.get_canvas_style())
        scrollbar = tk.Scrollbar(container_frame, **theme_manager.get_scrollbar_style(),
                                command=self.images_canvas.yview)
        self.images_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.images_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollable frame
        self.images_container = tk.Frame(self.images_canvas, bg=colors["bg_secondary"])
        self.images_canvas.create_window((0, 0), window=self.images_container, anchor="nw")
        
        # Bind scroll events
        self.images_container.bind("<Configure>", self.update_scroll_region)
        self.images_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def create_drop_zone(self, parent):
        """Create drag and drop zone"""
        colors = theme_manager.get_theme_colors()
        
        self.drop_zone = tk.Frame(parent, 
                                 bg=colors["bg_primary"],
                                 relief="dashed",
                                 borderwidth=2,
                                 height=120)
        self.drop_zone.grid(row=0, column=0, sticky="ew", padx=10, pady=(40, 10))
        self.drop_zone.grid_propagate(False)
        
        # Drop zone content
        drop_content = tk.Frame(self.drop_zone, bg=colors["bg_primary"])
        drop_content.pack(expand=True, fill="both")
        
        # Icon
        try:
            if icon_manager and PIL_AVAILABLE:
                upload_icon = icon_manager.create_add_icon((48, 48), colors["secondary"])
                self.upload_icon = ImageTk.PhotoImage(upload_icon)
                icon_label = tk.Label(drop_content, image=self.upload_icon,
                                    bg=colors["bg_primary"])
                icon_label.pack(pady=(20, 10))
        except:
            pass
        
        # Text
        drop_label = tk.Label(drop_content, 
                             text="Drag & Drop Images Here\\nor Click to Browse",
                             **theme_manager.get_label_style("secondary"),
                             bg=colors["bg_primary"],
                             font=("Segoe UI", 12),
                             justify="center")
        drop_label.pack()
        
        # Make clickable
        def on_click(event):
            self.import_images()
        
        for widget in [self.drop_zone, drop_content, drop_label]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", self.on_drop_zone_hover)
            widget.bind("<Leave>", self.on_drop_zone_leave)
    
    def create_preview_panel(self, parent):
        """Create right panel for preview and settings"""
        colors = theme_manager.get_theme_colors()
        
        panel_frame = tk.Frame(parent, **theme_manager.get_frame_style("card"))
        panel_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        panel_frame.grid_columnconfigure(0, weight=1)
        panel_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = tk.Frame(panel_frame, bg=colors["bg_secondary"])
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        header_label = tk.Label(header, text="👁️ Preview & Settings",
                               **theme_manager.get_label_style("heading"),
                               bg=colors["bg_secondary"],
                               font=("Segoe UI", 14, "bold"))
        header_label.pack()
        
        # Content area
        content_area = tk.Frame(panel_frame, bg=colors["bg_secondary"])
        content_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        content_area.grid_columnconfigure(0, weight=1)
        
        # Preview area
        self.create_preview_area(content_area)
        
        # Settings area
        self.create_settings_area(content_area)
    
    def create_preview_area(self, parent):
        """Create preview area"""
        colors = theme_manager.get_theme_colors()
        
        preview_frame = tk.LabelFrame(parent, text="Preview",
                                     **theme_manager.get_label_style("heading"),
                                     bg=colors["bg_secondary"],
                                     relief="solid", borderwidth=1)
        preview_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame,
                                       bg=colors["bg_primary"],
                                       height=200,
                                       relief="sunken",
                                       borderwidth=1)
        self.preview_canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Preview placeholder
        self.show_preview_placeholder()
    
    def create_settings_area(self, parent):
        """Create settings area"""
        colors = theme_manager.get_theme_colors()
        
        settings_frame = tk.LabelFrame(parent, text="PDF Settings",
                                      **theme_manager.get_label_style("heading"),
                                      bg=colors["bg_secondary"],
                                      relief="solid", borderwidth=1)
        settings_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Watermark settings
        row = 0
        
        # Watermark checkbox
        watermark_check = tk.Checkbutton(settings_frame,
                                        text="Add Watermark",
                                        variable=self.apply_watermark,
                                        command=self.toggle_watermark,
                                        **theme_manager.get_label_style("primary"),
                                        bg=colors["bg_secondary"],
                                        font=("Segoe UI", 11))
        watermark_check.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        row += 1
        
        # Watermark text
        tk.Label(settings_frame, text="Watermark Text:",
                **theme_manager.get_label_style("secondary"),
                bg=colors["bg_secondary"]).grid(row=row, column=0, sticky="w", padx=10, pady=2)
        
        self.watermark_entry = tk.Entry(settings_frame,
                                       textvariable=self.watermark_text_var,
                                       state="disabled",
                                       **theme_manager.get_entry_style())
        self.watermark_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=2)
        
        row += 1
        
        # Quality setting
        tk.Label(settings_frame, text="Quality:",
                **theme_manager.get_label_style("secondary"),
                bg=colors["bg_secondary"]).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        self.quality_var = tk.IntVar(value=95)
        quality_scale = tk.Scale(settings_frame,
                                from_=50, to=100,
                                variable=self.quality_var,
                                orient="horizontal",
                                bg=colors["bg_secondary"],
                                fg=colors["text_primary"],
                                highlightthickness=0)
        quality_scale.grid(row=row, column=1, sticky="ew", padx=10, pady=2)
        
        row += 1
        
        # Page size
        tk.Label(settings_frame, text="Page Size:",
                **theme_manager.get_label_style("secondary"),
                bg=colors["bg_secondary"]).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        self.page_size_var = tk.StringVar(value="A4")
        page_size_combo = ttk.Combobox(settings_frame,
                                      textvariable=self.page_size_var,
                                      values=["A4", "Letter", "Legal", "A3", "Custom"],
                                      state="readonly")
        page_size_combo.grid(row=row, column=1, sticky="ew", padx=10, pady=2)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        colors = theme_manager.get_theme_colors()
        
        status_frame = tk.Frame(self.main_container,
                               bg=colors["bg_tertiary"],
                               height=30)
        status_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        status_frame.grid_propagate(False)
        
        # Status content
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(status_frame,
                               textvariable=self.status_var,
                               **theme_manager.get_label_style("secondary"),
                               bg=colors["bg_tertiary"],
                               font=("Segoe UI", 9))
        status_label.pack(side="left", padx=10, pady=5)
        
        # Progress bar (hidden by default)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame,
                                           variable=self.progress_var,
                                           maximum=100)
        # Don't pack initially
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        if TkinterDnD and DND_FILES:
            try:
                self.drop_zone.drop_target_register(DND_FILES)
                self.drop_zone.dnd_bind('<<Drop>>', self.handle_drop)
                
                self.images_canvas.drop_target_register(DND_FILES)
                self.images_canvas.dnd_bind('<<Drop>>', self.handle_drop)
            except:
                pass
    
    def setup_bindings(self):
        """Setup keyboard and other bindings"""
        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.import_images())
        self.root.bind("<Control-s>", lambda e: self.export_pdf())
        self.root.bind("<Control-t>", lambda e: self.toggle_theme())
        self.root.bind("<Delete>", lambda e: self.delete_selected())
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
    
    # Event handlers and utility methods
    def import_images(self):
        """Import images from file dialog"""
        filetypes = [
            ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=filetypes
        )
        
        if files:
            self.add_images(files)
    
    def add_images(self, file_paths):
        """Add images to the selection"""
        new_images = []
        for path in file_paths:
            if path not in self.selected_images:
                self.selected_images.append(path)
                new_images.append(path)
        
        if new_images:
            self.update_image_count()
            self.display_images(new_images)
            self.update_status(f"Added {len(new_images)} image(s)")
            
            if animation_manager:
                animation_manager.animate_notification(
                    self.root,
                    f"Added {len(new_images)} image(s) successfully",
                    "success"
                )
    
    def display_images(self, image_paths):
        """Display images in the container"""
        if not PIL_AVAILABLE:
            return
        
        for i, path in enumerate(image_paths):
            self.create_image_thumbnail(path, len(self.selected_images) - len(image_paths) + i)
        
        self.update_scroll_region()
    
    def create_image_thumbnail(self, image_path, index):
        """Create thumbnail for an image"""
        if not PIL_AVAILABLE:
            return
        
        try:
            colors = theme_manager.get_theme_colors()
            
            # Load and resize image
            img = Image.open(image_path)
            img.thumbnail(self.settings["thumbnail_size"])
            img_tk = ImageTk.PhotoImage(img)
            self.image_thumbnails.append(img_tk)
            
            # Create thumbnail frame
            thumb_frame = tk.Frame(self.images_container,
                                  **theme_manager.get_frame_style("card"),
                                  relief="solid", borderwidth=1,
                                  padx=10, pady=10)
            
            # Calculate grid position
            if self.current_view.get() == "grid":
                cols = 3
                row = index // cols
                col = index % cols
                thumb_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            else:
                thumb_frame.grid(row=index, column=0, sticky="ew", padx=5, pady=2)
            
            # Image display
            img_label = tk.Label(thumb_frame, image=img_tk,
                               bg=colors["bg_secondary"])
            img_label.pack(pady=(0, 5))
            
            # Image info
            filename = os.path.basename(image_path)
            if len(filename) > 20:
                filename = filename[:17] + "..."
            
            name_label = tk.Label(thumb_frame, text=filename,
                                 **theme_manager.get_label_style("secondary"),
                                 bg=colors["bg_secondary"],
                                 font=("Segoe UI", 9))
            name_label.pack()
            
            # Selection checkbox
            var = tk.BooleanVar(value=True)
            check = tk.Checkbutton(thumb_frame,
                                  text="Include",
                                  variable=var,
                                  bg=colors["bg_secondary"],
                                  command=lambda p=image_path, v=var: self.update_preview())
            check.pack(pady=(5, 0))
            
            self.selected_image_vars.append((image_path, var))
            
            # Add hover effect
            def on_enter(event):
                thumb_frame.configure(highlightbackground=colors["primary"], highlightthickness=2)
            
            def on_leave(event):
                thumb_frame.configure(highlightbackground=colors["border_light"], highlightthickness=1)
            
            thumb_frame.bind("<Enter>", on_enter)
            thumb_frame.bind("<Leave>", on_leave)
            
            # Make clickable for preview
            for widget in [thumb_frame, img_label, name_label]:
                widget.bind("<Button-1>", lambda e, p=image_path: self.show_image_preview(p))
            
        except Exception as e:
            self.update_status(f"Error loading image: {str(e)}")
    
    def handle_drop(self, event):
        """Handle drag and drop"""
        if not hasattr(event, 'data'):
            return
        
        dropped_files = self.root.tk.splitlist(event.data)
        image_files = []
        
        for file_path in dropped_files:
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                    image_files.append(file_path)
        
        if image_files:
            self.add_images(image_files)
    
    def update_image_count(self):
        """Update image count display"""
        count = len(self.selected_images)
        if count == 0:
            self.image_count_var.set("No images selected")
        elif count == 1:
            self.image_count_var.set("1 image selected")
        else:
            self.image_count_var.set(f"{count} images selected")
    
    def update_scroll_region(self, event=None):
        """Update scroll region for canvas"""
        self.images_canvas.configure(scrollregion=self.images_canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.images_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_button_hover(self, button, enter):
        """Handle button hover animation"""
        if animation_manager:
            animation_manager.animate_button_hover(button, enter)
    
    def on_drop_zone_hover(self, event):
        """Handle drop zone hover"""
        colors = theme_manager.get_theme_colors()
        self.drop_zone.configure(bg=colors["bg_secondary"])
    
    def on_drop_zone_leave(self, event):
        """Handle drop zone leave"""
        colors = theme_manager.get_theme_colors()
        self.drop_zone.configure(bg=colors["bg_primary"])
    
    def show_image_preview(self, image_path):
        """Show image preview in preview panel"""
        if not PIL_AVAILABLE:
            return
        
        try:
            # Load and resize image for preview
            img = Image.open(image_path)
            img.thumbnail(self.settings["preview_size"])
            preview_img = ImageTk.PhotoImage(img)
            
            # Clear previous preview
            self.preview_canvas.delete("all")
            
            # Show new preview
            canvas_width = self.preview_canvas.winfo_width() or 250
            canvas_height = self.preview_canvas.winfo_height() or 200
            
            x = canvas_width // 2
            y = canvas_height // 2
            
            self.preview_canvas.create_image(x, y, image=preview_img, anchor="center")
            
            # Store reference to prevent garbage collection
            self.current_preview = preview_img
            
        except Exception as e:
            self.update_status(f"Error showing preview: {str(e)}")
    
    def show_preview_placeholder(self):
        """Show placeholder in preview area"""
        colors = theme_manager.get_theme_colors()
        
        self.preview_canvas.delete("all")
        
        # Placeholder text
        self.preview_canvas.create_text(
            125, 100,  # Center of 250x200 canvas
            text="Click an image\\nto preview",
            fill=colors["text_secondary"],
            font=("Segoe UI", 12),
            justify="center"
        )
    
    def toggle_watermark(self):
        """Toggle watermark entry state"""
        if self.apply_watermark.get():
            self.watermark_entry.configure(state="normal")
        else:
            self.watermark_entry.configure(state="disabled")
    
    def update_preview(self):
        """Update preview based on current settings"""
        # This would update the PDF preview
        pass
    
    def set_view(self, view_type):
        """Set view type (grid or list)"""
        self.current_view.set(view_type)
        self.refresh_image_display()
    
    def refresh_image_display(self):
        """Refresh image display with current view"""
        # Clear current display
        for widget in self.images_container.winfo_children():
            widget.destroy()
        
        # Redisplay images
        if self.selected_images:
            self.display_images(self.selected_images)
    
    def clear_all_images(self):
        """Clear all selected images"""
        if not self.selected_images:
            return
        
        result = messagebox.askyesno(
            "Clear All Images",
            f"Are you sure you want to remove all {len(self.selected_images)} images?"
        )
        
        if result:
            self.selected_images.clear()
            self.image_thumbnails.clear()
            self.selected_image_vars.clear()
            self.resized_images_for_pdf.clear()
            
            # Clear UI
            for widget in self.images_container.winfo_children():
                widget.destroy()
            
            self.show_preview_placeholder()
            self.update_image_count()
            self.update_status("All images cleared")
            
            if animation_manager:
                animation_manager.animate_notification(
                    self.root,
                    "All images cleared",
                    "info"
                )
    
    def delete_selected(self):
        """Delete selected images"""
        # This would delete currently selected/highlighted images
        pass
    
    def export_pdf(self):
        """Export images to PDF"""
        if not self.selected_images:
            messagebox.showwarning("No Images", "Please select some images first.")
            return
        
        if not PIL_AVAILABLE:
            messagebox.showerror("Missing Dependencies", 
                               "PIL/Pillow is required for PDF export. Please install requirements.")
            return
        
        # Get selected images
        selected_files = [path for path, var in self.selected_image_vars if var.get()]
        
        if not selected_files:
            messagebox.showwarning("No Images Selected", 
                                 "Please select at least one image to include in the PDF.")
            return
        
        # Get save location
        pdf_path = filedialog.asksaveasfilename(
            title="Save PDF as...",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not pdf_path:
            return
        
        # Show progress
        self.show_progress()
        
        # Export in background thread
        threading.Thread(
            target=self.export_pdf_worker,
            args=(selected_files, pdf_path),
            daemon=True
        ).start()
    
    def export_pdf_worker(self, image_paths, pdf_path):
        """Worker thread for PDF export"""
        try:
            self.update_status("Processing images...")
            
            images = []
            total_images = len(image_paths)
            
            for i, path in enumerate(image_paths):
                # Update progress
                progress = (i / total_images) * 100
                self.root.after(0, lambda p=progress: self.update_progress(p))
                
                # Load and process image
                img = Image.open(path)
                img = img.convert("RGB")
                
                # Apply watermark if enabled
                if self.apply_watermark.get():
                    img = self.add_watermark_to_image(img)
                
                images.append(img)
            
            # Save PDF
            self.update_status("Saving PDF...")
            self.root.after(0, lambda: self.update_progress(90))
            
            if images:
                images[0].save(pdf_path, save_all=True, append_images=images[1:])
            
            # Complete
            self.root.after(0, lambda: self.export_complete(pdf_path))
            
        except Exception as e:
            self.root.after(0, lambda: self.export_error(str(e)))
    
    def add_watermark_to_image(self, image):
        """Add watermark to image"""
        if not self.watermark_text_var.get().strip():
            return image
        
        try:
            watermark_img = image.copy()
            draw = ImageDraw.Draw(watermark_img)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", 24)
                except:
                    font = ImageFont.load_default()
            
            text = self.watermark_text_var.get().strip()
            
            # Get text size
            try:
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw.textsize(text, font=font)
            
            # Position watermark
            x = watermark_img.width - text_width - 20
            y = watermark_img.height - text_height - 20
            
            # Draw shadow
            draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 128))
            # Draw main text
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))
            
            return watermark_img
            
        except Exception as e:
            print(f"Error adding watermark: {e}")
            return image
    
    def show_progress(self):
        """Show progress bar"""
        self.progress_bar.pack(side="right", padx=10, pady=5)
        self.progress_var.set(0)
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
    
    def hide_progress(self):
        """Hide progress bar"""
        self.progress_bar.pack_forget()
    
    def export_complete(self, pdf_path):
        """Handle export completion"""
        self.hide_progress()
        self.update_status("PDF exported successfully")
        
        if animation_manager:
            animation_manager.animate_notification(
                self.root,
                f"PDF saved successfully to {os.path.basename(pdf_path)}",
                "success"
            )
        
        # Ask to open file
        result = messagebox.askyesno(
            "Export Complete",
            f"PDF saved successfully!\\n\\nOpen the file now?",
            parent=self.root
        )
        
        if result:
            try:
                os.startfile(pdf_path)  # Windows
            except:
                try:
                    os.system(f'open "{pdf_path}"')  # macOS
                except:
                    os.system(f'xdg-open "{pdf_path}"')  # Linux
    
    def export_error(self, error_message):
        """Handle export error"""
        self.hide_progress()
        self.update_status("Export failed")
        
        if animation_manager:
            animation_manager.animate_notification(
                self.root,
                f"Export failed: {error_message}",
                "error"
            )
        
        messagebox.showerror("Export Error", f"Failed to export PDF:\\n{error_message}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        old_theme = theme_manager.current_theme
        theme_manager.toggle_theme()
        
        # Update UI (would require rebuilding in a real implementation)
        self.root.configure(bg=theme_manager.get_color("bg_primary"))
        
        if animation_manager:
            animation_manager.animate_notification(
                self.root,
                f"Switched to {theme_manager.current_theme} theme",
                "success"
            )
    
    def show_settings(self):
        """Show settings dialog"""
        if animation_manager:
            animation_manager.animate_notification(
                self.root,
                "Settings panel coming soon!",
                "info"
            )
    
    def toggle_fullscreen(self, event):
        """Toggle fullscreen mode"""
        self.root.attributes("-fullscreen", True)
    
    def exit_fullscreen(self, event):
        """Exit fullscreen mode"""
        self.root.attributes("-fullscreen", False)


if __name__ == "__main__":
    if TkinterDnD:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    app = ModernApp(root)
    root.mainloop()
