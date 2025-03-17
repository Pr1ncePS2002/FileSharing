import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import os
from PIL import Image, ImageTk

# Paths to Images
BACKGROUND_IMG = "C:/Projects/FileSharing/images/background.jpg"
ICON_IMG = "C:/Projects/FileSharing/images/icon.png"
SEND_IMG = "C:/Projects/FileSharing/images/send.png"
RECEIVE_IMG = "C:/Projects/FileSharing/images/receive.png"
PROFILE_IMG = "C:/Projects/FileSharing/images/share.png"

# GUI Setup
root = tk.Tk()
root.title("FileShare - Sender")
root.geometry("500x500")
root.configure(bg="#f0f0f0")
root.resizable(False, False)
root.iconphoto(False, tk.PhotoImage(file=ICON_IMG))

# Load Images
bg_image = Image.open(BACKGROUND_IMG).resize((500, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

send_image = Image.open(SEND_IMG).resize((40, 40))
send_photo = ImageTk.PhotoImage(send_image)

receive_image = Image.open(RECEIVE_IMG).resize((40, 40))
receive_photo = ImageTk.PhotoImage(receive_image)

profile_image = Image.open(PROFILE_IMG).resize((50, 50))
profile_photo = ImageTk.PhotoImage(profile_image)

# Background Label
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title
title_label = tk.Label(root, text="FileShare", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2196F3")
title_label.pack(pady=10)

# Profile Icon
profile_label = tk.Label(root, image=profile_photo, bg="#f0f0f0")
profile_label.pack()

# File Selection
file_label = tk.Label(root, text="No file selected", font=("Arial", 12), bg="#f0f0f0", fg="black")
file_label.pack(pady=5)

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        file_label.config(text=f"Selected File: {os.path.basename(file_path)}")
        messagebox.showinfo("File Selected", f"You selected: {file_path}")

select_button = tk.Button(root, text="Select File", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=select_file)
select_button.pack(pady=10)

# IP Address Input
ip_label = tk.Label(root, text="Receiver's IP Address:", font=("Arial", 12), bg="#f0f0f0", fg="black")
ip_label.pack()

ip_entry = tk.Entry(root, width=20, font=("Arial", 12), bd=2, relief="solid", fg="black", bg="white")
ip_entry.pack(pady=5)
ip_entry.config(highlightbackground="navy", highlightcolor="navy", highlightthickness=1)


def send_file():
    receiver_ip = ip_entry.get()
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return
    if not receiver_ip:
        messagebox.showerror("Error", "Enter receiver's IP address!")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((receiver_ip, 12345))
        file_name = os.path.basename(file_path)
        client_socket.send(file_name.encode())
        with open(file_path, "rb") as file:
            while (data := file.read(1024)):
                client_socket.send(data)
        messagebox.showinfo("Success", "File sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file: {e}")
    finally:
        client_socket.close()

send_button = tk.Button(root, image=send_photo, bg="#4CAF50", command=send_file)
send_button.pack(pady=10)

root.mainloop()
