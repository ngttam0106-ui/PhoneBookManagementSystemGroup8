import hashlib


class Security:

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Convert password to SHA-256 hash
        """

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def verify_password(password: str,
                        hashed_password: str) -> bool:
        """
        Verify password
        """

        return Security.hash_password(password) == hashed_password