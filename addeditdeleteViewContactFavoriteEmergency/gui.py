# -*- coding: utf-8 -*-
"""
gui.py
------
Tang giao dien (View layer), xay dung bang Tkinter/ttk. Cai dat CHINH XAC
5 man hinh mo ta trong Muc VII bao cao, thuoc pham vi phu trach:

    VII.10 Add contact Screen          -> AddContactWindow   (UC6)
    VII.11 Contact list screen         -> PhoneBookApp        (ho tro UC10)
    VII.12 View screen                 -> ViewContactWindow   (UC10, UC12)
    VII.13 Edit contact screen         -> EditContactWindow   (UC11)
    VII.14 Delete contact screen       -> ConfirmDialog       (UC13)

CAP NHAT THEO MOCKUP THUC TE (anh Khang gui):
- Danh sach lien he: bam vao MOT DONG se MO RONG ngay tai cho, hien 3 nut
  "View | Edit | Delete" gan lien duoi dong do (giong dong "Nguyen Van B"
  trong anh mau "5. Contact List Screen"). Chi 1 dong duoc mo rong tai 1
  thoi diem. -> lop ContactRow.
- Nut tron "+" noi o goc duoi phai danh sach: bam vao hien popup 2 dong
  "Create New Group" / "Add Contact" (giong anh mau "Create new group and
  add contact interface"). "Add Contact" chay chuc nang that (UC6);
  "Create New Group" CHI la giao dien cho dung mockup - khong noi logic
  that vi Contact Group Management (FR-4) la phan cua thanh vien khac
  trong nhom. -> lop FabMenu.

GHI CHU PHAM VI (khong doi so voi truoc):
- Chuc nang Browse/Search/Sort DAY DU (UC7, UC8, UC9 - FR-3) la phan viec
  cua thanh vien khac; o day chi co 1 o tim kiem don gian de de demo/su dung.
- Man hinh View KHONG con 3 nut Message/Call/Video nua (da bo theo yeu cau -
  vi khong co FR nao yeu cau goi dien/nhan tin that nen bo luon cho gon,
  thay vi de lai dang placeholder).
- Favorite/Emergency van duoc bat/tat CHINH tai man hinh View Contact Detail
  (dung UC12: "On the contact detail screen, the user selects..."), vi
  mockup danh sach chi ve San View/Edit/Delete cho dong mo rong.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from contact_manager import ContactManager
from avatar_utils import make_avatar_image, make_fab_icon

# ----------------------------------------------------------------------
# Bang mau & font dung chung toan bo giao dien
# ----------------------------------------------------------------------
FONT_FAMILY = "Segoe UI"

COLOR_BG = "#F3F5FA"
COLOR_SURFACE = "#FFFFFF"
COLOR_INFO_CARD = "#F7F8FC"
COLOR_PRIMARY = "#3057D5"
COLOR_PRIMARY_DARK = "#28469E"
COLOR_DANGER = "#E0483E"
COLOR_DANGER_DARK = "#B93A31"
COLOR_TEXT = "#1F2430"
COLOR_TEXT_MUTED = "#6B7280"
COLOR_BORDER = "#E3E6EE"
COLOR_FAVORITE = "#E08E00"
COLOR_EMERGENCY = "#E0483E"
COLOR_FAVORITE_BG = "#FFF6E5"
COLOR_EMERGENCY_BG = "#FDECEC"


def configure_styles(root: tk.Tk) -> None:
    """Cau hinh toan bo ttk.Style dung chung cho ca ung dung."""
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".", font=(FONT_FAMILY, 10), background=COLOR_BG)
    style.configure("App.TFrame", background=COLOR_BG)
    style.configure("Surface.TFrame", background=COLOR_SURFACE)
    style.configure("InfoCard.TFrame", background=COLOR_INFO_CARD)

    style.configure("PageTitle.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 20, "bold"))
    style.configure("DialogTitle.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 16, "bold"))
    style.configure("ContactName.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 15, "bold"))
    style.configure("Eyebrow.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_MUTED,
                    font=(FONT_FAMILY, 9, "bold"))
    style.configure("FieldLabel.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 10, "bold"))
    style.configure("Body.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 10))
    style.configure("Hint.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_MUTED,
                    font=(FONT_FAMILY, 9))
    style.configure("Error.TLabel", background=COLOR_SURFACE, foreground=COLOR_DANGER_DARK,
                    font=(FONT_FAMILY, 9, "bold"))
    style.configure("InfoLabel.TLabel", background=COLOR_INFO_CARD, foreground=COLOR_TEXT_MUTED,
                    font=(FONT_FAMILY, 10))
    style.configure("InfoValue.TLabel", background=COLOR_INFO_CARD, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 10, "bold"))
    style.configure("EmptyState.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_MUTED,
                    font=(FONT_FAMILY, 11), anchor="center")

    style.configure("TEntry", fieldbackground=COLOR_SURFACE, foreground=COLOR_TEXT,
                    bordercolor=COLOR_BORDER, lightcolor=COLOR_BORDER, darkcolor=COLOR_BORDER,
                    padding=6)

    style.configure("Primary.TButton", background=COLOR_PRIMARY, foreground="white",
                    font=(FONT_FAMILY, 10, "bold"), padding=(14, 8), borderwidth=0)
    style.map("Primary.TButton", background=[("active", COLOR_PRIMARY_DARK)])

    style.configure("Secondary.TButton", background="#EEF1F8", foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 10), padding=(14, 8), borderwidth=0)
    style.map("Secondary.TButton",
              background=[("active", "#DDE3F2"), ("disabled", "#F2F3F7")],
              foreground=[("disabled", COLOR_TEXT_MUTED)])

    style.configure("Danger.TButton", background=COLOR_DANGER, foreground="white",
                    font=(FONT_FAMILY, 10, "bold"), padding=(14, 8), borderwidth=0)
    style.map("Danger.TButton",
              background=[("active", COLOR_DANGER_DARK), ("disabled", "#F1B9B5")])

    style.configure("Ghost.TButton", background=COLOR_SURFACE, foreground=COLOR_PRIMARY,
                    font=(FONT_FAMILY, 9), padding=(10, 6), borderwidth=1, relief="solid")
    style.map("Ghost.TButton", background=[("active", "#EEF1F8")])

    style.configure("ToggleActiveFavorite.TButton", background=COLOR_FAVORITE, foreground="white",
                    font=(FONT_FAMILY, 10, "bold"), padding=(14, 8), borderwidth=0)
    style.configure("ToggleActiveEmergency.TButton", background=COLOR_EMERGENCY, foreground="white",
                    font=(FONT_FAMILY, 10, "bold"), padding=(14, 8), borderwidth=0)

    # Nut cho 3-segment "View | Edit | Delete" trong dong lien he mo rong
    style.configure("Segment.TButton", background=COLOR_SURFACE, foreground=COLOR_TEXT,
                    font=(FONT_FAMILY, 9, "bold"), padding=(8, 10), borderwidth=0, relief="flat")
    style.map("Segment.TButton", background=[("active", "#EEF1F8")])
    style.configure("SegmentDanger.TButton", background=COLOR_SURFACE, foreground=COLOR_DANGER_DARK,
                    font=(FONT_FAMILY, 9, "bold"), padding=(8, 10), borderwidth=0, relief="flat")
    style.map("SegmentDanger.TButton", background=[("active", COLOR_EMERGENCY_BG)])


def center_window(win: tk.Toplevel, parent) -> None:
    """Dinh vi cua so con o giua man hinh (hoac giua cua so cha), giu nguyen
    kich thuoc da tu dong tinh theo noi dung ben trong."""
    win.update_idletasks()
    width, height = win.winfo_width(), win.winfo_height()
    if parent is not None:
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        x, y = px + (pw - width) // 2, py + (ph - height) // 2
    else:
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        x, y = (sw - width) // 2, (sh - height) // 2
    win.geometry(f"+{max(x, 0)}+{max(y, 0)}")


# ----------------------------------------------------------------------
# Form dung chung cho Add Contact & Edit Contact (4 truong: Name, Phone,
# Email, Address - dung Section VII.10 / VII.13)
# ----------------------------------------------------------------------
def make_contact_vars(values: dict | None = None) -> dict:
    values = values or {}
    return {
        "name": tk.StringVar(value=values.get("name", "")),
        "phone": tk.StringVar(value=values.get("phone", "")),
        "email": tk.StringVar(value=values.get("email", "")),
        "address": tk.StringVar(value=values.get("address", "")),
    }


def pack_form_rows(parent: tk.Widget, field_vars: dict) -> ttk.Entry:
    """Ve 4 dong Label + Entry (Name*, Phone Number*, Email, Address).
    Tra ve entry dau tien (Name) de goi focus_set() ben ngoai."""
    labels = [
        ("Name *", "name"), ("Phone Number *", "phone"),
        ("Email", "email"), ("Address", "address"),
    ]
    first_entry = None
    for label_text, key in labels:
        row = ttk.Frame(parent, style="Surface.TFrame")
        row.pack(fill="x", pady=(0, 12))
        ttk.Label(row, text=label_text, style="FieldLabel.TLabel").pack(anchor="w")
        entry = ttk.Entry(row, textvariable=field_vars[key], font=(FONT_FAMILY, 11))
        entry.pack(fill="x", ipady=5)
        if first_entry is None:
            first_entry = entry
    return first_entry


class AvatarPicker(ttk.Frame):
    """Widget xem truoc + chon anh dai dien, dung chung cho Add & Edit.
    Preview cap nhat SONG SONG khi nguoi dung go ten (neu chua chon anh)."""

    def __init__(self, parent, name_var: tk.StringVar, initial_avatar_path: str = "",
                 button_text: str = "Add a Photo"):
        super().__init__(parent, style="Surface.TFrame")
        self.name_var = name_var
        self.avatar_path = initial_avatar_path
        self._photo_ref = None

        self.preview_label = tk.Label(self, bd=0, background=COLOR_SURFACE)
        self.preview_label.pack(pady=(0, 8))

        ttk.Button(self, text=button_text, style="Ghost.TButton",
                   command=self._choose_photo).pack()

        self._trace_id = name_var.trace_add("write", lambda *_: self._refresh_preview())
        self._refresh_preview()

    def _choose_photo(self):
        path = filedialog.askopenfilename(
            title="Select a photo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")],
        )
        if path:
            self.avatar_path = path
            self._refresh_preview()

    def _refresh_preview(self):
        self._photo_ref = make_avatar_image(self.name_var.get(), self.avatar_path, size=88)
        self.preview_label.configure(image=self._photo_ref)


class ConfirmDialog(tk.Toplevel):
    """Hop thoai xac nhan dung chung (UC13 - <<include>> Confirm Delete,
    va tuong tu cho cac thao tac nguy hiem khac - Muc VII.14)."""

    def __init__(self, parent, title: str, message: str,
                 confirm_text: str = "Delete", danger: bool = True, on_confirm=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=COLOR_SURFACE)
        self.resizable(False, False)
        self.transient(parent)
        self._on_confirm = on_confirm
        self.result = False

        container = ttk.Frame(self, padding=24, style="Surface.TFrame")
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=title, style="DialogTitle.TLabel").pack(anchor="w", pady=(0, 12))
        ttk.Label(container, text=message, style="Body.TLabel",
                  wraplength=320, justify="left").pack(anchor="w", pady=(0, 24))

        btn_row = ttk.Frame(container, style="Surface.TFrame")
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text="Cancel", style="Secondary.TButton",
                   command=self._cancel).pack(side="right", padx=(8, 0))
        ttk.Button(btn_row, text=confirm_text,
                   style="Danger.TButton" if danger else "Primary.TButton",
                   command=self._confirm).pack(side="right")

        center_window(self, parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _confirm(self):
        self.result = True
        self.destroy()
        if self._on_confirm:
            self._on_confirm()

    def _cancel(self):
        self.result = False
        self.destroy()


class AddContactWindow(tk.Toplevel):
    """UC6 - Add Contact (Muc VII.10)."""

    def __init__(self, parent, manager: ContactManager, on_saved):
        super().__init__(parent)
        self.manager = manager
        self.on_saved = on_saved
        self.title("Add Contact")
        self.configure(bg=COLOR_SURFACE)
        self.resizable(False, False)
        self.transient(parent)

        container = ttk.Frame(self, padding=24, style="Surface.TFrame")
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Add Contact", style="DialogTitle.TLabel").pack(anchor="w", pady=(0, 16))

        self.form_vars = make_contact_vars()
        self.avatar_picker = AvatarPicker(container, name_var=self.form_vars["name"],
                                          button_text="Add a Photo")
        self.avatar_picker.pack(pady=(0, 16))

        first_entry = pack_form_rows(container, self.form_vars)

        self.error_label = ttk.Label(container, text="", style="Error.TLabel",
                                      wraplength=360, justify="left")
        self.error_label.pack(anchor="w", fill="x", pady=(0, 4))

        ttk.Label(container, text="* Required fields", style="Hint.TLabel").pack(anchor="w")

        btn_row = ttk.Frame(container, style="Surface.TFrame")
        btn_row.pack(fill="x", pady=(20, 0))
        ttk.Button(btn_row, text="Cancel", style="Secondary.TButton",
                   command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(btn_row, text="Add", style="Primary.TButton",
                   command=self._on_add).pack(side="right")

        center_window(self, parent)
        self.grab_set()
        first_entry.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_add(self):
        v = self.form_vars
        success, message, _contact = self.manager.add_contact(
            name=v["name"].get(), phone_number=v["phone"].get(),
            email=v["email"].get(), address=v["address"].get(),
            avatar_path=self.avatar_picker.avatar_path,
        )
        if not success:
            self.error_label.configure(text=message)
            return
        messagebox.showinfo("Success", message, parent=self)
        self.destroy()
        self.on_saved()


class EditContactWindow(tk.Toplevel):
    """UC11 - Edit Contact (Muc VII.13)."""

    def __init__(self, parent, manager: ContactManager, contact, on_saved):
        super().__init__(parent)
        self.manager = manager
        self.contact = contact
        self.on_saved = on_saved
        self.title("Edit Contact")
        self.configure(bg=COLOR_SURFACE)
        self.resizable(False, False)
        self.transient(parent)

        container = ttk.Frame(self, padding=24, style="Surface.TFrame")
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Edit Contact", style="DialogTitle.TLabel").pack(anchor="w", pady=(0, 16))

        self.form_vars = make_contact_vars({
            "name": contact.name, "phone": contact.phone_number,
            "email": contact.email, "address": contact.address,
        })
        self.avatar_picker = AvatarPicker(container, name_var=self.form_vars["name"],
                                          initial_avatar_path=contact.avatar_path,
                                          button_text="Change Photo")
        self.avatar_picker.pack(pady=(0, 16))

        first_entry = pack_form_rows(container, self.form_vars)

        self.error_label = ttk.Label(container, text="", style="Error.TLabel",
                                      wraplength=360, justify="left")
        self.error_label.pack(anchor="w", fill="x", pady=(0, 4))

        ttk.Label(container, text="* Required fields", style="Hint.TLabel").pack(anchor="w")

        btn_row = ttk.Frame(container, style="Surface.TFrame")
        btn_row.pack(fill="x", pady=(20, 0))
        ttk.Button(btn_row, text="Cancel", style="Secondary.TButton",
                   command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(btn_row, text="Save Changes", style="Primary.TButton",
                   command=self._on_save).pack(side="right")

        center_window(self, parent)
        self.grab_set()
        first_entry.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_save(self):
        v = self.form_vars
        success, message = self.manager.edit_contact(
            contact_id=self.contact.contact_id,
            name=v["name"].get(), phone_number=v["phone"].get(),
            email=v["email"].get(), address=v["address"].get(),
            avatar_path=self.avatar_picker.avatar_path,
        )
        if not success:
            self.error_label.configure(text=message)
            return
        messagebox.showinfo("Success", message, parent=self)
        self.destroy()
        self.on_saved()


class ViewContactWindow(tk.Toplevel):
    """UC10 - View Contact Detail (Muc VII.12).
    La diem noi <<extend>> den UC11 (Edit), UC12 (Mark Special Contact),
    UC13 (Delete) - dung nhu mo ta trong Muc 10.6 Extension point."""

    def __init__(self, parent, manager: ContactManager, contact_id: int, on_change):
        super().__init__(parent)
        self.manager = manager
        self.contact_id = contact_id
        self.on_change = on_change
        self.configure(bg=COLOR_SURFACE)
        self.resizable(False, False)
        self.transient(parent)
        self._photo_ref = None

        self.container = ttk.Frame(self, padding=24, style="Surface.TFrame")
        self.container.pack(fill="both", expand=True)

        self._build()
        center_window(self, parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        contact = self.manager.get_contact_by_id(self.contact_id)
        if contact is None:
            ttk.Label(self.container, text="This contact no longer exists.",
                      style="Body.TLabel").pack(pady=20)
            ttk.Button(self.container, text="Close", style="Secondary.TButton",
                       command=self.destroy).pack()
            return

        self.title(contact.name)

        header = ttk.Frame(self.container, style="Surface.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="VIEW", style="Eyebrow.TLabel").pack(side="left")
        ttk.Button(header, text="Edit", style="Secondary.TButton",
                   command=self._open_edit).pack(side="right")

        self._photo_ref = make_avatar_image(contact.name, contact.avatar_path, size=96)
        tk.Label(self.container, image=self._photo_ref, bg=COLOR_SURFACE).pack(pady=(12, 4))
        ttk.Label(self.container, text=contact.name, style="ContactName.TLabel").pack(pady=(0, 16))

        info_frame = ttk.Frame(self.container, style="InfoCard.TFrame", padding=16)
        info_frame.pack(fill="x", pady=(0, 16))
        self._info_row(info_frame, "Phone Number", contact.phone_number)
        self._info_row(info_frame, "Email", contact.email or "-")
        self._info_row(info_frame, "Address", contact.address or "-")

        badge_row = ttk.Frame(self.container, style="Surface.TFrame")
        badge_row.pack(fill="x", pady=(0, 16))

        fav_text = "\u2605 Favorited" if contact.is_favorite else "+ Add to Favorites"
        fav_style = "ToggleActiveFavorite.TButton" if contact.is_favorite else "Secondary.TButton"
        ttk.Button(badge_row, text=fav_text, style=fav_style,
                   command=self._toggle_favorite).pack(side="left", fill="x", expand=True, padx=(0, 6))

        em_text = "Emergency Contact" if contact.is_emergency else "+ Add emergency contacts"
        em_style = "ToggleActiveEmergency.TButton" if contact.is_emergency else "Secondary.TButton"
        ttk.Button(badge_row, text=em_text, style=em_style,
                   command=self._toggle_emergency).pack(side="left", fill="x", expand=True, padx=(6, 0))

        ttk.Button(self.container, text="Delete Contact", style="Danger.TButton",
                   command=self._delete).pack(fill="x")

    @staticmethod
    def _info_row(parent, label, value):
        row = ttk.Frame(parent, style="InfoCard.TFrame")
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label, style="InfoLabel.TLabel").pack(side="left")
        ttk.Label(row, text=value, style="InfoValue.TLabel").pack(side="right")

    def _open_edit(self):
        contact = self.manager.get_contact_by_id(self.contact_id)
        if contact is not None:
            EditContactWindow(self, self.manager, contact, on_saved=self._after_change)

    def _toggle_favorite(self):
        success, _message, _state = self.manager.toggle_favorite(self.contact_id)
        if success:
            self._after_change()

    def _toggle_emergency(self):
        success, _message, _state = self.manager.toggle_emergency(self.contact_id)
        if success:
            self._after_change()

    def _delete(self):
        contact = self.manager.get_contact_by_id(self.contact_id)
        if contact is None:
            return

        def do_delete():
            success, message = self.manager.delete_contact(self.contact_id)
            self.destroy()
            self.on_change()
            if success:
                messagebox.showinfo("Success", message)

        ConfirmDialog(
            self, title="Delete Contact",
            message=f"Are you sure you want to delete '{contact.name}' from "
                    f"your phonebook? This action cannot be undone.",
            confirm_text="Delete", danger=True, on_confirm=do_delete,
        )

    def _after_change(self):
        self._build()
        center_window(self, self.master)
        self.on_change()


class ContactRow(tk.Frame):
    """
    Mot dong lien he trong danh sach (Muc VII.11). Bam vao BAT KY DAU tren
    dong (avatar, ten, sdt...) se MO RONG / THU GON ngay tai cho, hien 3 nut
    "View | Edit | Delete" gan lien phia duoi - giong hanh vi cua dong
    "Nguyen Van B" trong anh mockup "5. Contact List Screen".
    """

    def __init__(self, parent, contact, on_toggle, on_view, on_edit, on_delete):
        row_bg = (
            COLOR_EMERGENCY_BG if contact.is_emergency
            else COLOR_FAVORITE_BG if contact.is_favorite
            else COLOR_SURFACE
        )
        super().__init__(parent, bg=row_bg)
        self.contact = contact
        self.on_toggle = on_toggle
        self.expanded = False

        # ---- dong thong tin chinh (avatar + ten + sdt + nhan) ----
        self.main_line = tk.Frame(self, bg=row_bg, cursor="hand2")

        self._avatar_img = make_avatar_image(contact.name, contact.avatar_path, size=36)
        avatar_lbl = tk.Label(self.main_line, image=self._avatar_img, bg=row_bg)
        avatar_lbl.pack(side="left", padx=(16, 12), pady=12)

        text_col = tk.Frame(self.main_line, bg=row_bg, cursor="hand2")
        text_col.pack(side="left", fill="x", expand=True, pady=12)

        name_lbl = tk.Label(text_col, text=contact.name, bg=row_bg, fg=COLOR_TEXT,
                             font=(FONT_FAMILY, 11, "bold"), anchor="w", cursor="hand2")
        name_lbl.pack(anchor="w", fill="x")

        badges = []
        if contact.is_emergency:
            badges.append("Emergency")
        if contact.is_favorite:
            badges.append("Favorite")
        sub_text = contact.phone_number + ("   \u2022   " + "  ".join(badges) if badges else "")
        sub_lbl = tk.Label(text_col, text=sub_text, bg=row_bg, fg=COLOR_TEXT_MUTED,
                            font=(FONT_FAMILY, 9), anchor="w", cursor="hand2")
        sub_lbl.pack(anchor="w", fill="x")

        for widget in (self, self.main_line, avatar_lbl, text_col, name_lbl, sub_lbl):
            widget.bind("<Button-1>", self._handle_click)

        # ---- dong 3 nut View | Edit | Delete (an/hien theo expanded) ----
        self.actions_frame = tk.Frame(self, bg=row_bg)
        border_box = tk.Frame(self.actions_frame, bg=COLOR_BORDER)
        border_box.pack(fill="x", padx=16, pady=(0, 14))
        inner = tk.Frame(border_box, bg=row_bg)
        inner.pack(fill="x", padx=1, pady=1)

        ttk.Button(inner, text="View", style="Segment.TButton",
                   command=lambda: on_view(contact.contact_id)).pack(side="left", fill="both", expand=True)
        tk.Frame(inner, bg=COLOR_BORDER, width=1).pack(side="left", fill="y")
        ttk.Button(inner, text="Edit", style="Segment.TButton",
                   command=lambda: on_edit(contact.contact_id)).pack(side="left", fill="both", expand=True)
        tk.Frame(inner, bg=COLOR_BORDER, width=1).pack(side="left", fill="y")
        ttk.Button(inner, text="Delete", style="SegmentDanger.TButton",
                   command=lambda: on_delete(contact.contact_id)).pack(side="left", fill="both", expand=True)

        self.separator = ttk.Separator(self, orient="horizontal")

        self._relayout()

    def _handle_click(self, _event=None):
        self.on_toggle(self.contact.contact_id)

    def _relayout(self):
        self.main_line.pack_forget()
        self.actions_frame.pack_forget()
        self.separator.pack_forget()
        self.main_line.pack(fill="x")
        if self.expanded:
            self.actions_frame.pack(fill="x")
        self.separator.pack(fill="x")

    def set_expanded(self, expanded: bool):
        self.expanded = expanded
        self._relayout()


class FabMenu(tk.Toplevel):
    """
    Popup nho hien ra ngay tren nut '+' noi, giong anh mockup "Create new
    group and add contact interface": 2 dong "Create New Group" / "Add
    Contact". Tu dong dong lai khi mat focus (bam ra ngoai) hoac nhan Esc.
    """

    def __init__(self, parent, anchor_widget: tk.Widget, on_add_contact, on_create_group):
        super().__init__(parent)
        self.overrideredirect(True)
        try:
            self.attributes("-topmost", True)
        except tk.TclError:
            pass
        self.configure(bg=COLOR_BORDER)

        card = tk.Frame(self, bg=COLOR_SURFACE)
        card.pack(padx=1, pady=1)

        self._make_item(card, "\U0001F465", "Create New Group", on_create_group)
        tk.Frame(card, bg=COLOR_BORDER, height=1).pack(fill="x")
        self._make_item(card, "\U0001F464", "Add Contact", on_add_contact)

        self.update_idletasks()
        ax = anchor_widget.winfo_rootx()
        ay = anchor_widget.winfo_rooty()
        aw = anchor_widget.winfo_width()
        pw = self.winfo_width()
        ph = self.winfo_height()
        x = ax + aw - pw
        y = ay - ph - 10
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<FocusOut>", lambda e: self.after(1, self._maybe_close))
        self.focus_force()

    def _maybe_close(self):
        try:
            if self.focus_displayof() is None:
                self.destroy()
        except tk.TclError:
            pass

    def _make_item(self, parent, icon, text, command):
        row = tk.Frame(parent, bg=COLOR_SURFACE, cursor="hand2")
        row.pack(fill="x")
        lbl = tk.Label(row, text=f"{icon}   {text}", bg=COLOR_SURFACE, fg=COLOR_TEXT,
                        font=(FONT_FAMILY, 10), anchor="w", padx=18, pady=12, cursor="hand2")
        lbl.pack(fill="x")

        def handler(_event=None):
            self.destroy()
            command()

        def on_enter(_e=None):
            row.configure(bg="#EEF1F8")
            lbl.configure(bg="#EEF1F8")

        def on_leave(_e=None):
            row.configure(bg=COLOR_SURFACE)
            lbl.configure(bg=COLOR_SURFACE)

        for widget in (row, lbl):
            widget.bind("<Button-1>", handler)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)


class PhoneBookApp(tk.Tk):
    """Cua so chinh: danh sach lien he (dong mo rong) + nut '+' noi de
    Add Contact - diem khoi dau cho View/Edit/Delete/Mark Special Contact
    (Muc VII.11 Contact list screen)."""

    def __init__(self, manager: ContactManager):
        super().__init__()
        self.manager = manager
        self.title("Phone Book Management System - Contact Module")
        self.geometry("640x720")
        self.minsize(420, 480)
        self.configure(bg=COLOR_BG)
        configure_styles(self)

        self.rows: dict[int, ContactRow] = {}
        self._expanded_contact_id = None

        self._build_layout()
        self.refresh_list()

    # ------------------------------------------------------------------
    def _build_layout(self):
        top_bar = ttk.Frame(self, style="Surface.TFrame", padding=(24, 20))
        top_bar.pack(fill="x")
        ttk.Label(top_bar, text="My Contacts", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(top_bar, text=f"Logged in as: User #{self.manager.user_id} (demo session)",
                  style="Hint.TLabel").pack(anchor="w")
        self.stats_label = ttk.Label(top_bar, style="Hint.TLabel")
        self.stats_label.pack(anchor="w")

        search_bar = ttk.Frame(self, style="Surface.TFrame", padding=(24, 0, 24, 16))
        search_bar.pack(fill="x")
        ttk.Label(search_bar, text="Search by name or phone number",
                  style="FieldLabel.TLabel").pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_list())
        ttk.Entry(search_bar, textvariable=self.search_var,
                  font=(FONT_FAMILY, 11)).pack(fill="x", ipady=5)

        body = ttk.Frame(self, style="App.TFrame", padding=(24, 0, 24, 24))
        body.pack(fill="both", expand=True)

        self.list_card = tk.Frame(body, bg=COLOR_SURFACE, highlightbackground=COLOR_BORDER,
                                   highlightthickness=1)
        self.list_card.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.list_card, bg=COLOR_SURFACE, highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self.list_card, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)

        self.rows_frame = tk.Frame(self.canvas, bg=COLOR_SURFACE)
        self._canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        self.rows_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.itemconfig(self._canvas_window, width=e.width)
        )
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        self.empty_state = ttk.Label(
            self.list_card, text="No contacts yet.\nTap the + button to get started.",
            style="EmptyState.TLabel", justify="center",
        )

        # ---- nut tron '+' noi o goc duoi phai (Muc VII.11 / VII.16) ----
        self._fab_icon = make_fab_icon(size=56, bg_color=COLOR_PRIMARY)
        self.fab_button = tk.Button(
            self, image=self._fab_icon, bd=0, highlightthickness=0,
            bg=COLOR_BG, activebackground=COLOR_BG, cursor="hand2",
            command=self._open_fab_menu,
        )
        self.fab_button.place(in_=self.list_card, relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

    # ------------------------------------------------------------------
    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if getattr(event, "num", None) == 4:
            self.canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ------------------------------------------------------------------
    def refresh_list(self):
        """Ve lai danh sach (loc theo o tim kiem neu co nhap), giu nguyen
        dong dang mo rong neu contact do van con trong ket qua loc."""
        keyword = self.search_var.get().strip().lower()
        contacts = self.manager.get_all_contacts()
        filtered = [
            c for c in contacts
            if not keyword or keyword in c.name.lower() or keyword in c.phone_number.lower()
        ]

        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        self.rows.clear()

        if self._expanded_contact_id is not None and not any(
            c.contact_id == self._expanded_contact_id for c in filtered
        ):
            self._expanded_contact_id = None

        if not filtered:
            self.canvas.pack_forget()
            self.vscroll.pack_forget()
            self.empty_state.pack(fill="both", expand=True, pady=60)
        else:
            self.empty_state.pack_forget()
            if not self.canvas.winfo_ismapped():
                self.canvas.pack(side="left", fill="both", expand=True)
                self.vscroll.pack(side="right", fill="y")
            for c in filtered:
                row = ContactRow(
                    self.rows_frame, c, on_toggle=self._on_row_toggle,
                    on_view=self._handle_view, on_edit=self._handle_edit,
                    on_delete=self._handle_delete,
                )
                row.pack(fill="x")
                if c.contact_id == self._expanded_contact_id:
                    row.set_expanded(True)
                self.rows[c.contact_id] = row

        self.stats_label.configure(text=f"Total contacts: {len(contacts)}")

    def _on_row_toggle(self, contact_id: int):
        if self._expanded_contact_id == contact_id:
            self._expanded_contact_id = None
        else:
            if self._expanded_contact_id is not None:
                old_row = self.rows.get(self._expanded_contact_id)
                if old_row is not None:
                    old_row.set_expanded(False)
            self._expanded_contact_id = contact_id
        row = self.rows.get(contact_id)
        if row is not None:
            row.set_expanded(self._expanded_contact_id == contact_id)

    # ------------------------------------------------------------------
    def _handle_view(self, contact_id: int):
        ViewContactWindow(self, self.manager, contact_id, on_change=self.refresh_list)

    def _handle_edit(self, contact_id: int):
        contact = self.manager.get_contact_by_id(contact_id)
        if contact is not None:
            EditContactWindow(self, self.manager, contact, on_saved=self.refresh_list)

    def _handle_delete(self, contact_id: int):
        contact = self.manager.get_contact_by_id(contact_id)
        if contact is None:
            return

        def do_delete():
            success, message = self.manager.delete_contact(contact_id)
            if self._expanded_contact_id == contact_id:
                self._expanded_contact_id = None
            self.refresh_list()
            if success:
                messagebox.showinfo("Success", message)

        ConfirmDialog(
            self, title="Delete Contact",
            message=f"Are you sure you want to delete '{contact.name}' from "
                    f"your phonebook? This action cannot be undone.",
            confirm_text="Delete", danger=True, on_confirm=do_delete,
        )

    # ------------------------------------------------------------------
    def _open_fab_menu(self):
        FabMenu(self, self.fab_button, on_add_contact=self._open_add,
                on_create_group=self._create_group_placeholder)

    def _open_add(self):
        AddContactWindow(self, self.manager, on_saved=self.refresh_list)

    def _create_group_placeholder(self):
        messagebox.showinfo(
            "Not available in this module",
            "Creating contact groups is part of Contact Group Management "
            "(FR-4), built in a separate module by another team member. "
            "This option is shown here to match the interface design, but "
            "isn't wired to real functionality in this part of the project.",
        )
