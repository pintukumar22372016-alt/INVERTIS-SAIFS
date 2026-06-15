from utils.db_connection import get_db_connection


class DoubtModel:

    @staticmethod
    def add_doubt(
        subject,
        question
    ):

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO doubts
            (
                subject,
                question
            )
            VALUES (?,?)
            """,
            (
                subject,
                question
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_doubts():

        conn = get_db_connection()

        doubts = conn.execute(
            """
            SELECT * FROM doubts
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return doubts

    @staticmethod
    def answer_doubt(
        doubt_id,
        answer
    ):

        conn = get_db_connection()

        conn.execute(
            """
            UPDATE doubts
            SET answer=?
            WHERE id=?
            """,
            (
                answer,
                doubt_id
            )
        )

        conn.commit()
        conn.close()