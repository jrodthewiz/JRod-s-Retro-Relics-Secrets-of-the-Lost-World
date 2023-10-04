import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def select_folder():
    folder_path.set(filedialog.askdirectory())

def update_files():
    folder = folder_path.get()
    scale_value = float(scale_var.get())
    
    for root_dir, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root_dir, file)
            process_file(file_path, scale_value)

def process_file(file_path, scale_value):
    try:
        with Image.open(file_path) as img:
            new_size = (int(img.width * scale_value), int(img.height * scale_value))
            resized_img = img.resize(new_size)
            resized_img.save(file_path)
    except Exception as e:
        print(f"Could not process {file_path}: {e}")

# Create the main window
window = tk.Tk()
window.title("File Scaling Application")

# Create a StringVar() to store the folder path
folder_path = tk.StringVar()
scale_var = tk.StringVar(value='1.0')  # default scale value

# Create and place the widgets
folder_label = tk.Label(window, text="Select Folder:")
folder_label.pack(pady=(10, 0))

folder_entry = tk.Entry(window, textvariable=folder_path, width=50)
folder_entry.pack(pady=5)

folder_button = tk.Button(window, text="Browse", command=select_folder)
folder_button.pack(pady=(0, 10))

scale_label = tk.Label(window, text="Scale Value:")
scale_label.pack(pady=5)

scale_entry = tk.Entry(window, textvariable=scale_var, width=10)
scale_entry.pack(pady=5)

update_button = tk.Button(window, text="Update Files", command=update_files)
update_button.pack(pady=20)

# Run the main event loop
window.mainloop()
