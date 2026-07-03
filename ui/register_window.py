import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService


class RegisterWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Register")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="REGISTER ACCOUNT",
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

        self.phone_entry.pack(ipady=4)

        # ==========================
        # Password
        # ==========================

        tk.Label(
            self.root,
            text="Password"
        ).pack(anchor="w", padx=60, pady=(10,0))

        self.password_entry = tk.Entry(
            self.root,
            width=35,
            show="*"
        )

        self.password_entry.pack(ipady=4)

        # ==========================
        # Confirm Password
        # ==========================

        tk.Label(
            self.root,
            text="Confirm Password"
        ).pack(anchor="w", padx=60, pady=(10,0))

        self.confirm_entry = tk.Entry(
            self.root,
            width=35,
            show="*"
        )

        self.confirm_entry.pack(ipady=4)

        # ==========================
        # Button
        # ==========================

        tk.Button(
            self.root,
            text="Register",
            width=18,
            command=self.register
        ).pack(pady=25)

        tk.Button(
            self.root,
            text="Back",
            width=18,
            command=self.root.destroy
        ).pack()

    # =======================================

    def register(self):

        full_name = self.full_name_entry.get()

        email = self.email_entry.get()

        phone = self.phone_entry.get()

        password = self.password_entry.get()

        confirm = self.confirm_entry.get()

        success, message = AuthService.register(
            full_name,
            email,
            phone,
            password,
            confirm
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.clear_form()

            self.root.destroy()

        else:

            messagebox.showerror(
                "Register Failed",
                message
            )

    # =======================================

    def clear_form(self):

        self.full_name_entry.delete(0, tk.END)

        self.email_entry.delete(0, tk.END)

        self.phone_entry.delete(0, tk.END)

        self.password_entry.delete(0, tk.END)

        self.confirm_entry.delete(0, tk.END)