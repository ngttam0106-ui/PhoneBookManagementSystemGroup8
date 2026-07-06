import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from services.contact_service import ContactService
from ui.contact_window import ContactWindow
from ui.group_window import GroupWindow


class MainWindow:

    def __init__(self, root, current_user, login_window):

        self.root = root
        self.current_user = current_user
        self.login_window = login_window

        self.contact_service = ContactService()

        self.root.title("Phone Book Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        self.setup_ui()

    def setup_ui(self):

        # ================= HEADER =================

        header = tk.Frame(
            self.root,
            bg="#1E90FF",
            height=60
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="PHONE BOOK MANAGEMENT SYSTEM",
            bg="#1E90FF",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # ================= LEFT MENU =================

        menu = tk.Frame(
            self.root,
            bg="#EEEEEE",
            width=220
        )

        menu.pack(
            side="left",
            fill="y"
        )

        tk.Label(
            menu,
            text=f"Welcome\n{self.current_user.full_name}",
            bg="#EEEEEE",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        tk.Button(
            menu,
            text="Contacts",
            width=18,
            command=self.show_contacts
        ).pack(pady=10)

        tk.Button(
            menu,
            text="Groups",
            width=18,
            command=self.open_groups
        ).pack(pady=10)

        tk.Button(
            menu,
            text="Profile",
            width=18,
            command=self.open_profile
        ).pack(pady=10)

        tk.Button(
            menu,
            text="Logout",
            width=18,
            bg="red",
            fg="white",
            command=self.logout
        ).pack(side="bottom", pady=30)

        # ================= CONTENT =================

        content = tk.Frame(
            self.root,
            bg="white"
        )

        content.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text="Dashboard",
            bg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        # ================= SEARCH =================

        search_frame = tk.Frame(
            content,
            bg="white"
        )

        search_frame.pack()

        tk.Label(
            search_frame,
            text="Search:",
            bg="white"
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=35
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_contact
        ).pack(side="left")

        # ================= TABLE =================

        columns = (
            "Name",
            "Phone",
            "Email"
        )

        self.table = ttk.Treeview(
            content,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:

            self.table.heading(
                col,
                text=col
            )

            self.table.column(
                col,
                width=220
            )

        self.table.pack(pady=20)

        # Load dữ liệu thật

        self.load_table(
            self.contact_service.get_all_contacts()
        )

        # ================= BUTTON =================

        button_frame = tk.Frame(
            content,
            bg="white"
        )

        button_frame.pack()

        tk.Button(
            button_frame,
            text="Add",
            width=10,
            command=self.show_contacts
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Edit",
            width=10,
            command=self.show_contacts
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=10,
            command=self.show_contacts
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            width=10,
            command=self.refresh_table
        ).grid(row=0, column=3, padx=5)

        # ================= STATUS =================

        tk.Label(
            self.root,
            text="Ready...",
            anchor="w",
            bg="#DDDDDD"
        ).pack(
            fill="x",
            side="bottom"
        )

    # =====================================================

    def load_table(self, contacts):

        for item in self.table.get_children():
            self.table.delete(item)

        for contact in contacts:

            self.table.insert(
                "",
                tk.END,
                values=(
                    contact.name,
                    contact.phone,
                    contact.email
                )
            )

    # =====================================================

    def search_contact(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":

            contacts = self.contact_service.get_all_contacts()

        else:

            contacts = self.contact_service.search_contact(
                keyword
            )

        self.load_table(contacts)

    # =====================================================

    def refresh_table(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.load_table(
            self.contact_service.get_all_contacts()
        )

    # =====================================================

    def show_contacts(self):

        ContactWindow()

    # =====================================================

    def open_groups(self):

        GroupWindow()

    # =====================================================

    def open_profile(self):

        messagebox.showinfo(
            "Profile",
            f"Full Name: {self.current_user.full_name}\n"
            f"Email: {self.current_user.email}"
        )

    # =====================================================

    def logout(self):

        self.root.destroy()

        self.login_window.deiconify()