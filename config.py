import os


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SECRET_KEY = (
        "saifs_college_project_2026"
    )

    DATABASE = os.path.join(
        BASE_DIR,
        "database",
        "db.sqlite3"
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads",
        "notes"
    )

    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )

    ALLOWED_EXTENSIONS = {
        "pdf",
        "doc",
        "docx",
        "ppt",
        "pptx"
    }