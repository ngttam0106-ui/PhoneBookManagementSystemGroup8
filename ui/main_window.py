import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from ui.contact_window import ContactWindow
from ui.group_window import GroupWindow


class MainWindow:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Phone Book Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        self.setup_ui()

    def setup_ui(self):

        # ================= Header =================
        header = tk.Frame(self.root, bg="#1E90FF", height=60)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="PHONE BOOK MANAGEMENT SYSTEM",
            bg="#1E90FF",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)

        # ================= Left Menu =================
        menu = tk.Frame(self.root, bg="#EEEEEE", width=220)
        menu.pack(side="left", fill="y")

        tk.Label(
            menu,
            text="Dashboard",
            bg="#EEEEEE",
            font=("Arial", 15, "bold")
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
            command=self.root.destroy
        ).pack(side="bottom", pady=30)

        # ================= Right Content =================
        content = tk.Frame(self.root, bg="white")
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Welcome",
            bg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Search
        search_frame = tk.Frame(content, bg="white")
        search_frame.pack()

        tk.Label(
            search_frame,
            text="Search:",
            bg="white"
        ).pack(side="left")

        self.search_entry = tk.Entry(search_frame, width=35)
        self.search_entry.pack(side="left", padx=10)

        tk.Button(
            search_frame,
            text="Search"
        ).pack(side="left")

        # Table
        columns = ("Name", "Phone", "Email")

        self.table = ttk.Treeview(
            content,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=180)

        self.table.pack(pady=20)

        # Demo Data
        self.table.insert("", "end", values=("Nguyen Van A", "0901234567", "a@gmail.com"))
        self.table.insert("", "end", values=("Tran Thi B", "0912345678", "b@gmail.com"))

        # Buttons
        button_frame = tk.Frame(content, bg="white")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="Add",
            width=10
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Edit",
            width=10
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=10
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            width=10
        ).grid(row=0, column=3, padx=5)

        # Status
        status = tk.Label(
            self.root,
            text="Ready...",
            anchor="w",
            bg="#DDDDDD"
        )
        status.pack(fill="x", side="bottom")

    def show_contacts(self):
        ContactWindow()

    def open_groups(self):
        GroupWindow()

    def open_profile(self):
        messagebox.showinfo(
            "Profile",
            "Open Profile Window"
        )
    def run(self):
        self.root.mainloop()