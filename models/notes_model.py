from utils.db_connection import get_db_connection


class NotesModel:

    @staticmethod
    def add_note(
        subject,
        file_name
    ):

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO notes
            (
                subject,
                file_name
            )
            VALUES (?,?)
            """,
            (
                subject,
                file_name
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_notes():

        conn = get_db_connection()

        notes = conn.execute(
            """
            SELECT * FROM notes
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return notes

    @staticmethod
    def delete_note(
        note_id
    ):

        conn = get_db_connection()

        conn.execute(
            """
            DELETE FROM notes
            WHERE id=?
            """,
            (note_id,)
        )

        conn.commit()
        conn.close()