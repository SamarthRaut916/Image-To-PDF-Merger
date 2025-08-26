from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# Global variables
selected_images = []
image_thumbnails = []
selected_image_vars = []
right_panel_widgets = {}
resized_images_for_pdf = {}

def import_image():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if files:
        selected_images.extend(files)
        image_count_var.set(f"Images Selected: {len(selected_images)}")
        display_images(files)

def handle_drop(data):
    dropped_files = root.tk.splitlist(data)
    image_files = []

    for file_path in dropped_files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
            image_files.append(file_path)

    if image_files:
        selected_images.extend(image_files)
        image_count_var.set(f"Images Selected: {len(selected_images)}")
        display_images(image_files)

def display_images(image_paths):
    row, col = 0, 0
    for path in image_paths:
        try:
            img = Image.open(path)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            image_thumbnails.append(img_tk)

            frame = tk.Frame(images_container, bg="#f0f0f0", padx=5, pady=5, highlightthickness=1, highlightbackground="#ccc")
            frame.grid(row=row, column=col, sticky="nw", padx=10, pady=10)

            lbl = tk.Label(frame, image=img_tk, bg="#f0f0f0")
            lbl.pack()

            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(
                frame, text="Select", variable=var,
                command=lambda p=path, v=var: update_right_panel(p, v)
            )
            chk.pack()

            selected_image_vars.append((path, var))
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
            resized_images_for_pdf[path] = img.copy()

            img_tk = ImageTk.PhotoImage(img)
            image_thumbnails.append(img_tk)

            lbl = tk.Label(right_scrollable_frame, image=img_tk, bg="white", bd=1, relief="solid")
            lbl.image = img_tk
            lbl.pack(pady=5)
            right_panel_widgets[path] = lbl
        except Exception as e:
            print(f"Error displaying image in right panel: {e}")
    else:
        widget = right_panel_widgets.pop(path, None)
        resized_images_for_pdf.pop(path, None)
        if widget:
            widget.destroy()

def add_watermark(image, text="Samarth Raut"):
    watermark_img = image.copy()
    draw = ImageDraw.Draw(watermark_img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    textwidth, textheight = draw.textsize(text, font)
    x = watermark_img.width - textwidth - 10
    y = watermark_img.height - textheight - 10

    draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 128))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))

    return watermark_img

def save_as_pdf():
    selected_files = [path for path, var in selected_image_vars if var.get()]
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
        img = resized_images_for_pdf.get(path)
        if img:
            watermarked_img = add_watermark(img)
            image_list.append(watermarked_img)
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

# ---------- GUI Setup ---------- #

root = TkinterDnD.Tk()
root.title("📸 Stylish Image to PDF Exporter")
root.geometry("1100x600")
root.configure(bg="#e1f5fe")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6, background="#039be5", foreground="white")
style.configure("TCheckbutton", font=("Segoe UI", 9), background="#f0f0f0")
style.map("TButton", background=[("active", "#0277bd")])

root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# LEFT PANEL
left_frame = tk.Frame(root, bg="#b3e5fc", width=520)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.grid_propagate(False)

tk.Label(left_frame, text="📂 Image Import Panel", bg="#b3e5fc", font=("Segoe UI", 12, "bold")).pack(pady=10)
ttk.Button(left_frame, text="Import Images", command=import_image).pack(pady=5)

image_count_var = tk.StringVar(value="Images Selected: 0")
checkbox_var = tk.BooleanVar()
ttk.Checkbutton(left_frame, textvariable=image_count_var, variable=checkbox_var).pack(pady=5)

canvas_frame = tk.Frame(left_frame, bg="#b3e5fc")
canvas_frame.pack(fill="both", expand=True, pady=5)

images_canvas = tk.Canvas(canvas_frame, bg="#b3e5fc", highlightthickness=0)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=images_canvas.yview)
images_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
images_canvas.pack(side="left", fill="both", expand=True)

images_container = tk.Frame(images_canvas, bg="#ffffff")
images_canvas.create_window((0, 0), window=images_container, anchor="nw")
images_container.bind("<Configure>", update_scroll_region)

left_frame.drop_target_register(DND_FILES)
left_frame.dnd_bind('<<Drop>>', lambda e: handle_drop(e.data))

# CENTER LINE
center_frame = tk.Frame(root, width=20, bg="#01579b")
center_frame.grid(row=0, column=1, sticky="ns")

ttk.Button(root, text="Add Image", command=import_image).grid(row=0, column=1, padx=5, pady=250)

# RIGHT PANEL
right_frame = tk.Frame(root, bg="#c8e6c9", width=520)
right_frame.grid(row=0, column=2, sticky="nsew")
right_frame.grid_propagate(False)

tk.Label(right_frame, text="🖼️ Selected Image Preview", bg="#c8e6c9", font=("Segoe UI", 12, "bold")).pack(pady=10)

right_canvas_frame = tk.Frame(right_frame)
right_canvas_frame.pack(fill="both", expand=True, pady=10)

right_canvas = tk.Canvas(right_canvas_frame, bg="#ffffff", highlightthickness=0)
right_scrollbar = ttk.Scrollbar(right_canvas_frame, orient="vertical", command=right_canvas.yview)
right_canvas.configure(yscrollcommand=right_scrollbar.set)

right_scrollbar.pack(side="right", fill="y")
right_canvas.pack(side="left", fill="both", expand=True)

right_scrollable_frame = tk.Frame(right_canvas, bg="#ffffff")
right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
right_scrollable_frame.bind("<Configure>", update_scroll_region)

ttk.Button(right_frame, text="💾 Save as PDF", command=save_as_pdf).pack(pady=10)

# Mouse scroll
images_canvas.bind_all("<MouseWheel>", _on_mousewheel)
images_canvas.bind_all("<Button-4>", lambda e: images_canvas.yview_scroll(-1, "units"))
images_canvas.bind_all("<Button-5>", lambda e: images_canvas.yview_scroll(1, "units"))

root.mainloop()
