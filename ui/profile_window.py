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

        # Thiết lập cửa sổ
        self.root.title("User Profile")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        # Bỏ topmost để không bị đè cửa sổ chọn file
        self.root.attributes("-topmost", False)

        # Xử lý avatar an toàn: nếu None thì gán chuỗi rỗng
        self.avatar_path = getattr(self.current_user, 'avatar', "") or ""
        self.avatar_image = None
        self.avatar_size = (150, 150)

        self.create_widgets()

    def create_widgets(self):
        # Tiêu đề
        tk.Label(self.root, text="USER PROFILE", font=("Arial", 18, "bold")).pack(pady=20)

        # Full Name
        tk.Label(self.root, text="Full Name").pack(anchor="w", padx=60)
        self.full_name_entry = tk.Entry(self.root, width=35)
        self.full_name_entry.insert(0, self.current_user.full_name or "")
        self.full_name_entry.pack(ipady=4)

        # Email
        tk.Label(self.root, text="Email").pack(anchor="w", padx=60, pady=(10, 0))
        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.insert(0, self.current_user.email or "")
        self.email_entry.config(state="disabled")
        self.email_entry.pack(ipady=4)

        # Phone
        tk.Label(self.root, text="Phone Number").pack(anchor="w", padx=60, pady=(10, 0))
        self.phone_entry = tk.Entry(self.root, width=35)
        self.phone_entry.insert(0, self.current_user.phone or "")
        self.phone_entry.pack(ipady=4)

        # Avatar Label
        tk.Label(self.root, text="Avatar").pack(anchor="w", padx=60, pady=(20, 0))
        self.avatar_label = tk.Label(self.root, width=150, height=150, relief="solid", bd=1)
        self.avatar_label.config(width=20, height=10)  # Kích thước tính theo đơn vị ký tự
        self.avatar_label.pack(pady=10)

        self.load_avatar()

        tk.Button(self.root, text="Choose Avatar", width=20, command=self.choose_avatar).pack()

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)

        tk.Button(button_frame, text="Save Changes", width=15, command=self.save_profile).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel", width=15, command=self.root.destroy).grid(row=0, column=1, padx=10)

    def load_avatar(self):
        target_size = (150, 150)  # Kích thước bạn muốn
        if self.avatar_path and os.path.exists(self.avatar_path):
            try:
                image = Image.open(self.avatar_path)
                # ImageOps.fit tự động cắt ảnh theo tỷ lệ khung hình chuẩn
                image = ImageOps.fit(image, target_size, Image.Resampling.LANCZOS)

                self.avatar_image = ImageTk.PhotoImage(image)
                self.avatar_label.config(image=self.avatar_image, text="", width=150, height=150)
            except Exception:
                self.avatar_label.config(text="Error", width=20, height=10)
        else:
            self.avatar_label.config(text="No Avatar", width=20, height=10)

    def choose_avatar(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.avatar_path = file_path
            self.load_avatar()

    def save_profile(self):
        full_name = self.full_name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Gọi service để update
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