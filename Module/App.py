import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Exporter with Optional Watermark")

        # Start in zoomed window
        self.root.state('zoomed')

        # Configure grid columns and rows to resize
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Optional: Press Esc to exit fullscreen mode
        def exit_fullscreen(event=None):
            self.root.attributes("-fullscreen", False)
            self.root.state('normal')

        self.root.bind("<Escape>", exit_fullscreen)

        # ---------- Tkinter Variables (after root) ---------- #
        self.selected_images = []
        self.image_thumbnails = []
        self.selected_image_vars = []
        self.right_panel_widgets = {}
        self.resized_images_for_pdf = {}

        self.image_count_var = tk.StringVar(master=self.root, value="Images Selected: 0")
        self.checkbox_var = tk.BooleanVar(master=self.root)

        self.apply_watermark = tk.BooleanVar(master=self.root, value=False)
        self.watermark_text_var = tk.StringVar(master=self.root, value="Samarth Raut")

        # ---------- Functions ---------- #
        def import_image():
            files = filedialog.askopenfilenames(
                title="Select Images",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if files:
                self.selected_images.extend(files)
                self.image_count_var.set(f"Images Selected: {len(self.selected_images)}")
                display_images(files)

        def handle_drop(data):
            dropped_files = self.root.tk.splitlist(data)
            image_files = [
                file_path for file_path in dropped_files
                if os.path.splitext(file_path)[1].lower() in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
            ]
            if image_files:
                self.selected_images.extend(image_files)
                self.image_count_var.set(f"Images Selected: {len(self.selected_images)}")
                display_images(image_files)

        def display_images(image_paths):
            row, col = 0, 0
            for path in image_paths:
                try:
                    img = Image.open(path)
                    img.thumbnail((100, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    self.image_thumbnails.append(img_tk)

                    frame = tk.Frame(images_container, bg="white", padx=5, pady=5)
                    frame.grid(row=row, column=col, sticky="nw")

                    lbl = tk.Label(frame, image=img_tk, bg="white")
                    lbl.pack()

                    var = tk.BooleanVar(value=True)
                    chk = tk.Checkbutton(
                        frame, text="Select", variable=var, bg="white",
                        command=lambda p=path, v=var: update_right_panel(p, v)
                    )
                    chk.pack()

                    self.selected_image_vars.append((path, var))
                    update_right_panel(path, var)

                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1

                except Exception as e:
                    print(f"Error loading image {path}: {e}")

        def update_right_panel(path, var):
            if var.get():
                try:
                    img = Image.open(path)
                    img = img.convert("RGB")
                    img.thumbnail((200, 200))
                    self.resized_images_for_pdf[path] = img.copy()

                    img_tk = ImageTk.PhotoImage(img)
                    self.image_thumbnails.append(img_tk)

                    lbl = tk.Label(right_scrollable_frame, image=img_tk, bg="white")
                    lbl.image = img_tk
                    lbl.pack(pady=5)
                    self.right_panel_widgets[path] = lbl
                except Exception as e:
                    print(f"Error displaying image in right panel: {e}")
            else:
                widget = self.right_panel_widgets.pop(path, None)
                self.resized_images_for_pdf.pop(path, None)
                if widget:
                    widget.destroy()

        def add_watermark(image, text="Samarth Raut"):
            watermark_img = image.copy()
            draw = ImageDraw.Draw(watermark_img)

            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", 20)
                except:
                    font = ImageFont.load_default()

            try:
                bbox = font.getbbox(text)
                textwidth = bbox[2] - bbox[0]
                textheight = bbox[3] - bbox[1]
            except AttributeError:
                textwidth, textheight = draw.textsize(text, font=font)

            x = watermark_img.width - textwidth - 10
            y = watermark_img.height - textheight - 10

            draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 128))  # shadow
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))  # main text

            return watermark_img

        def save_as_pdf():
            selected_files = [path for path, var in self.selected_image_vars if var.get()]
            if not selected_files:
                print("No images selected.")
                return

            pdf_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save PDF as..."
            )
            if not pdf_path:
                return

            image_list = []
            for path in selected_files:
                img = self.resized_images_for_pdf.get(path)
                if img:
                    if self.apply_watermark.get():
                        text = self.watermark_text_var.get().strip() or "Samarth Raut"
                        img = add_watermark(img, text=text)
                    image_list.append(img)
                else:
                    print(f"Warning: No resized image found for {path}")

            if image_list:
                try:
                    image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
                    print(f"✅ PDF saved to: {pdf_path}")
                except Exception as e:
                    print(f"Failed to save PDF: {e}")

        def update_scroll_region(event):
            images_canvas.configure(scrollregion=images_canvas.bbox("all"))
            right_canvas.configure(scrollregion=right_canvas.bbox("all"))

        def _on_mousewheel(event):
            images_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # ---------- GUI Layout ---------- #
        # Left Panel
        left_frame = tk.Frame(self.root, bg="lightblue")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)

        tk.Button(left_frame, text="Import Images", command=import_image).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Checkbutton(left_frame, textvariable=self.image_count_var, variable=self.checkbox_var).grid(row=0, column=0, padx=100, pady=5, sticky="ew")

        canvas_frame = tk.Frame(left_frame)
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)

        global images_canvas
        images_canvas = tk.Canvas(canvas_frame, bg="lightblue")
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=images_canvas.yview)
        images_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky="ns")
        images_canvas.grid(row=0, column=0, sticky="nsew")

        global images_container
        images_container = tk.Frame(images_canvas, bg="white")
        images_canvas.create_window((0, 0), window=images_container, anchor="nw")
        images_container.bind("<Configure>", update_scroll_region)

        left_frame.drop_target_register(DND_FILES)
        left_frame.dnd_bind('<<Drop>>', lambda e: handle_drop(e.data))

        # Center
        tk.Button(self.root, text="Add Image", command=import_image).grid(row=0, column=1, padx=5, pady=180)

        # Right Panel
        right_frame = tk.Frame(self.root, bg="lightgreen")
        right_frame.grid(row=0, column=2, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)

        right_canvas_frame = tk.Frame(right_frame)
        right_canvas_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
        right_canvas_frame.grid_columnconfigure(0, weight=1)
        right_canvas_frame.grid_rowconfigure(0, weight=1)

        global right_canvas
        right_canvas = tk.Canvas(right_canvas_frame, bg="white")
        right_scrollbar = tk.Scrollbar(right_canvas_frame, orient="vertical", command=right_canvas.yview)
        right_canvas.configure(yscrollcommand=right_scrollbar.set)

        right_scrollbar.grid(row=0, column=1, sticky="ns")
        right_canvas.grid(row=0, column=0, sticky="nsew")

        global right_scrollable_frame
        right_scrollable_frame = tk.Frame(right_canvas, bg="white")
        right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
        right_scrollable_frame.bind("<Configure>", update_scroll_region)

        # Watermark Controls
        tk.Checkbutton(
            right_frame,
            text="Add Watermark",
            variable=self.apply_watermark,
            command=lambda: watermark_entry.configure(state="normal" if self.apply_watermark.get() else "disabled"),
            bg="lightgreen"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        watermark_entry = tk.Entry(right_frame, textvariable=self.watermark_text_var, state="disabled")
        watermark_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        tk.Button(right_frame, text="Save PDF", command=save_as_pdf).grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        # Mouse Scroll
        images_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        images_canvas.bind_all("<Button-4>", lambda e: images_canvas.yview_scroll(-1, "units"))
        images_canvas.bind_all("<Button-5>", lambda e: images_canvas.yview_scroll(1, "units"))
