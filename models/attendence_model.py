from utils.db_connection import get_db_connection


class AttendanceModel:

    @staticmethod
    def mark_attendance(
        student_name,
        subject,
        status
    ):

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO attendance
            (
                student_name,
                subject,
                status
            )
            VALUES (?,?,?)
            """,
            (
                student_name,
                subject,
                status
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_attendance():

        conn = get_db_connection()

        data = conn.execute(
            """
            SELECT * FROM attendance
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return data

    @staticmethod
    def get_student_attendance(
        student_name
    ):

        conn = get_db_connection()

        data = conn.execute(
            """
            SELECT * FROM attendance
            WHERE student_name=?
            """,
            (student_name,)
        ).fetchall()

        conn.close()

        return data