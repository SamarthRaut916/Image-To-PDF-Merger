import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
from pathlib import Path
from Module.Splashscreen import SplashScreen
# Try to import PIL, but gracefully handle if not available
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class SimpleImageToPDF:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.selected_images = []
        self.image_thumbnails = []  # Store thumbnail PhotoImage objects
        self.image_checkboxes = []  # Store checkbox variables
        self.thumbnail_widgets = []  # Store thumbnail widget references
        self.create_ui()

    def setup_window(self):
        """Setup main window"""
        self.root.title("Image to PDF Converter - Enhanced Edition v2.0")
        self.root.geometry("1000x700")

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500)
        y = (self.root.winfo_screenheight() // 2) - (350)
        self.root.geometry(f"1000x700+{x}+{y}")

        # Configure colors
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#64748b',
            'success': '#10b981',
            'danger': '#ef4444',
            'bg_primary': '#ffffff',
            'bg_secondary': '#f8fafc',
            'text_primary': '#1e293b'
        }

        self.root.configure(bg=self.colors['bg_primary'])

    def create_ui(self):
        """Create the user interface"""
        # Header
        self.create_header()

        # Main content
        self.create_main_content()

        # Footer
        self.create_footer()

    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(
            self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(header_frame,
                               text="🖼️ Image to PDF Converter",
                               font=('Segoe UI', 20, 'bold'),
                               bg=self.colors['primary'],
                               fg='white')
        title_label.pack(side='left', padx=20, pady=20)

        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                  text="Enhanced Edition v2.0 • Modern • Professional",
                                  font=('Segoe UI', 10),
                                  bg=self.colors['primary'],
                                  fg='#cbd5e1')
        subtitle_label.pack(side='left', padx=(0, 20), pady=(35, 15))

        # Info
        info_label = tk.Label(header_frame,
                              text=f"Images Selected: {len(self.selected_images)}",
                              font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['primary'],
                              fg='white')
        info_label.pack(side='right', padx=20, pady=20)

        self.info_label = info_label

    def create_main_content(self):
        """Create main content area"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Left panel - Image selection
        left_frame = tk.LabelFrame(main_frame,
                                   text="📁 Select Images",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   padx=10, pady=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Import button
        import_btn = tk.Button(left_frame,
                               text="📂 Browse for Images",
                               command=self.import_images,
                               font=('Segoe UI', 12, 'bold'),
                               bg=self.colors['primary'],
                               fg='white',
                               relief='flat',
                               padx=20, pady=10,
                               cursor='hand2')
        import_btn.pack(pady=10)

        # Images container with scrollbar
        container_frame = tk.Frame(left_frame, bg=self.colors['bg_secondary'])
        container_frame.pack(fill='both', expand=True, pady=10)

        # Canvas for scrollable thumbnails
        self.images_canvas = tk.Canvas(
            container_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(
            container_frame, orient='vertical', command=self.images_canvas.yview)
        self.images_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.images_canvas.pack(side='left', fill='both', expand=True)

        # Scrollable frame inside canvas
        self.thumbnails_frame = tk.Frame(self.images_canvas, bg='white')
        self.images_canvas.create_window(
            (0, 0), window=self.thumbnails_frame, anchor='nw')

        # Bind mousewheel to canvas
        def on_mousewheel(event):
            self.images_canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units")

        self.images_canvas.bind("<MouseWheel>", on_mousewheel)

        # Update scroll region when frame changes
        def configure_scroll_region(event):
            self.images_canvas.configure(
                scrollregion=self.images_canvas.bbox("all"))

        self.thumbnails_frame.bind('<Configure>', configure_scroll_region)

        # Clear button
        clear_btn = tk.Button(left_frame,
                              text="🗑️ Clear All",
                              command=self.clear_images,
                              font=('Segoe UI', 10),
                              bg=self.colors['danger'],
                              fg='white',
                              relief='flat',
                              padx=15, pady=5)
        clear_btn.pack(pady=5)

        # Right panel - Settings and export
        right_frame = tk.LabelFrame(main_frame,
                                    text="⚙️ Settings & Export",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    padx=10, pady=10)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        right_frame.config(width=300)
        right_frame.pack_propagate(False)

        # Preview area - scrollable for multiple checked images
        preview_frame = tk.LabelFrame(right_frame,
                                      text="👁️ Selected Images Preview",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg=self.colors['bg_secondary'])
        preview_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Create scrollable preview area
        self.preview_canvas = tk.Canvas(preview_frame,
                                        bg='white',
                                        highlightthickness=0,
                                        height=400)  # Set explicit height for better scrolling
        preview_scrollbar = tk.Scrollbar(preview_frame,
                                         orient="vertical",
                                         command=self.preview_canvas.yview)
        self.preview_scrollable_frame = tk.Frame(
            self.preview_canvas, bg='white')

        # Enhanced scrolling configuration
        def configure_scroll_region(event=None):
            # Force update of scroll region
            self.preview_canvas.update_idletasks()
            self.preview_canvas.configure(
                scrollregion=self.preview_canvas.bbox("all"))

        def configure_canvas_width(event):
            # Make sure the scrollable frame takes full canvas width
            canvas_width = event.width
            self.preview_canvas.itemconfig(
                self.canvas_window, width=canvas_width)

        self.preview_scrollable_frame.bind(
            "<Configure>", configure_scroll_region)
        self.preview_canvas.bind("<Configure>", configure_canvas_width)

        self.canvas_window = self.preview_canvas.create_window((0, 0),
                                                               window=self.preview_scrollable_frame,
                                                               anchor="nw")
        self.preview_canvas.configure(yscrollcommand=preview_scrollbar.set)

        # Enhanced mouse wheel scrolling
        def _on_mousewheel(event):
            # Only scroll if there's content that extends beyond visible area
            bbox = self.preview_canvas.bbox("all")
            if bbox and bbox[3] > self.preview_canvas.winfo_height():
                self.preview_canvas.yview_scroll(
                    int(-1*(event.delta/120)), "units")

        def bind_mousewheel(event):
            self.preview_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def unbind_mousewheel(event):
            self.preview_canvas.unbind_all("<MouseWheel>")

        # Bind/unbind mousewheel only when mouse is over the canvas
        self.preview_canvas.bind("<Enter>", bind_mousewheel)
        self.preview_canvas.bind("<Leave>", unbind_mousewheel)

        # Keyboard scrolling support
        def _on_key_scroll(event):
            bbox = self.preview_canvas.bbox("all")
            if bbox and bbox[3] > self.preview_canvas.winfo_height():
                if event.keysym == "Up":
                    self.preview_canvas.yview_scroll(-1, "units")
                elif event.keysym == "Down":
                    self.preview_canvas.yview_scroll(1, "units")
                elif event.keysym == "Page_Up":
                    self.preview_canvas.yview_scroll(-1, "pages")
                elif event.keysym == "Page_Down":
                    self.preview_canvas.yview_scroll(1, "pages")
                elif event.keysym == "Home":
                    self.preview_canvas.yview_moveto(0)
                elif event.keysym == "End":
                    self.preview_canvas.yview_moveto(1)

        def bind_keyboard(event):
            self.preview_canvas.focus_set()
            self.preview_canvas.bind("<Key>", _on_key_scroll)

        def unbind_keyboard(event):
            self.preview_canvas.unbind("<Key>")

        self.preview_canvas.bind("<Button-1>", bind_keyboard)
        self.preview_canvas.bind("<FocusOut>", unbind_keyboard)

        self.preview_canvas.pack(
            side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        preview_scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)

        # Initial preview message
        self.empty_preview_label = tk.Label(self.preview_scrollable_frame,
                                            text="Select images to see preview\nwith sequence numbers",
                                            bg='white',
                                            fg='gray',
                                            font=('Segoe UI', 10))
        self.empty_preview_label.pack(pady=20)

        # Settings
        settings_frame = tk.LabelFrame(right_frame,
                                       text="📄 PDF Settings",
                                       font=('Segoe UI', 10, 'bold'),
                                       bg=self.colors['bg_secondary'])
        settings_frame.pack(fill='x', pady=(0, 10))

        # Page size
        tk.Label(settings_frame, text="Page Size:",
                 font=('Segoe UI', 9),
                 bg=self.colors['bg_secondary']).pack(anchor='w', padx=5)

        self.page_size_var = tk.StringVar(value="A4")
        page_combo = ttk.Combobox(settings_frame,
                                  textvariable=self.page_size_var,
                                  values=["A4", "Letter", "Legal", "A3"],
                                  state="readonly")
        page_combo.pack(fill='x', padx=5, pady=2)

        # Image Fit Mode
        tk.Label(settings_frame, text="Image Fit:",
                 font=('Segoe UI', 9),
                 bg=self.colors['bg_secondary']).pack(anchor='w', padx=5, pady=(10, 0))

        self.fit_mode_var = tk.StringVar(value="Fit to Page")
        fit_combo = ttk.Combobox(settings_frame,
                                 textvariable=self.fit_mode_var,
                                 values=["Fit to Page",
                                         "Fill Page", "Original Size"],
                                 state="readonly")
        fit_combo.pack(fill='x', padx=5, pady=2)

        # Fit mode description
        self.fit_desc_var = tk.StringVar()
        self.fit_desc_label = tk.Label(settings_frame,
                                       textvariable=self.fit_desc_var,
                                       font=('Segoe UI', 7),
                                       fg='gray',
                                       bg=self.colors['bg_secondary'],
                                       wraplength=250)
        self.fit_desc_label.pack(fill='x', padx=5, pady=(0, 5))

        # Update description when fit mode changes
        def update_fit_description(*args):
            mode = self.fit_mode_var.get()
            descriptions = {
                "Fit to Page": "Scales image to fit completely within page (maintains aspect ratio)",
                "Fill Page": "Scales image to fill entire page (may crop, maintains aspect ratio)",
                "Original Size": "Keeps original image size (may exceed page boundaries)"
            }
            self.fit_desc_var.set(descriptions.get(mode, ""))

        self.fit_mode_var.trace('w', update_fit_description)
        update_fit_description()  # Set initial description

        # Quality
        tk.Label(settings_frame, text="Quality:",
                 font=('Segoe UI', 9),
                 bg=self.colors['bg_secondary']).pack(anchor='w', padx=5, pady=(10, 0))

        self.quality_var = tk.IntVar(value=95)
        quality_scale = tk.Scale(settings_frame,
                                 from_=50, to=100,
                                 variable=self.quality_var,
                                 orient='horizontal',
                                 bg=self.colors['bg_secondary'])
        quality_scale.pack(fill='x', padx=5, pady=2)

        # Watermark
        self.watermark_var = tk.BooleanVar()
        watermark_check = tk.Checkbutton(settings_frame,
                                         text="Add Watermark",
                                         variable=self.watermark_var,
                                         command=self.toggle_watermark,
                                         font=('Segoe UI', 9),
                                         bg=self.colors['bg_secondary'])
        watermark_check.pack(anchor='w', padx=5, pady=(10, 0))

        self.watermark_text_var = tk.StringVar(value="Samarth Raut")
        self.watermark_entry = tk.Entry(settings_frame,
                                        textvariable=self.watermark_text_var,
                                        state='disabled')
        self.watermark_entry.pack(fill='x', padx=5, pady=2)

        # Export button
        export_btn = tk.Button(right_frame,
                               text="💾 Export to PDF",
                               command=self.export_pdf,
                               font=('Segoe UI', 14, 'bold'),
                               bg=self.colors['success'],
                               fg='white',
                               relief='flat',
                               padx=20, pady=15,
                               cursor='hand2')
        export_btn.pack(side='bottom', fill='x', pady=10)

        # Bind events
        # Note: Thumbnail selection will be handled by individual checkboxes

    def create_footer(self):
        """Create footer"""
        footer_frame = tk.Frame(
            self.root, bg=self.colors['secondary'], height=40)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)

        # Status
        self.status_var = tk.StringVar(value="Ready to convert images")
        status_label = tk.Label(footer_frame,
                                textvariable=self.status_var,
                                font=('Segoe UI', 9),
                                bg=self.colors['secondary'],
                                fg='white')
        status_label.pack(side='left', padx=10, pady=10)

        # Credit
        credit_label = tk.Label(footer_frame,
                                text="Enhanced by Samarth Raut • v2.0",
                                font=('Segoe UI', 9),
                                bg=self.colors['secondary'],
                                fg='#cbd5e1')
        credit_label.pack(side='right', padx=10, pady=10)

    def import_images(self):
        """Import images from file dialog"""
        filetypes = [
            ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("All Files", "*.*")
        ]

        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=filetypes
        )

        if files:
            new_images = []
            for file_path in files:
                if file_path not in self.selected_images:
                    self.selected_images.append(file_path)
                    new_images.append(file_path)

            # Create thumbnails for new images
            for file_path in new_images:
                self.create_thumbnail(file_path)

            self.update_info()
            self.update_preview_sequence()  # Update preview with new images
            self.status_var.set(f"Added {len(new_images)} image(s)")

    def create_thumbnail(self, image_path):
        """Create and display thumbnail for an image"""
        if not PIL_AVAILABLE:
            # If PIL not available, show simple text entry
            self.create_simple_entry(image_path)
            return

        try:
            # Load and create thumbnail
            img = Image.open(image_path)
            img.thumbnail((120, 120))  # Thumbnail size
            photo = ImageTk.PhotoImage(img)
            self.image_thumbnails.append(photo)

            # Create thumbnail frame
            thumb_frame = tk.Frame(self.thumbnails_frame,
                                   bg='white',
                                   relief='solid',
                                   borderwidth=1,
                                   padx=5, pady=5)

            # Calculate position (2 columns)
            row = len(self.thumbnail_widgets) // 2
            col = len(self.thumbnail_widgets) % 2
            thumb_frame.grid(row=row, column=col, padx=5, pady=5, sticky='w')

            # Image display
            img_label = tk.Label(thumb_frame, image=photo, bg='white')
            img_label.pack()

            # Filename
            filename = os.path.basename(image_path)
            if len(filename) > 15:
                filename = filename[:12] + "..."

            name_label = tk.Label(thumb_frame,
                                  text=filename,
                                  font=('Segoe UI', 8),
                                  bg='white',
                                  fg=self.colors['text_primary'])
            name_label.pack()

            # Checkbox for selection
            var = tk.BooleanVar(value=True)
            checkbox = tk.Checkbutton(thumb_frame,
                                      text="Include",
                                      variable=var,
                                      bg='white',
                                      font=('Segoe UI', 8),
                                      command=lambda: self.on_checkbox_change())
            checkbox.pack()

            self.image_checkboxes.append(var)
            self.thumbnail_widgets.append(thumb_frame)

            # Make thumbnail clickable for preview
            def show_preview_click(event):
                self.show_preview(image_path)

            img_label.bind("<Button-1>", show_preview_click)
            name_label.bind("<Button-1>", show_preview_click)

            # Hover effects
            def on_enter(event):
                thumb_frame.config(bg=self.colors['bg_secondary'])
                img_label.config(bg=self.colors['bg_secondary'])
                name_label.config(bg=self.colors['bg_secondary'])
                checkbox.config(bg=self.colors['bg_secondary'])

            def on_leave(event):
                thumb_frame.config(bg='white')
                img_label.config(bg='white')
                name_label.config(bg='white')
                checkbox.config(bg='white')

            for widget in [thumb_frame, img_label, name_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

        except Exception as e:
            print(f"Error creating thumbnail for {image_path}: {e}")
            self.create_simple_entry(image_path)

    def create_simple_entry(self, image_path):
        """Create simple text entry when PIL is not available"""
        # Simple frame with filename and checkbox
        simple_frame = tk.Frame(self.thumbnails_frame,
                                bg='white',
                                relief='solid',
                                borderwidth=1,
                                padx=10, pady=5)

        row = len(self.thumbnail_widgets)
        simple_frame.grid(row=row, column=0, columnspan=2,
                          padx=5, pady=2, sticky='ew')

        # Filename
        filename = os.path.basename(image_path)
        name_label = tk.Label(simple_frame,
                              text=f"📷 {filename}",
                              font=('Segoe UI', 10),
                              bg='white',
                              fg=self.colors['text_primary'])
        name_label.pack(side='left')

        # Checkbox
        var = tk.BooleanVar(value=True)
        checkbox = tk.Checkbutton(simple_frame,
                                  text="Include",
                                  variable=var,
                                  bg='white',
                                  command=lambda: self.on_checkbox_change())
        checkbox.pack(side='right')

        self.image_checkboxes.append(var)
        self.thumbnail_widgets.append(simple_frame)

    def on_checkbox_change(self):
        """Handle checkbox state changes and update preview sequence"""
        self.update_preview_sequence()
        self.update_info()  # Update the count display

    def update_preview_sequence(self):
        """Update preview area to show all checked images with sequence numbers"""
        # Clear existing preview widgets
        for widget in self.preview_scrollable_frame.winfo_children():
            widget.destroy()

        # Get checked images
        checked_images = []
        for i, is_checked in enumerate(self.image_checkboxes):
            if is_checked.get():
                checked_images.append(
                    (i + 1, self.selected_images[i]))  # (sequence, path)

        if not checked_images:
            # Show empty message
            empty_label = tk.Label(self.preview_scrollable_frame,
                                   text="No images selected\nCheck images to see preview",
                                   bg='white',
                                   fg='gray',
                                   font=('Segoe UI', 10))
            empty_label.pack(pady=20)
            self.update_scroll_region()
            return

        # Show title with scroll hint
        title_text = f"📋 Selected Images ({len(checked_images)} images)"
        if len(checked_images) > 3:  # If many images, show scroll hint
            title_text += "\n💡 Use mouse wheel or arrow keys to scroll"

        title_label = tk.Label(self.preview_scrollable_frame,
                               text=title_text,
                               bg='white',
                               fg=self.colors['text_primary'],
                               font=('Segoe UI', 12, 'bold'),
                               justify='center')
        # Show each checked image with sequence number
        title_label.pack(pady=(10, 5))
        for seq_num, (orig_index, image_path) in enumerate(checked_images, 1):
            if not PIL_AVAILABLE:
                # Simple text preview when PIL not available
                img_frame = tk.Frame(self.preview_scrollable_frame,
                                     bg='white',
                                     relief='solid',
                                     borderwidth=1)
                img_frame.pack(fill='x', padx=10, pady=2)

                seq_label = tk.Label(img_frame,
                                     text=f"{seq_num}.",
                                     bg='white',
                                     fg=self.colors['primary'],
                                     font=('Segoe UI', 12, 'bold'))
                seq_label.pack(side='left', padx=5)

                filename = os.path.basename(image_path)
                name_label = tk.Label(img_frame,
                                      text=filename,
                                      bg='white',
                                      fg=self.colors['text_primary'],
                                      font=('Segoe UI', 9))
                name_label.pack(side='left', fill='x', expand=True)
            else:
                try:
                    # Create frame for this image
                    img_frame = tk.Frame(self.preview_scrollable_frame,
                                         bg='white',
                                         relief='solid',
                                         borderwidth=1,
                                         padx=5, pady=5)
                    img_frame.pack(fill='x', padx=10, pady=2)

                    # Sequence number
                    seq_label = tk.Label(img_frame,
                                         text=f"{seq_num}.",
                                         bg='white',
                                         fg=self.colors['primary'],
                                         font=('Segoe UI', 14, 'bold'))
                    seq_label.pack(side='left', padx=(0, 10))

                    # Image preview
                    img = Image.open(image_path)
                    # Smaller thumbnail for sequence view
                    img.thumbnail((80, 60))
                    photo = ImageTk.PhotoImage(img)

                    img_label = tk.Label(img_frame, image=photo, bg='white')
                    img_label.image = photo  # Keep reference
                    img_label.pack(side='left', padx=(0, 10))

                    # Image info
                    info_frame = tk.Frame(img_frame, bg='white')
                    info_frame.pack(side='left', fill='x', expand=True)

                    filename = os.path.basename(image_path)
                    name_label = tk.Label(info_frame,
                                          text=filename,
                                          bg='white',
                                          fg=self.colors['text_primary'],
                                          font=('Segoe UI', 9, 'bold'),
                                          anchor='w')
                    name_label.pack(fill='x')

                    # Image dimensions
                    with Image.open(image_path) as temp_img:
                        dimensions = f"{temp_img.width} × {temp_img.height}"

                    dim_label = tk.Label(info_frame,
                                         text=f"Size: {dimensions}",
                                         bg='white',
                                         fg='gray',
                                         font=('Segoe UI', 8),
                                         anchor='w')
                    dim_label.pack(fill='x')

                except Exception as e:
                    # Error loading image
                    error_frame = tk.Frame(self.preview_scrollable_frame,
                                           bg='white',
                                           relief='solid',
                                           borderwidth=1)
                    error_frame.pack(fill='x', padx=10, pady=2)

                    seq_label = tk.Label(error_frame,
                                         text=f"{seq_num}.",
                                         bg='white',
                                         fg=self.colors['primary'],
                                         font=('Segoe UI', 12, 'bold'))
                    seq_label.pack(side='left', padx=5)

                    error_label = tk.Label(error_frame,
                                           text=f"Error: {os.path.basename(image_path)}",
                                           bg='white',
                                           fg='red',
                                           font=('Segoe UI', 9))
                    error_label.pack(side='left', fill='x', expand=True)

        # Add scroll indicator at the bottom if content is scrollable
        self.update_scroll_region()

        # Check if scrolling is needed and add indicator
        bbox = self.preview_canvas.bbox("all")
        if bbox:
            canvas_height = self.preview_canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            if content_height > canvas_height and len(checked_images) > 0:
                scroll_hint = tk.Label(self.preview_scrollable_frame,
                                       text="⬇️ Scroll down for more images ⬇️",
                                       bg='lightblue',
                                       fg='darkblue',
                                       font=('Segoe UI', 8, 'italic'),
                                       pady=5)
                scroll_hint.pack(fill='x', padx=10, pady=5)

        # Update scroll region with enhanced handling
        self.update_scroll_region()

    def update_scroll_region(self):
        """Update the scroll region for the preview canvas"""
        self.preview_scrollable_frame.update_idletasks()
        self.preview_canvas.update_idletasks()

        # Force scroll region recalculation
        bbox = self.preview_canvas.bbox("all")
        if bbox:
            self.preview_canvas.configure(scrollregion=bbox)
            # Show/hide scrollbar based on content size
            canvas_height = self.preview_canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            if content_height > canvas_height:
                # Content is scrollable, ensure scrollbar is visible
                pass  # Scrollbar is already packed
        else:
            self.preview_canvas.configure(scrollregion=(0, 0, 0, 0))

        # Reset scroll position to top when content changes
        self.preview_canvas.yview_moveto(0)

    def test_scroll_functionality(self):
        """Test method to verify scrolling works with many items"""
        # This method can be called for testing - adds dummy preview items
        for i in range(10):
            test_frame = tk.Frame(self.preview_scrollable_frame,
                                  bg='lightgray',
                                  relief='solid',
                                  borderwidth=1,
                                  height=60)
            test_frame.pack(fill='x', padx=10, pady=2)

            test_label = tk.Label(test_frame,
                                  text=f"Test Item {i+1} - This should be scrollable",
                                  bg='lightgray')
            test_label.pack(pady=15)

        self.update_scroll_region()

    def clear_images(self):
        """Clear all selected images"""
        if self.selected_images:
            result = messagebox.askyesno("Clear Images",
                                         f"Remove all {len(self.selected_images)} images?")
            if result:
                # Clear all data
                self.selected_images.clear()
                self.image_thumbnails.clear()
                self.image_checkboxes.clear()

                # Destroy all thumbnail widgets
                for widget in self.thumbnail_widgets:
                    widget.destroy()
                self.thumbnail_widgets.clear()

                # Clear preview
                self.update_preview_sequence()  # This will show empty state

                self.update_info()
                self.status_var.set("All images cleared")

    def show_preview(self, image_path):
        """Show image preview - now handled by update_preview_sequence"""
        # This method is kept for compatibility but the preview is now
        # handled automatically by update_preview_sequence when checkboxes change
        pass

    def toggle_watermark(self):
        """Toggle watermark entry"""
        if self.watermark_var.get():
            self.watermark_entry.config(state='normal')
        else:
            self.watermark_entry.config(state='disabled')

    def update_info(self):
        """Update image count info"""
        total_count = len(self.selected_images)

        # Count checked images
        checked_count = 0
        if hasattr(self, 'image_checkboxes'):
            for checkbox_var in self.image_checkboxes:
                if checkbox_var.get():
                    checked_count += 1

        if total_count == 0:
            self.info_label.config(text="No images imported")
        elif checked_count == total_count:
            self.info_label.config(
                text=f"Images: {total_count} (all selected)")
        else:
            self.info_label.config(
                text=f"Images: {checked_count}/{total_count} selected")

    def get_page_dimensions(self, page_size):
        """Get page dimensions in pixels (at 72 DPI)"""
        # Common page sizes in inches, converted to pixels at 72 DPI
        page_sizes = {
            "A4": (595, 842),      # 8.27 × 11.69 inches
            "Letter": (612, 792),  # 8.5 × 11 inches
            "Legal": (612, 1008),  # 8.5 × 14 inches
            "A3": (842, 1191)      # 11.69 × 16.54 inches
        }
        return page_sizes.get(page_size, (595, 842))  # Default to A4

    def resize_image_for_page(self, img, page_size, fit_mode="Fit to Page", margin=50):
        """Resize image to fit within page dimensions based on fit mode"""
        if fit_mode == "Original Size":
            return img

        page_width, page_height = self.get_page_dimensions(page_size)

        # Calculate available space (page size minus margins)
        available_width = page_width - (2 * margin)
        available_height = page_height - (2 * margin)

        # Get current image dimensions
        img_width, img_height = img.size

        if fit_mode == "Fit to Page":
            # Scale to fit completely within page (maintains aspect ratio)
            width_scale = available_width / img_width
            height_scale = available_height / img_height
            scale_factor = min(width_scale, height_scale, 1.0)  # Don't upscale

        elif fit_mode == "Fill Page":
            # Scale to fill the page (may crop, maintains aspect ratio)
            width_scale = available_width / img_width
            height_scale = available_height / img_height
            scale_factor = max(width_scale, height_scale)  # Fill entire page

        else:  # Original Size
            return img

        # Calculate new dimensions
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        # Resize image
        if scale_factor != 1.0:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # For "Fill Page" mode, crop if necessary to fit exact page dimensions
        if fit_mode == "Fill Page":
            if new_width > available_width or new_height > available_height:
                # Calculate crop box to center the image
                left = max(0, (new_width - available_width) // 2)
                top = max(0, (new_height - available_height) // 2)
                right = left + min(available_width, new_width)
                bottom = top + min(available_height, new_height)

                img = img.crop((left, top, right, bottom))

        return img

    def export_pdf(self):
        """Export images to PDF"""
        if not self.selected_images:
            messagebox.showwarning(
                "No Images", "Please select some images first.")
            return

        # Get only checked images
        checked_images = []
        for i, is_checked in enumerate(self.image_checkboxes):
            if is_checked.get():
                checked_images.append(self.selected_images[i])

        if not checked_images:
            messagebox.showwarning(
                "No Images Selected", "Please check at least one image to export.")
            return

        if not PIL_AVAILABLE:
            messagebox.showerror("Missing Library",
                                 "Pillow (PIL) library is required for PDF export.\\n\\n"
                                 "Please install it with: pip install Pillow")
            return

        # Get save location
        pdf_path = filedialog.asksaveasfilename(
            title="Save PDF as...",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not pdf_path:
            return

        try:
            self.status_var.set("Converting images to PDF...")
            self.root.update()

            # Get selected page size and fit mode
            selected_page_size = self.page_size_var.get()
            selected_fit_mode = self.fit_mode_var.get()

            # Process only checked images
            pdf_images = []
            for i, image_path in enumerate(checked_images):
                # Update progress
                progress = f"Processing image {i+1}/{len(checked_images)} - Loading..."
                self.status_var.set(progress)
                self.root.update()

                # Load and convert image
                img = Image.open(image_path)
                img = img.convert('RGB')

                # Update progress
                progress = f"Processing image {i+1}/{len(checked_images)} - Resizing for {selected_page_size}..."
                self.status_var.set(progress)
                self.root.update()

                # Resize image to fit page size
                img = self.resize_image_for_page(
                    img, selected_page_size, selected_fit_mode)

                # Add watermark if enabled
                if self.watermark_var.get():
                    progress = f"Processing image {i+1}/{len(checked_images)} - Adding watermark..."
                    self.status_var.set(progress)
                    self.root.update()
                    img = self.add_watermark(img)

                pdf_images.append(img)

            # Save PDF
            self.status_var.set("Saving PDF...")
            self.root.update()

            if pdf_images:
                pdf_images[0].save(pdf_path, save_all=True,
                                   append_images=pdf_images[1:])

            # Success
            self.status_var.set(
                f"PDF saved successfully: {os.path.basename(pdf_path)}")

            result = messagebox.askyesno("Success",
                                         f"PDF created successfully!\\n\\n"
                                         f"Location: {pdf_path}\\n\\n"
                                         f"Open the file?")
            if result:
                os.startfile(pdf_path)

        except Exception as e:
            error_msg = f"Error creating PDF: {str(e)}"
            self.status_var.set("Export failed")
            messagebox.showerror("Export Error", error_msg)

    def add_watermark(self, image):
        """Add watermark to image"""
        if not self.watermark_text_var.get().strip():
            return image

        try:
            watermark_img = image.copy()
            draw = ImageDraw.Draw(watermark_img)
            text = self.watermark_text_var.get().strip()

            # Try to load font
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()

            # Get text dimensions
            try:
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                text_width, text_height = draw.textsize(text, font=font)

            # Position watermark
            x = watermark_img.width - text_width - 20
            y = watermark_img.height - text_height - 20

            # Draw watermark with shadow
            draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))

            return watermark_img

        except Exception as e:
            print(f"Watermark error: {e}")
            return image
