import re


class Validator:

    @staticmethod
    def is_empty(text):
        if text is None:
            return True
        return text.strip() == ""

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        pattern = r'^0\d{9}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def is_valid_password(password):
        return len(password) >= 6

    @staticmethod
    def is_same_password(password, confirm_password):
        return password == confirm_password