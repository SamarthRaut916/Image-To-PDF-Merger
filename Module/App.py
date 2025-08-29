import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter - Professional Edition")
        self.root.state('zoomed')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.selected_images = []
        self.image_thumbnails = []
        self.selected_image_vars = []
        self.right_panel_widgets = {}
        self.resized_images_for_pdf = {}

        self.image_count_var = tk.StringVar(value="Images Selected: 0")
        self.apply_watermark = tk.BooleanVar(value=False)
        self.watermark_text_var = tk.StringVar(value="Samarth Raut")

        self.setup_ui()

    def setup_ui(self):
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        if DND_AVAILABLE:
            self.setup_drag_drop()

    def create_left_panel(self):
        left_frame = tk.Frame(self.root, bg="#E8F4FD")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)

        header_frame = tk.Frame(left_frame, bg="#E8F4FD")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)

        import_btn = tk.Button(
            header_frame,
            text="📁 Import Images",
            command=self.import_images,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padx=20,
            pady=8
        )
        import_btn.grid(row=0, column=0, sticky="w")

        count_label = tk.Label(
            header_frame,
            textvariable=self.image_count_var,
            bg="#E8F4FD",
            font=("Arial", 10),
            fg="#333"
        )
        count_label.grid(row=0, column=1, sticky="e")

        if not DND_AVAILABLE:
            info_label = tk.Label(
                header_frame,
                text="(Drag & Drop not available)",
                bg="#E8F4FD",
                font=("Arial", 8),
                fg="#666"
            )
            info_label.grid(row=1, column=0, columnspan=2,
                            sticky="w", pady=(2, 0))

        canvas_frame = tk.Frame(left_frame, bg="#E8F4FD")
        canvas_frame.grid(row=1, column=0, sticky="nsew",
                          padx=10, pady=(0, 10))
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)

        self.images_canvas = tk.Canvas(
            canvas_frame, bg="white", highlightthickness=1, highlightbackground="#DDD")
        scrollbar = tk.Scrollbar(
            canvas_frame, orient="vertical", command=self.images_canvas.yview)
        self.images_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky="ns")
        self.images_canvas.grid(row=0, column=0, sticky="nsew")

        self.images_container = tk.Frame(self.images_canvas, bg="white")
        self.images_canvas.create_window(
            (0, 0), window=self.images_container, anchor="nw")
        self.images_container.bind("<Configure>", self.update_scroll_region)

        self.left_frame = left_frame

    def create_center_panel(self):
        center_frame = tk.Frame(self.root, bg="#F5F5F5", width=100)
        center_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        center_frame.grid_propagate(False)

        add_btn = tk.Button(
            center_frame,
            text="➕\nAdd\nMore",
            command=self.import_images,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            pady=20
        )
        add_btn.pack(expand=True)

    def create_right_panel(self):
        right_frame = tk.Frame(self.root, bg="#FFF3E0")
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        preview_label = tk.Label(
            right_frame,
            text="📋 Selected Images Preview",
            bg="#FFF3E0",
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        preview_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        canvas_frame = tk.Frame(right_frame, bg="#FFF3E0")
        canvas_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)

        self.right_canvas = tk.Canvas(
            canvas_frame, bg="white", highlightthickness=1, highlightbackground="#DDD")
        right_scrollbar = tk.Scrollbar(
            canvas_frame, orient="vertical", command=self.right_canvas.yview)
        self.right_canvas.configure(yscrollcommand=right_scrollbar.set)

        right_scrollbar.grid(row=0, column=1, sticky="ns")
        self.right_canvas.grid(row=0, column=0, sticky="nsew")

        self.right_scrollable_frame = tk.Frame(self.right_canvas, bg="white")
        self.right_canvas.create_window(
            (0, 0), window=self.right_scrollable_frame, anchor="nw")
        self.right_scrollable_frame.bind(
            "<Configure>", self.update_scroll_region)

        controls_frame = tk.Frame(right_frame, bg="#FFF3E0")
        controls_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        controls_frame.grid_columnconfigure(0, weight=1)

        watermark_check = tk.Checkbutton(
            controls_frame,
            text="🔖 Add Watermark",
            variable=self.apply_watermark,
            command=self.toggle_watermark,
            bg="#FFF3E0",
            font=("Arial", 10),
            anchor="w"
        )
        watermark_check.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.watermark_entry = tk.Entry(
            controls_frame,
            textvariable=self.watermark_text_var,
            state="disabled",
            font=("Arial", 10)
        )
        self.watermark_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        save_btn = tk.Button(
            controls_frame,
            text="💾 Save as PDF",
            command=self.save_as_pdf,
            bg="#FF5722",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="flat",
            pady=15
        )
        save_btn.grid(row=2, column=0, sticky="ew")

    def setup_drag_drop(self):
        if DND_AVAILABLE:
            self.left_frame.drop_target_register(DND_FILES)
            self.left_frame.dnd_bind('<<Drop>>', self.handle_drop)

        self.images_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def import_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]
        )
        if files:
            self.selected_images.extend(files)
            self.image_count_var.set(
                f"Images Selected: {len(self.selected_images)}")
            self.display_images(files)

    def handle_drop(self, event):
        if DND_AVAILABLE:
            dropped_files = self.root.tk.splitlist(event.data)
            image_files = [
                file_path for file_path in dropped_files
                if os.path.splitext(file_path)[1].lower() in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"]
            ]
            if image_files:
                self.selected_images.extend(image_files)
                self.image_count_var.set(
                    f"Images Selected: {len(self.selected_images)}")
                self.display_images(image_files)

    def display_images(self, image_paths):
        row, col = 0, 0
        for path in image_paths:
            try:
                img = Image.open(path)
                img.thumbnail((120, 120))
                img_tk = ImageTk.PhotoImage(img)
                self.image_thumbnails.append(img_tk)

                frame = tk.Frame(self.images_container, bg="white",
                                 relief="solid", borderwidth=1, padx=5, pady=5)
                frame.grid(row=row, column=col, padx=5, pady=5, sticky="nw")

                lbl = tk.Label(frame, image=img_tk, bg="white")
                lbl.pack()

                filename = os.path.basename(path)
                if len(filename) > 15:
                    filename = filename[:12] + "..."

                name_lbl = tk.Label(frame, text=filename, bg="white", font=(
                    "Arial", 8), wraplength=120)
                name_lbl.pack()

                var = tk.BooleanVar(value=True)
                chk = tk.Checkbutton(
                    frame,
                    text="✓ Include",
                    variable=var,
                    bg="white",
                    font=("Arial", 8),
                    command=lambda p=path, v=var: self.update_right_panel(p, v)
                )
                chk.pack()

                self.selected_image_vars.append((path, var))
                self.update_right_panel(path, var)

                col += 1
                if col >= 3:
                    col = 0
                    row += 1

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not load image: {os.path.basename(path)}")

    def update_right_panel(self, path, var):
        if var.get():
            try:
                img = Image.open(path)
                img = img.convert("RGB")
                img.thumbnail((250, 250))
                self.resized_images_for_pdf[path] = img.copy()

                img_tk = ImageTk.PhotoImage(img)
                self.image_thumbnails.append(img_tk)

                frame = tk.Frame(self.right_scrollable_frame, bg="white",
                                 relief="solid", borderwidth=1, padx=10, pady=10)
                frame.pack(fill="x", padx=10, pady=5)

                lbl = tk.Label(frame, image=img_tk, bg="white")
                lbl.image = img_tk
                lbl.pack()

                name_lbl = tk.Label(frame, text=os.path.basename(
                    path), bg="white", font=("Arial", 10))
                name_lbl.pack()

                self.right_panel_widgets[path] = frame

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not process image: {os.path.basename(path)}")
        else:
            widget = self.right_panel_widgets.pop(path, None)
            self.resized_images_for_pdf.pop(path, None)
            if widget:
                widget.destroy()

    def add_watermark(self, image, text="Samarth Raut"):
        watermark_img = image.copy()
        draw = ImageDraw.Draw(watermark_img)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 24)
            except:
                font = ImageFont.load_default()

        try:
            bbox = font.getbbox(text)
            textwidth = bbox[2] - bbox[0]
            textheight = bbox[3] - bbox[1]
        except AttributeError:
            textwidth, textheight = draw.textsize(text, font=font)

        x = watermark_img.width - textwidth - 20
        y = watermark_img.height - textheight - 20

        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 100))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))

        return watermark_img

    def save_as_pdf(self):
        selected_files = [path for path,
                          var in self.selected_image_vars if var.get()]
        if not selected_files:
            messagebox.showwarning(
                "No Selection", "Please select at least one image.")
            return

        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as..."
        )
        if not pdf_path:
            return

        try:
            image_list = []
            for path in selected_files:
                img = self.resized_images_for_pdf.get(path)
                if img:
                    if self.apply_watermark.get():
                        text = self.watermark_text_var.get().strip() or "Samarth Raut"
                        img = self.add_watermark(img, text=text)
                    image_list.append(img)

            if image_list:
                image_list[0].save(pdf_path, save_all=True,
                                   append_images=image_list[1:])
                messagebox.showinfo(
                    "Success", f"PDF saved successfully!\n{pdf_path}")
            else:
                messagebox.showerror("Error", "No images to save.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

    def toggle_watermark(self):
        if self.apply_watermark.get():
            self.watermark_entry.configure(state="normal")
        else:
            self.watermark_entry.configure(state="disabled")

    def update_scroll_region(self, event=None):
        self.images_canvas.configure(
            scrollregion=self.images_canvas.bbox("all"))
        self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.images_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
