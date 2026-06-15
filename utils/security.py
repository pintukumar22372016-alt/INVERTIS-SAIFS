from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


class SecurityManager:

    @staticmethod
    def hash_password(password):

        return generate_password_hash(
            password
        )

    @staticmethod
    def verify_password(
        stored_password,
        provided_password
    ):

        return check_password_hash(
            stored_password,
            provided_password
        )

    @staticmethod
    def sanitize_input(text):

        if not text:
            return ""

        return (
            text.strip()
                .replace("<", "")
                .replace(">", "")
        )