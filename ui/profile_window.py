import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from services.auth_service import AuthService


class ProfileWindow:

    def __init__(self, root, current_user):

        self.root = root
        self.current_user = current_user

        self.root.title("Profile")
        self.root.geometry("550x550")
        self.root.resizable(False, False)

        self.avatar_path = current_user.avatar

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="USER PROFILE",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=20)

        # ==========================
        # Full Name
        # ==========================

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

        # ==========================
        # Email
        # ==========================

        tk.Label(
            self.root,
            text="Email"
        ).pack(anchor="w", padx=60, pady=(10,0))

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

        # ==========================
        # Phone
        # ==========================

        tk.Label(
            self.root,
            text="Phone Number"
        ).pack(anchor="w", padx=60, pady=(10,0))

        self.phone_entry = tk.Entry(
            self.root,
            width=35
        )

        self.phone_entry.insert(
            0,
            self.current_user.phone
        )

        self.phone_entry.pack(ipady=4)

        # ==========================
        # Avatar
        # ==========================

        tk.Button(
            self.root,
            text="Choose Avatar",
            command=self.choose_avatar
        ).pack(pady=20)

        self.avatar_label = tk.Label(
            self.root,
            text=self.avatar_path if self.avatar_path else "No avatar selected"
        )

        self.avatar_label.pack()

        # ==========================
        # Save
        # ==========================

        tk.Button(
            self.root,
            text="Save Changes",
            width=20,
            command=self.save_profile
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Back",
            width=20,
            command=self.root.destroy
        ).pack()

    # ==================================

    def choose_avatar(self):

        file_path = filedialog.askopenfilename(

            title="Select Avatar",

            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file_path:

            self.avatar_path = file_path

            self.avatar_label.config(
                text=file_path
            )

    # ==================================

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
                "Error",
                message
            )