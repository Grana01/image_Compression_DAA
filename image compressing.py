import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
import threading
import time

# Global variables
image_path = None
compressed_image = None  # Store compressed image globally

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if image_path:
        display_selected_image(image_path)

def display_selected_image(path):
    img = Image.open(path).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    original_image_label.config(image=img_tk)
    original_image_label.image = img_tk

def compress_image():
    if not image_path:
        messagebox.showerror("Error", "Please select an image first!")
        return
    
    progress["value"] = 0  # Reset progress bar
    threading.Thread(target=process_compression, daemon=True).start()

def process_compression():
    global compressed_image
    try:
        threshold = int(threshold_slider.get())
        image = Image.open(image_path).convert('RGB')
        img_array = np.array(image)
        compressed_array = np.copy(img_array)

        total_pixels = img_array.shape[0] * img_array.shape[1]
        processed_pixels = 0

        for row in range(img_array.shape[0]):
            for col in range(img_array.shape[1]):
                compressed_array[row, col] = np.where(img_array[row, col] < threshold, 0, img_array[row, col])
                processed_pixels += 1

                if processed_pixels % 500 == 0:  # Update every 500 pixels
                    progress["value"] = (processed_pixels / total_pixels) * 100
                    root.update_idletasks()
                    time.sleep(0.001)  # Simulate processing delay

        progress["value"] = 100  # Ensure it reaches 100%

        compressed_image = Image.fromarray(compressed_array.astype(np.uint8))
        display_compressed_image(compressed_image)

        status_bar.config(text="Compression completed. Click 'Download Image' to save.")

    except Exception as e:
        status_bar.config(text=f"Error: {str(e)}")

def display_compressed_image(image):
    img = image.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    compressed_image_label.config(image=img_tk)
    compressed_image_label.image = img_tk

def download_image():
    """ Save the last compressed image """
    if compressed_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg")])
        if save_path:
            compressed_image.save(save_path)
            status_bar.config(text=f"Image saved: {os.path.basename(save_path)}")
        else:
            status_bar.config(text="Download canceled.")
    else:
        messagebox.showerror("Error", "No compressed image available. Please compress an image first.")

def update_threshold_value(val):
    threshold_value_label.config(text=f"Threshold: {val}")

# UI Setup
root = tk.Tk()
root.title("Image Compression Tool")
root.geometry("700x550")
root.config(bg="#e0f7fa")

# Main Frame
main_frame = tk.Frame(root, bg="#e0f7fa")
main_frame.pack(pady=20)

# Title
title_label = tk.Label(main_frame, text="Greedy Image Compression", font=("Arial", 18, "bold"), bg="#e0f7fa")
title_label.pack(pady=10)

# Image Selection Button
select_button = tk.Button(main_frame, text="Select Image", command=select_image, bg="#00796b", fg="white", font=("Arial", 12))
select_button.pack(pady=5)

# Threshold Controls
threshold_label = tk.Label(main_frame, text="Threshold (0-255):", bg="#e0f7fa", font=("Arial", 12))
threshold_label.pack(pady=5)

threshold_slider = tk.Scale(main_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=update_threshold_value, bg="#e0f7fa")
threshold_slider.set(128)
threshold_slider.pack(pady=5)

threshold_value_label = tk.Label(main_frame, text="Threshold: 128", bg="#e0f7fa", font=("Arial", 12))
threshold_value_label.pack(pady=5)

# Compression Button
compress_button = tk.Button(main_frame, text="Compress Image", command=compress_image, bg="#00796b", fg="white", font=("Arial", 12))
compress_button.pack(pady=5)

# Download Button
download_button = tk.Button(main_frame, text="Download Image", command=download_image, bg="#ff9800", fg="white", font=("Arial", 12))
download_button.pack(pady=5)

# Image Preview
image_frame = tk.Frame(main_frame, bg="#e0f7fa")
image_frame.pack(pady=10)

original_image_label = tk.Label(image_frame, bg="#c8e6c9", width=200, height=200, bd=2, relief="solid")
original_image_label.grid(row=0, column=0, padx=10)

compressed_image_label = tk.Label(image_frame, bg="#ffcdd2", width=200, height=200, bd=2, relief="solid")
compressed_image_label.grid(row=0, column=1, padx=10)

# Progress Bar
progress_label = tk.Label(main_frame, text="Progress:", bg="#e0f7fa", font=("Arial", 12))
progress_label.pack(pady=5)

progress = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=5)

# Status Bar
status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10), bg="#80cbc4")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
