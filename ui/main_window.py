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

        self.contact_service = ContactService(current_user=current_user)

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

        self.welcome_label = tk.Label(
            menu,
            text=f"Welcome\n{self.current_user.full_name}",
            bg="#EEEEEE",
            font=("Arial", 14, "bold")
        )

        self.welcome_label.pack(pady=20)

        # Contacts menu entry intentionally hidden/disabled per user request

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
            "Email",
            "Address",
            "Favorite",
            "Emergency"
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

            width = 220 if col in ["Name", "Phone", "Email", "Address"] else 120
            self.table.column(
                col,
                width=width
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
            command=self.edit_selected
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=10,
            command=self.delete_selected
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="View",
            width=10,
            command=self.view_selected
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            width=10,
            command=self.refresh_table
        ).grid(row=0, column=4, padx=5)

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
            # insert with iid set to contact_id so we can identify rows easily
            try:
                iid = str(contact.contact_id)
            except Exception:
                iid = None

            if iid:
                self.table.insert(
                    "",
                    tk.END,
                    iid=iid,
                    values=(
                        contact.name,
                        contact.phone,
                        contact.email,
                        contact.address,
                        "Yes" if contact.favorite else "No",
                        "Yes" if contact.emergency else "No"
                    )
                )
            else:
                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        contact.name,
                        contact.phone,
                        contact.email,
                        contact.address,
                        "Yes" if contact.favorite else "No",
                        "Yes" if contact.emergency else "No"
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

        # Reload contacts from storage in case other services modified them
        try:
            self.contact_service.contacts = self.contact_service.file_manager.load_contacts()
        except Exception:
            # fallback: recreate service
            try:
                self.contact_service = ContactService(current_user=self.current_user)
            except Exception:
                pass

        self.load_table(
            self.contact_service.get_all_contacts()
        )

    def view_all_contacts(self):
        self.load_table(self.contact_service.get_all_contacts())

    def view_favorite_contacts(self):
        self.load_table(self.contact_service.get_favorite_contacts())

    def view_emergency_contacts(self):
        self.load_table(self.contact_service.get_emergency_contacts())

    # =====================================================

    def contact_added_handler(self, contact_id=None):
        """Called after a contact is added/updated: refresh table, lift window and select the contact.

        If `contact_id` is None, the last row will be selected.
        """

        self.refresh_table()

        try:
            self.root.deiconify()
            self.root.lift()
            # briefly make topmost so it appears above other windows
            try:
                self.root.attributes('-topmost', True)
                self.root.after(100, lambda: self.root.attributes('-topmost', False))
            except Exception:
                pass
            self.root.focus_force()
        except Exception:
            pass

        children = self.table.get_children()
        if not children:
            return

        if contact_id is None:
            last = children[-1]
            try:
                self.table.selection_set(last)
                self.table.see(last)
            except Exception:
                pass
            return

        iid = str(contact_id)
        if iid in children:
            try:
                self.table.selection_set(iid)
                self.table.see(iid)
            except Exception:
                pass

    # =====================================================

    def delete_selected(self):
        """Delete the currently selected contact from storage and refresh table."""

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return

        # iid was set to contact_id when loading
        iid = selected[0]

        # confirm
        if not messagebox.askyesno("Confirm", "Delete selected contact?"):
            return

        try:
            contact_id = int(iid)
        except Exception:
            # fallback: try to match by values
            vals = self.table.item(iid)['values']
            contact_id = None
            for contact in self.contact_service.get_all_contacts():
                if (contact.name, contact.phone, contact.email) == (vals[0], vals[1], vals[2]):
                    contact_id = contact.contact_id
                    break

        if contact_id is None:
            messagebox.showerror("Error", "Could not determine selected contact ID.")
            return

        deleted = self.contact_service.delete_contact(contact_id)

        if deleted:
            messagebox.showinfo("Deleted", "Contact deleted.")
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Failed to delete contact.")

    # =====================================================

    def edit_selected(self):
        """Open the selected contact in the ContactWindow for editing."""

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit.")
            return

        iid = selected[0]

        try:
            contact_id = int(iid)
        except Exception:
            vals = self.table.item(iid)['values']
            contact_id = None
            for contact in self.contact_service.get_all_contacts():
                if (contact.name, contact.phone, contact.email) == (vals[0], vals[1], vals[2]):
                    contact_id = contact.contact_id
                    break

        if contact_id is None:
            messagebox.showerror("Error", "Could not determine selected contact ID for editing.")
            return

        contact = self.contact_service.get_contact(contact_id)

        if contact is None:
            messagebox.showerror("Error", "Selected contact not found.")
            return

        # Open edit dialog and pass callback to refresh and select this contact
        ContactWindow(
            current_user=self.current_user,
            on_saved=self.contact_added_handler,
            contact=contact
        )

    # =====================================================

    def view_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to view.")
            return

        iid = selected[0]
        try:
            contact_id = int(iid)
        except Exception:
            vals = self.table.item(iid)['values']
            contact_id = None
            for contact in self.contact_service.get_all_contacts():
                if (contact.name, contact.phone, contact.email) == (vals[0], vals[1], vals[2]):
                    contact_id = contact.contact_id
                    break

        if contact_id is None:
            messagebox.showerror("Error", "Could not determine selected contact ID for viewing.")
            return

        contact = self.contact_service.get_contact(contact_id)
        if contact is None:
            messagebox.showerror("Error", "Selected contact not found.")
            return

        messagebox.showinfo(
            "Contact Details",
            f"Name: {contact.name}\n"
            f"Phone: {contact.phone}\n"
            f"Email: {contact.email}\n"
            f"Address: {contact.address}\n"
            f"Favorite: {'Yes' if contact.favorite else 'No'}\n"
            f"Emergency: {'Yes' if contact.emergency else 'No'}"
        )

    # =====================================================

    def show_contacts(self):

        ContactWindow(
            current_user=self.current_user,
            on_saved=self.contact_added_handler
        )

    # =====================================================

    def open_groups(self):

        GroupWindow()

    # =====================================================

    def open_profile(self):
        from ui.profile_window import ProfileWindow
        profile_root = tk.Toplevel(self.root)

        ProfileWindow(
            profile_root,
            self.current_user
        )

        profile_root.grab_set()

        self.root.wait_window(profile_root)

        self.refresh_user_info()

    # =====================================================

    def refresh_user_info(self):

        self.welcome_label.config(
            text=f"Welcome\n{self.current_user.full_name}"
        )

    # =====================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:

            self.root.destroy()

            self.login_window.deiconify()