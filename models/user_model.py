from utils.db_connection import get_db_connection


class UserModel:

    @staticmethod
    def create_user(name, college_id, password, role):

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO users
            (name,college_id,password,role)
            VALUES (?,?,?,?)
            """,
            (name, college_id, password, role)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_college_id(college_id):

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE college_id=?
            """,
            (college_id,)
        ).fetchone()

        conn.close()

        return user

    @staticmethod
    def get_all_users():

        conn = get_db_connection()

        users = conn.execute(
            "SELECT * FROM users"
        ).fetchall()

        conn.close()

        return users

    @staticmethod
    def delete_user(user_id):

        conn = get_db_connection()

        conn.execute(
            """
            DELETE FROM users
            WHERE id=?
            """,
            (user_id,)
        )

        conn.commit()
        conn.close()