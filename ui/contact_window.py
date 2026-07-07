import tkinter as tk
from tkinter import messagebox

from services.contact_service import ContactService


class ContactWindow:

    def __init__(self, current_user=None, on_saved=None, contact=None):
        self.service = ContactService(current_user=current_user)
        self.on_saved = on_saved
        self.contact = contact

        self.root = tk.Toplevel()
        title = "Edit Contact" if contact is not None else "Add Contact"
        self.root.title(title)
        self.root.geometry("420x360")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

        self.fields = {}

        # Phone field only accepts digits while typing
        def validate_digit_only(new_value):
            if new_value == "":
                return True
            return new_value.isdigit()

        validate_command = self.root.register(validate_digit_only)

        labels = [
            ("Name", "name"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Address", "address"),
        ]

        for index, (text, key) in enumerate(labels):
            tk.Label(self.root, text=text).grid(row=index, column=0, sticky="w", padx=12, pady=8)
            if key == "phone":
                entry = tk.Entry(self.root, width=35, validate="key", validatecommand=(validate_command, "%P"))
            else:
                entry = tk.Entry(self.root, width=35)
            entry.grid(row=index, column=1, padx=12, pady=8)
            self.fields[key] = entry

        # If editing, pre-fill fields
        if self.contact is not None:
            try:
                self.fields["name"].insert(0, self.contact.name)
                self.fields["phone"].insert(0, self.contact.phone)
                self.fields["email"].insert(0, self.contact.email)
                self.fields["address"].insert(0, self.contact.address)
            except Exception:
                pass

        # Initialize checkbox variables from contact when editing so the tick state persists
        fav_init = self.contact.favorite if self.contact is not None else False
        emg_init = self.contact.emergency if self.contact is not None else False

        self.favorite_var = tk.BooleanVar(value=fav_init)
        self.emergency_var = tk.BooleanVar(value=emg_init)

        tk.Checkbutton(self.root, text="Favorite", variable=self.favorite_var).grid(
            row=4, column=0, padx=12, pady=8, sticky="w"
        )
        tk.Checkbutton(self.root, text="Emergency", variable=self.emergency_var).grid(
            row=4, column=1, padx=12, pady=8, sticky="w"
        )

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=5, column=0, columnspan=2, pady=14)

        tk.Button(button_frame, text="Save", width=14, command=self.save_contact).grid(row=0, column=0, padx=8)
        tk.Button(button_frame, text="Cancel", width=14, command=self.root.destroy).grid(row=0, column=1, padx=8)

    def save_contact(self):
        name = self.fields["name"].get().strip()
        phone = self.fields["phone"].get().strip()
        email = self.fields["email"].get().strip()
        address = self.fields["address"].get().strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and Phone are required.")
            return

        if not phone.isdigit():
            messagebox.showwarning("Warning", "Phone must contain only digits.")
            return

        if email and not email.lower().endswith("@gmail.com"):
            messagebox.showwarning("Warning", "Email must end with '@gmail.com'.")
            return

        if self.service.is_duplicate_contact(
            name=name,
            phone=phone,
            email=email,
            address=address,
            exclude_id=self.contact.contact_id if self.contact is not None else None,
        ):
            messagebox.showwarning(
                "Warning",
                "Duplicate contact detected. Name, phone, email, and address must be unique."
            )
            return

        # If editing an existing contact, call edit_contact; else add a new one
        if self.contact is not None:
            success = self.service.edit_contact(
                contact_id=self.contact.contact_id,
                name=name,
                phone=phone,
                email=email,
                address=address,
                favorite=self.favorite_var.get(),
                emergency=self.emergency_var.get(),
            )

            if not success:
                messagebox.showwarning(
                    "Warning",
                    "Duplicate contact detected. Name, phone, email, and address must be unique."
                )
                return

            # Close dialog then notify
            try:
                self.root.destroy()
            except Exception:
                pass

            if self.on_saved is not None:
                try:
                    self.on_saved(self.contact.contact_id)
                except Exception:
                    pass

            messagebox.showinfo("Success", "Contact has been updated.")
            return

        contact = self.service.add_contact(
            name=name,
            phone=phone,
            email=email,
            address=address,
            favorite=self.favorite_var.get(),
            emergency=self.emergency_var.get(),
        )

        if contact is None:
            messagebox.showwarning(
                "Warning",
                "Duplicate contact detected. Name, phone, email, and address must be unique."
            )
            return

        # Close the add dialog first so any subsequent windows/messages appear on top
        try:
            self.root.destroy()
        except Exception:
            pass

        if self.on_saved is not None:
            # Notify parent (MainWindow) to refresh and focus; pass new contact id
            try:
                self.on_saved(contact.contact_id)
            except Exception:
                pass

        else:
            # If no callback provided (e.g., opened from Login or standalone),
            # open the main window with a Guest user so the user can see the table immediately.
            try:
                from ui.main_window import MainWindow
                from model.user import User

                guest = User(0, "Guest", "guest@example.com", "", "", "")

                new_win = tk.Toplevel()
                main = MainWindow(new_win, guest, None)
                # Refresh and select the new contact
                try:
                    main.contact_added_handler()
                except Exception:
                    main.refresh_table()
            except Exception:
                pass

        messagebox.showinfo("Success", "Contact has been added.")

