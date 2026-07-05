import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from services.group_service import GroupService


class GroupWindow:

    def __init__(self):
        self.service = GroupService()

        self.root = tk.Toplevel()
        self.root.title("Group Management")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # ===== Danh sách nhóm =====
        tk.Label(
            self.root,
            text="Group List",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.group_table = ttk.Treeview(
            self.root,
            columns=("ID", "Group Name"),
            show="headings",
            height=8
        )

        self.group_table.heading("ID", text="ID")
        self.group_table.heading("Group Name", text="Group Name")

        self.group_table.column("ID", width=80, anchor="center")
        self.group_table.column("Group Name", width=300)

        self.group_table.pack()

        # ===== Button =====
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

        # ===== Contact trong nhóm =====
        tk.Label(
            self.root,
            text="Contacts in Group",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        self.contact_table = ttk.Treeview(
            self.root,
            columns=("Contact ID",),
            show="headings",
            height=8
        )

        self.contact_table.heading(
            "Contact ID",
            text="Contact ID"
        )

        self.contact_table.column(
            "Contact ID",
            width=200,
            anchor="center"
        )

        self.contact_table.pack(fill="x")

        self.group_table.bind(
            "<<TreeviewSelect>>",
            lambda event: self.show_contacts()
        )

        # Load dữ liệu
        self.load_groups()

    def load_groups(self):

        for item in self.group_table.get_children():
            self.group_table.delete(item)

        for group in self.service.groups:

            self.group_table.insert(
                "",
                tk.END,
                values=(
                    group.group_id,
                    group.group_name
                )
            )

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

    def update_group(self):

        selected = self.group_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a group."
            )
            return

        values = self.group_table.item(selected[0])["values"]

        group_id = values[0]

        new_name = simpledialog.askstring(
            "Rename Group",
            "New group name:"
        )

        if not new_name:
            return

        self.service.update_group(
            group_id,
            new_name
        )

        self.load_groups()

    def delete_group(self):

        selected = self.group_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a group."
            )
            return

        values = self.group_table.item(selected[0])["values"]

        group_id = values[0]

        self.service.delete_group(group_id)

        self.load_groups()

        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

    def show_contacts(self):

        selected = self.group_table.selection()

        if not selected:
            return

        values = self.group_table.item(selected[0])["values"]

        group_id = values[0]

        contact_ids = self.service.get_group_contacts(group_id)

        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

        for contact_id in contact_ids:

            self.contact_table.insert(
                "",
                tk.END,
                values=(contact_id,)
            )