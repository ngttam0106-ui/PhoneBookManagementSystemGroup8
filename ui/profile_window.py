import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from services.file_manager import FileManager
from services.auth_service import AuthService


class ProfileWindow:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user

        self.root.title("User Profile")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.avatar_path = current_user.avatar
        self.avatar_image = None
        self.avatar_size = (150, 150)  # Kích thước khung và ảnh

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="USER PROFILE", font=("Arial", 18, "bold")).pack(pady=20)

        # Full Name
        tk.Label(self.root, text="Full Name").pack(anchor="w", padx=60)
        self.full_name_entry = tk.Entry(self.root, width=35)
        self.full_name_entry.insert(0, self.current_user.full_name)
        self.full_name_entry.pack(ipady=4)

        # Email
        tk.Label(self.root, text="Email").pack(anchor="w", padx=60, pady=(10, 0))
        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.insert(0, self.current_user.email)
        self.email_entry.config(state="disabled")
        self.email_entry.pack(ipady=4)

        # Phone
        tk.Label(self.root, text="Phone Number").pack(anchor="w", padx=60, pady=(10, 0))
        self.phone_entry = tk.Entry(self.root, width=35)
        self.phone_entry.insert(0, self.current_user.phone)
        self.phone_entry.pack(ipady=4)

        # Avatar Label - Định hình khung 150x150 cố định
        tk.Label(self.root, text="Avatar").pack(anchor="w", padx=60, pady=(20, 0))
        self.avatar_label = tk.Label(self.root, width=20, height=10, relief="solid", bd=1)
        self.avatar_label.config(width=self.avatar_size[0], height=self.avatar_size[1])
        self.avatar_label.pack(pady=10)

        self.load_avatar()

        tk.Button(self.root, text="Choose Avatar", width=20, command=self.choose_avatar).pack()

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)

        tk.Button(button_frame, text="Save Changes", width=15, command=self.save_profile).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel", width=15, command=self.root.destroy).grid(row=0, column=1, padx=10)

    def load_avatar(self):
        if self.avatar_path and os.path.exists(self.avatar_path):
            try:
                image = Image.open(self.avatar_path)
                # Dùng ImageOps.fit để cắt ảnh chuẩn 150x150 không méo
                image = ImageOps.fit(image, self.avatar_size, Image.Resampling.LANCZOS)
                self.avatar_image = ImageTk.PhotoImage(image)
                self.avatar_label.config(image=self.avatar_image, text="")
            except Exception:
                self.avatar_label.config(image="", text="Load Error")
        else:
            self.avatar_label.config(image="", text="No Avatar")

    def choose_avatar(self):
        # Tạm tắt topmost để không đè cửa sổ chọn file
        self.root.attributes("-topmost", False)
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        self.root.attributes("-topmost", True)

        if file_path:
            self.avatar_path = file_path
            self.load_avatar()

    def save_profile(self):
        full_name = self.full_name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        success, message = AuthService.update_profile(
            self.current_user.user_id, full_name, phone, self.avatar_path
        )

        if success:
            self.current_user.full_name = full_name
            self.current_user.phone = phone
            self.current_user.avatar = self.avatar_path
            messagebox.showinfo("Success", message)
            self.root.destroy()
        else:
            messagebox.showerror("Update Failed", message)