import os

from model.user import User


class FileManager:

    USER_FILE = "data/users.txt"

    @staticmethod
    def create_data_folder():

        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(FileManager.USER_FILE):

            with open(FileManager.USER_FILE, "w", encoding="utf-8"):
                pass


    @staticmethod
    def load_users():

        FileManager.create_data_folder()

        users = []

        with open(FileManager.USER_FILE,
                  "r",
                  encoding="utf-8") as file:

            for line in file:

                if line.strip() == "":
                    continue

                user = User.from_line(line)

                if user is not None:
                    users.append(user)

        return users


    @staticmethod
    def save_users(users):

        FileManager.create_data_folder()

        with open(FileManager.USER_FILE,
                  "w",
                  encoding="utf-8") as file:

            for user in users:
                file.write(user.to_line() + "\n")


    @staticmethod
    def append_user(user):

        FileManager.create_data_folder()

        with open(FileManager.USER_FILE,
                  "a",
                  encoding="utf-8") as file:

            file.write(user.to_line() + "\n")