import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

from services.group_service import GroupService
from services.contact_service import ContactService


class GroupWindow:

    def __init__(self):

        self.service = GroupService()
        self.contact_service = ContactService()

        self.root = tk.Toplevel()
        self.root.title("Group Management")
        self.root.geometry("850x550")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="GROUP MANAGEMENT",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ================= Group =================

        tk.Label(
            self.root,
            text="Group List",
            font=("Arial", 12, "bold")
        ).pack()

        self.group_table = ttk.Treeview(
            self.root,
            columns=("ID", "Group Name"),
            show="headings",
            height=8
        )

        self.group_table.heading("ID", text="ID")
        self.group_table.heading("Group Name", text="Group Name")

        self.group_table.column("ID", width=80, anchor="center")
        self.group_table.column("Group Name", width=250)

        self.group_table.pack(pady=5)

        self.group_table.bind(
            "<<TreeviewSelect>>",
            lambda event: self.show_contacts()
        )

        # ================= Buttons =================

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Create",
            width=12,
            command=self.create_group
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update",
            width=12,
            command=self.update_group
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=12,
            command=self.delete_group
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Add Contact",
            width=12,
            command=self.add_contact
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Remove Contact",
            width=15,
            command=self.remove_contact
        ).grid(row=0, column=4, padx=5)

        # ================= Contact =================

        tk.Label(
            self.root,
            text="Contacts In Group",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        self.contact_table = ttk.Treeview(
            self.root,
            columns=("ID", "Name", "Phone"),
            show="headings",
            height=10
        )

        self.contact_table.heading("ID", text="ID")
        self.contact_table.heading("Name", text="Name")
        self.contact_table.heading("Phone", text="Phone")

        self.contact_table.column("ID", width=70, anchor="center")
        self.contact_table.column("Name", width=250)
        self.contact_table.column("Phone", width=180)

        self.contact_table.pack(fill="x", padx=10)

        self.load_groups()

    # ===================================================

    def load_groups(self):

        for item in self.group_table.get_children():
            self.group_table.delete(item)

        groups = self.service.groups

        for group in groups:

            self.group_table.insert(
                "",
                tk.END,
                values=(
                    group.group_id,
                    group.group_name
                )
            )

    # ===================================================

    def create_group(self):

        group_name = simpledialog.askstring(
            "Create Group",
            "Enter group name:"
        )

        if not group_name:
            return

        self.service.create_group(
            user_id=1,
            group_name=group_name
        )

        self.load_groups()

    # ===================================================

    def update_group(self):

        selected = self.group_table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a group."
            )

            return

        group_id = self.group_table.item(
            selected[0]
        )["values"][0]

        new_name = simpledialog.askstring(
            "Rename Group",
            "Enter new group name:"
        )

        if not new_name:
            return

        self.service.update_group(
            group_id,
            new_name
        )

        self.load_groups()

    # ===================================================

    def delete_group(self):

        selected = self.group_table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a group."
            )

            return

        group_id = self.group_table.item(
            selected[0]
        )["values"][0]

        if not messagebox.askyesno(
            "Confirm",
            "Delete this group?"
        ):
            return

        self.service.delete_group(group_id)

        self.load_groups()

        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

    # ===================================================

    def add_contact(self):

        selected = self.group_table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a group."
            )

            return

        group_id = self.group_table.item(
            selected[0]
        )["values"][0]

        contacts = self.contact_service.get_all_contacts()

        if len(contacts) == 0:

            messagebox.showinfo(
                "Information",
                "No contacts available."
            )

            return

        text = ""

        for contact in contacts:

            text += f"{contact.contact_id} - {contact.name}\n"

        contact_id = simpledialog.askinteger(
            "Add Contact",
            f"Available Contacts:\n\n{text}\nEnter Contact ID:"
        )

        if contact_id is None:
            return

        self.service.add_contact_to_group(
            contact_id,
            group_id
        )

        self.show_contacts()

    # ===================================================

    def remove_contact(self):

        selected_group = self.group_table.selection()
        selected_contact = self.contact_table.selection()

        if not selected_group or not selected_contact:

            messagebox.showwarning(
                "Warning",
                "Please select a contact."
            )

            return

        group_id = self.group_table.item(
            selected_group[0]
        )["values"][0]

        contact_id = self.contact_table.item(
            selected_contact[0]
        )["values"][0]

        self.service.remove_contact_from_group(
            contact_id,
            group_id
        )

        self.show_contacts()

    # ===================================================

    def show_contacts(self):

        selected = self.group_table.selection()

        if not selected:
            return

        group_id = self.group_table.item(
            selected[0]
        )["values"][0]

        contacts = self.service.get_group_contacts(
            group_id
        )

        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

        for contact in contacts:

            self.contact_table.insert(
                "",
                tk.END,
                values=(
                    contact.contact_id,
                    contact.name,
                    contact.phone
                )
            )