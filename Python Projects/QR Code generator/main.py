import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

# Global variable for QR image
qr_image = None

# Generate QR Code
def generate_qr():
    global qr_image

    data = entry.get()

    if not data:
        messagebox.showwarning("Warning", "Please enter text or URL")
        return

    # Create QR code
    qr = qrcode.make(data)

    # Resize image for display
    qr = qr.resize((200, 200))

    qr_image = qr

    # Convert image for Tkinter
    tk_image = ImageTk.PhotoImage(qr)

    # Show image in label
    qr_label.config(image=tk_image)
    qr_label.image = tk_image

    # Show save button
    save_btn.pack(pady=10)


# Save QR Code
def save_qr():
    global qr_image

    if qr_image is None:
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")],
        title="Save QR Code"
    )

    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("Success", "QR Code Saved Successfully!")


# Main Window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x500")
root.resizable(False, False)

# Heading
title = tk.Label(
    root,
    text="QR Code Generator",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

# Input Field
entry = tk.Entry(root, width=35, font=("Arial", 12))
entry.pack(pady=10)

# Generate Button
generate_btn = tk.Button(
    root,
    text="Generate QR",
    command=generate_qr,
    bg="blue",
    fg="white",
    font=("Arial", 12)
)
generate_btn.pack(pady=10)

# QR Code Display Label
qr_label = tk.Label(root)
qr_label.pack(pady=20)

# Save Button (hidden initially)
save_btn = tk.Button(
    root,
    text="Save QR Code",
    command=save_qr,
    bg="green",
    fg="white",
    font=("Arial", 12)
)

# Run App
root.mainloop()