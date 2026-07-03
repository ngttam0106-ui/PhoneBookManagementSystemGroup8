import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService


class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Phone Book Management System")
        self.root.geometry("500x420")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        # ===== Title =====
        title = tk.Label(
            self.root,
            text="PHONE BOOK MANAGEMENT",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=25)

        # ===== Email =====

        email_label = tk.Label(
            self.root,
            text="Email",
            font=("Arial", 11)
        )

        email_label.pack(anchor="w", padx=60)

        self.email_entry = tk.Entry(
            self.root,
            width=35,
            font=("Arial", 11)
        )

        self.email_entry.pack(ipady=4)

        # ===== Password =====

        password_label = tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        )

        password_label.pack(anchor="w", padx=60, pady=(15, 0))

        self.password_entry = tk.Entry(
            self.root,
            width=35,
            font=("Arial", 11),
            show="*"
        )

        self.password_entry.pack(ipady=4)

        # ===== Login Button =====

        login_btn = tk.Button(
            self.root,
            text="Login",
            width=18,
            font=("Arial", 11),
            command=self.login
        )

        login_btn.pack(pady=25)

        # ===== Register Button =====

        register_btn = tk.Button(
            self.root,
            text="Register",
            width=18,
            font=("Arial", 11),
            command=self.open_register
        )

        register_btn.pack()

        # ===== Exit Button =====

        exit_btn = tk.Button(
            self.root,
            text="Exit",
            width=18,
            bg="red",
            fg="white",
            font=("Arial", 11),
            command=self.root.quit
        )

        exit_btn.pack(pady=18)

    # ===================================

    def login(self):

        email = self.email_entry.get().strip()

        password = self.password_entry.get()

        success, user = AuthService.login(
            email,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                f"Welcome {user.full_name}"
            )

            self.open_main(user)

        else:

            messagebox.showerror(
                "Login Failed",
                "Incorrect email or password."
            )

    # ===================================

    def open_register(self):

        from ui.register_window import RegisterWindow

        register = tk.Toplevel(self.root)

        RegisterWindow(register)

    # ===================================

    def open_main(self, current_user):

        self.root.withdraw()

        from ui.main_window import MainWindow

        new_window = tk.Toplevel()

        MainWindow(
            new_window,
            current_user,
            self.root
        )