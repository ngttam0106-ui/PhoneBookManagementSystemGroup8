import re


class Validator:

    @staticmethod
    def is_empty(value):
        return value.strip() == ""


    @staticmethod
    def is_valid_email(email):

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        return re.match(pattern, email) is not None


    @staticmethod
    def is_valid_phone(phone):

        pattern = r'^[0-9]{10}$'

        return re.match(pattern, phone) is not None


    @staticmethod
    def is_valid_password(password):

        return len(password) >= 6


    @staticmethod
    def is_same_password(password, confirm):

        return password == confirm