import os
from model.user import User
from model.contact import Contact
from model.group import Group
from model.contact_group import ContactGroup


class FileManager:

    USER_FILE = "data/users.txt"
    CONTACT_FILE = "data/contacts.txt"
    GROUP_FILE = "data/groups.txt"
    MAPPING_FILE = "data/mapping.txt"

    # ================= USER =================
    @staticmethod
    def update_user(updated_user):
        users = FileManager.load_users()
        for i, user in enumerate(users):
            if user.user_id == updated_user.user_id:
                users[i] = updated_user
                break
        FileManager.save_users(users)

    @staticmethod
    def load_users():

        users = []

        try:
            with open(FileManager.USER_FILE, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if line == "":
                        continue

                    user = User.from_line(line)

                    if user:
                        users.append(user)

        except FileNotFoundError:
            pass

        return users

    @staticmethod
    def save_users(users):

        with open(FileManager.USER_FILE, "w", encoding="utf-8") as file:

            for user in users:
                file.write(user.to_line() + "\n")

    @staticmethod
    def append_user(user):

        with open(FileManager.USER_FILE, "a", encoding="utf-8") as file:

            file.write(user.to_line() + "\n")

    # ================= CONTACT =================
    @staticmethod
    def reset_all_contacts(current_user):
        """Xóa danh bạ thuộc về người dùng hiện tại."""
        all_contacts = FileManager.load_contacts()
        remaining_contacts = [c for c in all_contacts if c.user_id != current_user.user_id]
        FileManager.save_contacts(remaining_contacts)

    @staticmethod
    def load_contacts():

        contacts = []

        try:

            with open(FileManager.CONTACT_FILE, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if line == "":
                        continue

                    data = line.split("|")

                    contact = Contact(
                        contact_id=int(data[0]),
                        user_id=int(data[1]),
                        name=data[2],
                        phone=data[3],
                        email=data[4],
                        address=data[5],
                        avatar=data[6],
                        favorite=data[7] == "True",
                        emergency=data[8] == "True"
                    )

                    contacts.append(contact)

        except FileNotFoundError:
            pass

        return contacts

    @staticmethod
    def save_contacts(contacts):

        with open(FileManager.CONTACT_FILE, "w", encoding="utf-8") as file:

            for contact in contacts:

                file.write(
                    f"{contact.contact_id}|"
                    f"{contact.user_id}|"
                    f"{contact.name}|"
                    f"{contact.phone}|"
                    f"{contact.email}|"
                    f"{contact.address}|"
                    f"{contact.avatar}|"
                    f"{contact.favorite}|"
                    f"{contact.emergency}\n"
                )

    # ================= GROUP =================

    @staticmethod
    def load_groups():

        groups = []

        try:

            with open(FileManager.GROUP_FILE, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if line == "":
                        continue

                    data = line.split("|")

                    group = Group(
                        group_id=int(data[0]),
                        user_id=int(data[1]),
                        group_name=data[2]
                    )

                    groups.append(group)

        except FileNotFoundError:
            pass

        return groups

    @staticmethod
    def save_groups(groups):

        with open(FileManager.GROUP_FILE, "w", encoding="utf-8") as file:

            for group in groups:

                file.write(
                    f"{group.group_id}|"
                    f"{group.user_id}|"
                    f"{group.group_name}\n"
                )

    # ================= CONTACT GROUP =================

    @staticmethod
    def load_mapping():

        mappings = []

        try:

            with open(FileManager.MAPPING_FILE, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if line == "":
                        continue

                    data = line.split("|")

                    mapping = ContactGroup(
                        mapping_id=int(data[0]),
                        contact_id=int(data[1]),
                        group_id=int(data[2])
                    )

                    mappings.append(mapping)

        except FileNotFoundError:
            pass

        return mappings

    @staticmethod
    def save_mapping(mappings):

        with open(FileManager.MAPPING_FILE, "w", encoding="utf-8") as file:

            for mapping in mappings:

                file.write(
                    f"{mapping.mapping_id}|"
                    f"{mapping.contact_id}|"
                    f"{mapping.group_id}\n"
                )