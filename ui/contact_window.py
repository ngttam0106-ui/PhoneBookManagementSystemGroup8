import tkinter as tk
from tkinter import ttk

from services.contact_service import ContactService


class ContactWindow:

    def __init__(self):
        self.service = ContactService()

        self.root = tk.Toplevel()
        self.root.title("Contact Management")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self.search_var = tk.StringVar()

        # Search
        tk.Label(self.root, text="Search:").pack(pady=5)

        tk.Entry(
            self.root,
            textvariable=self.search_var,
            width=40
        ).pack()

        tk.Button(
            self.root,
            text="Search",
            command=self.search_contact
        ).pack(pady=5)

        # Sort
        self.sort_box = ttk.Combobox(
            self.root,
            values=[
                "A-Z",
                "Latest",
                "Oldest"
            ],
            state="readonly"
        )

        self.sort_box.current(0)
        self.sort_box.pack(pady=5)

        tk.Button(
            self.root,
            text="Sort",
            command=self.sort_contact
        ).pack(pady=5)

        # Table
        self.table = ttk.Treeview(
            self.root,
            columns=(
                "ID",
                "Name",
                "Phone",
                "Email",
                "Address"
            ),
            show="headings"
        )

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "Address"
        )

        for col in columns:
            self.table.heading(col, text=col)

        self.table.column("ID", width=60, anchor="center")
        self.table.column("Name", width=180)
        self.table.column("Phone", width=120)
        self.table.column("Email", width=220)
        self.table.column("Address", width=250)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)

        # Load dữ liệu
        self.load_table(
            self.service.get_all_contacts()
        )

    def load_table(self, contacts):

        for item in self.table.get_children():
            self.table.delete(item)

        for contact in contacts:

            self.table.insert(
                "",
                tk.END,
                values=(
                    contact.contact_id,
                    contact.name,
                    contact.phone,
                    contact.email,
                    contact.address
                )
            )

    def search_contact(self):

        keyword = self.search_var.get().strip()

        if keyword == "":
            self.load_table(
                self.service.get_all_contacts()
            )
            return

        contacts = self.service.search_contact(keyword)

        self.load_table(contacts)

    def sort_contact(self):

        option = self.sort_box.get()

        if option == "A-Z":
            contacts = self.service.sort_az()

        elif option == "Latest":
            contacts = self.service.sort_latest()

        else:
            contacts = self.service.sort_oldest()

        self.load_table(contacts)

    def add_contact(self):
        pass

    def edit_contact(self):
        pass

    def delete_contact(self):
        pass

    def view_contact(self):
        pass