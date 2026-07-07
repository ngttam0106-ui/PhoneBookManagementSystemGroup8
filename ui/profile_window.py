import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

from services.auth_service import AuthService


class ProfileWindow:

    def __init__(self, root, current_user):

        self.root = root
        self.current_user = current_user

        self.root.title("User Profile")
        self.root.geometry("550x600")
        self.root.resizable(False, False)

        self.avatar_path = current_user.avatar
        self.avatar_image = None

        self.create_widgets()

    # =====================================

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="USER PROFILE",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=20)

        # ================= Full Name =================

        tk.Label(
            self.root,
            text="Full Name"
        ).pack(anchor="w", padx=60)

        self.full_name_entry = tk.Entry(
            self.root,
            width=35
        )

        self.full_name_entry.insert(
            0,
            self.current_user.full_name
        )

        self.full_name_entry.pack(ipady=4)

        # ================= Email =================

        tk.Label(
            self.root,
            text="Email"
        ).pack(anchor="w", padx=60, pady=(10, 0))

        self.email_entry = tk.Entry(
            self.root,
            width=35
        )

        self.email_entry.insert(
            0,
            self.current_user.email
        )

        self.email_entry.config(state="disabled")

        self.email_entry.pack(ipady=4)

        # ================= Phone =================

        tk.Label(
            self.root,
            text="Phone Number"
        ).pack(anchor="w", padx=60, pady=(10, 0))

        self.phone_entry = tk.Entry(
            self.root,
            width=35
        )

        self.phone_entry.insert(
            0,
            self.current_user.phone
        )

        self.phone_entry.pack(ipady=4)

        # ================= Avatar =================

        tk.Label(
            self.root,
            text="Avatar"
        ).pack(anchor="w", padx=60, pady=(20, 0))

        self.avatar_label = tk.Label(
            self.root,
            width=120,
            height=120,
            relief="solid",
            bd=1
        )

        self.avatar_label.pack(pady=10)

        self.load_avatar()

        tk.Button(
            self.root,
            text="Choose Avatar",
            width=20,
            command=self.choose_avatar
        ).pack()

        # ================= Buttons =================

        button_frame = tk.Frame(self.root)

        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="Save Changes",
            width=15,
            command=self.save_profile
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Back",
            width=15,
            command=self.root.destroy
        ).grid(row=0, column=1, padx=10)

    # =====================================

    def load_avatar(self):

        if self.avatar_path and os.path.exists(self.avatar_path):

            try:

                image = Image.open(self.avatar_path)

                image = image.resize((120, 120))

                self.avatar_image = ImageTk.PhotoImage(image)

                self.avatar_label.config(
                    image=self.avatar_image,
                    text=""
                )

            except Exception:

                self.avatar_label.config(
                    image="",
                    text="Cannot load image"
                )

        else:

            self.avatar_label.config(
                image="",
                text="No Avatar"
            )

    # =====================================

    def choose_avatar(self):

        file_path = filedialog.askopenfilename(

            title="Select Avatar",

            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file_path:

            self.avatar_path = file_path

            self.load_avatar()

    # =====================================

    def save_profile(self):

        full_name = self.full_name_entry.get().strip()

        phone = self.phone_entry.get().strip()

        success, message = AuthService.update_profile(

            self.current_user.user_id,

            full_name,

            phone,

            self.avatar_path

        )

        if success:

            self.current_user.full_name = full_name
            self.current_user.phone = phone
            self.current_user.avatar = self.avatar_path

            messagebox.showinfo(
                "Success",
                message
            )

            self.root.destroy()

        else:

            messagebox.showerror(
                "Update Failed",
                message
            )