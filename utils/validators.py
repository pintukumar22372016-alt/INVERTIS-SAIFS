import re


class Validators:

    @staticmethod
    def validate_email(email):

        pattern = (
            r'^[a-zA-Z0-9._%+-]+'
            r'@[a-zA-Z0-9.-]+'
            r'\.[a-zA-Z]{2,}$'
        )

        return bool(
            re.match(pattern, email)
        )

    @staticmethod
    def validate_password(password):

        return len(password) >= 6

    @staticmethod
    def validate_name(name):

        return len(name.strip()) >= 3

    @staticmethod
    def validate_rating(rating):

        try:

            rating = int(rating)

            return 1 <= rating <= 5

        except:

            return False

    @staticmethod
    def validate_text(text):

        return len(text.strip()) > 0