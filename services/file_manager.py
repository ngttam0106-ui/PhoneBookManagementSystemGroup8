import os


class FileManager:

    def load_users(self):
        users = []

        if not os.path.exists("data/users.txt"):
            return users

        with open("data/users.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    users.append(line)

        return users

    def save_users(self, users):
        with open("data/users.txt", "w", encoding="utf-8") as file:
            for user in users:
                file.write(user + "\n")

    def load_contacts(self):
        contacts = []

        if not os.path.exists("data/contacts.txt"):
            return contacts

        with open("data/contacts.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    contacts.append(line)

        return contacts

    def save_contacts(self, contacts):
        with open("data/contacts.txt", "w", encoding="utf-8") as file:
            for contact in contacts:
                file.write(contact + "\n")

    def load_groups(self):
        groups = []

        if not os.path.exists("data/groups.txt"):
            return groups

        with open("data/groups.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    groups.append(line)

        return groups

    def save_groups(self, groups):
        with open("data/groups.txt", "w", encoding="utf-8") as file:
            for group in groups:
                file.write(group + "\n")

    def load_mapping(self):
        mapping = []

        if not os.path.exists("data/mapping.txt"):
            return mapping

        with open("data/mapping.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    mapping.append(line)

        return mapping

    def save_mapping(self, mapping):
        with open("data/mapping.txt", "w", encoding="utf-8") as file:
            for item in mapping:
                file.write(item + "\n")