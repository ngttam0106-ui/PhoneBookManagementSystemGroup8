import os

from model.user import User
from model.contact import Contact
from model.group import Group
from model.contact_group import ContactGroup


class FileManager:

    def __init__(self):
        self.user_file = "data/users.txt"
        self.contact_file = "data/contacts.txt"
        self.group_file = "data/groups.txt"
        self.mapping_file = "data/mapping.txt"

    # ================= USER =================

    def load_users(self):
        users = []

        try:
            with open(self.user_file, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    users.append(line)

        except FileNotFoundError:
            pass

        return users

    def save_users(self, users):

        with open(self.user_file, "w", encoding="utf-8") as file:

            for user in users:
                file.write(str(user) + "\n")

    # ================= CONTACT =================

    def load_contacts(self):

        contacts = []

        try:
            with open(self.contact_file, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if not line:
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

    def save_contacts(self, contacts):

        with open(self.contact_file, "w", encoding="utf-8") as file:

            for contact in contacts:

                line = (
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

                file.write(line)

    # ================= GROUP =================

    def load_groups(self):

        groups = []

        try:
            with open(self.group_file, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if not line:
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

    def save_groups(self, groups):

        with open(self.group_file, "w", encoding="utf-8") as file:

            for group in groups:

                line = (
                    f"{group.group_id}|"
                    f"{group.user_id}|"
                    f"{group.group_name}\n"
                )

                file.write(line)

    # ================= CONTACT GROUP =================

    def load_mapping(self):

        mappings = []

        try:

            with open(self.mapping_file, "r", encoding="utf-8") as file:

                for line in file:

                    line = line.strip()

                    if not line:
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

    def save_mapping(self, mappings):

        with open(self.mapping_file, "w", encoding="utf-8") as file:

            for mapping in mappings:

                line = (
                    f"{mapping.mapping_id}|"
                    f"{mapping.contact_id}|"
                    f"{mapping.group_id}\n"
                )

                file.write(line)