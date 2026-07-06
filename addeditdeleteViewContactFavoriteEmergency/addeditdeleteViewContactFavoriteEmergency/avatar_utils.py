# -*- coding: utf-8 -*-
"""
avatar_utils.py
----------------
Ham tien ich tao ANH DAI DIEN (avatar) HINH TRON cho Contact, phuc vu cac man
hinh Add/Edit/View (Muc VII.10, VII.12, VII.13): "Avatar Selection Area",
"Add a Photo Button", "Photo Editing Button".

Neu contact co avatar_path va file anh ton tai -> hien ANH THAT (crop tron).
Neu chua co anh -> hien HINH TRON MAU + CHU CAI DAU cua ten (placeholder),
mau sac duoc sinh on dinh tu ten (cung 1 ten luon ra cung 1 mau).

Yeu cau thu vien ngoai: Pillow (PIL). Cai dat bang:
    pip install pillow
"""

from __future__ import annotations
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont, ImageTk

# Bang mau de sinh avatar placeholder (mau pastel/hien dai, du tuong phan de
# doc chu trang o giua)
_PALETTE = [
    "#3057D5", "#1E9E5A", "#F5A623", "#9B59B6",
    "#E67E22", "#16A085", "#D24D57", "#2C3E50",
]


def _color_for_name(name: str) -> str:
    """Sinh mau on dinh (deterministic) tu ten, dung MD5 de bam."""
    digest = hashlib.md5((name or "?").encode("utf-8")).hexdigest()
    index = int(digest, 16) % len(_PALETTE)
    return _PALETTE[index]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    """Thu tai font chu dam; neu khong tim thay thi dung font mac dinh cua
    Pillow (van chay duoc, chi la khong dep bang)."""
    candidates = [
        "DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "arialbd.ttf",
        "Arial Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def make_fab_icon(size: int = 56, bg_color: str = "#3057D5", fg_color: str = "white") -> ImageTk.PhotoImage:
    """
    Sinh icon hinh tron mau + dau '+' mau trang o giua, dung cho nut noi
    "Floating Action Button" o goc duoi ben phai man hinh danh sach lien he
    (Muc VII.11 / VII.16 - nut '+' mo popup "Create New Group" / "Add Contact").
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size - 1, size - 1), fill=bg_color)
    cx = cy = size / 2
    arm = size * 0.26
    thickness = max(3, int(size * 0.09))
    draw.line((cx - arm, cy, cx + arm, cy), fill=fg_color, width=thickness)
    draw.line((cx, cy - arm, cx, cy + arm), fill=fg_color, width=thickness)
    return ImageTk.PhotoImage(img)


def make_avatar_image(name: str, avatar_path: str = "", size: int = 64) -> ImageTk.PhotoImage:
    """
    Tra ve mot ImageTk.PhotoImage HINH TRON, san sang gan vao ttk.Label/
    Treeview cua Tkinter.

    Tham so:
        name        : ten lien he (dung de lay chu cai dau + sinh mau placeholder)
        avatar_path : duong dan file anh da chon (co the rong neu chua co anh)
        size        : kich thuoc canh vuong truoc khi crop tron (pixel)
    """
    base_image = None
    if avatar_path and os.path.isfile(avatar_path):
        try:
            base_image = Image.open(avatar_path).convert("RGB").resize(
                (size, size), Image.LANCZOS
            )
        except Exception:
            base_image = None  # anh loi/khong doc duoc -> roi xuong placeholder

    if base_image is None:
        bg_color = _color_for_name(name)
        base_image = Image.new("RGB", (size, size), bg_color)
        draw = ImageDraw.Draw(base_image)
        initial = (name.strip()[0].upper() if name and name.strip() else "?")
        font = _load_font(int(size * 0.45))
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((size - text_w) / 2 - bbox[0], (size - text_h) / 2 - bbox[1]),
            initial, fill="white", font=font,
        )

    # Crop hinh vuong -> hinh tron bang mat na (mask) hinh elip
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    circular = Image.new("RGBA", (size, size))
    circular.paste(base_image, (0, 0), mask)

    return ImageTk.PhotoImage(circular)
