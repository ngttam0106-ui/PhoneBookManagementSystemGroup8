# -*- coding: utf-8 -*-
"""
models.py
---------
Tang Model (thuc the), tuong ung voi bang "Contacts" trong Class Diagram va
Data Model (Muc VI bao cao "Phone Book Management System").

Contacts: Stores the list of acquaintances and friends belonging to the users.
Each contact saves: name, phone number, email, address, creation date, avatar_path.
Unique Key (user_id, phone_number) -> khong duoc trung so dien thoai trong
cung 1 danh ba cua 1 user.

Lop Contact CHI la mot data class (thuc the thuan tuy), KHONG chua logic
nghiep vu (validate, kiem tra trung...). Logic nghiep vu nam o ContactManager
(contact_manager.py) - tuong ung Process 2.0 "Contact Management" trong DFD.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional


@dataclass
class Contact:
    """
    Thuoc tinh:
        contact_id   : Khoa chinh (Primary Key)
        user_id      : Khoa ngoai (Foreign Key) -> tham chieu den Users.
                        Moi Contact luon thuoc ve DUNG 1 User (quan he 1-N,
                        xem Muc VI.2.1 "Relationship between Users and Contacts").
        name         : Ho ten lien he (BAT BUOC - FR-2)
        phone_number : So dien thoai (BAT BUOC, duy nhat trong pham vi 1 user)
        email        : Email lien he (khong bat buoc)
        address      : Dia chi (khong bat buoc)
        avatar_path  : Duong dan file anh dai dien (khong bat buoc)
        created_at   : Ngay gio tao lien he ("creation date" trong Data Model)
        is_favorite  : Co danh dau "Favorite" (UC12 - Mark Special Contact)
        is_emergency : Co danh dau "Emergency" (FR-2) / "Urgent" (UC12) - cung
                        mot tinh nang, bao cao dung 2 ten khac nhau o 2 cho;
                        ta thong nhat dung ten "Emergency" (giong FR-2 va man
                        hinh View o Muc VII.12: "+ Add emergency contacts").
    """

    contact_id: int
    user_id: int
    name: str
    phone_number: str
    email: str = ""
    address: str = ""
    avatar_path: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    is_favorite: bool = False
    is_emergency: bool = False

    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Chuyen thanh dict de ghi xuong text.txt (dang JSON Lines)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        """Dung khi doc du lieu tu text.txt len lai thanh doi tuong Contact."""
        return cls(
            contact_id=int(data["contact_id"]),
            user_id=int(data["user_id"]),
            name=data.get("name", ""),
            phone_number=data.get("phone_number", ""),
            email=data.get("email", ""),
            address=data.get("address", ""),
            avatar_path=data.get("avatar_path", ""),
            created_at=data.get("created_at", ""),
            is_favorite=bool(data.get("is_favorite", False)),
            is_emergency=bool(data.get("is_emergency", False)),
        )

    # ------------------------------------------------------------------
    @property
    def priority_rank(self) -> tuple:
        """
        Khoa sap xep phuc vu yeu cau "priority display" (FR-2:
        "...add it to the Favorite list for quick access and priority
        display"). Uu tien: Emergency -> Favorite -> A-Z theo ten.
        """
        return (not self.is_emergency, not self.is_favorite, self.name.lower())

    @property
    def initial(self) -> str:
        """Ky tu dau tien cua ten, dung cho avatar placeholder."""
        stripped = (self.name or "").strip()
        return stripped[0].upper() if stripped else "?"
