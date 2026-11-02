import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().with_name("library.db")


def connect_db():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issue_records (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'Issued',
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO admins (username, password)
        VALUES (?, ?)
    """, ("admin", "admin123"))

    conn.commit()
    conn.close()


def check_admin(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM admins WHERE username = ? AND password = ?",
        (username, password)
    )
    result = cursor.fetchone() is not None
    conn.close()
    return result


if __name__ == "__main__":
    create_table()
    print("Database connected successfully!")
    print("All tables created successfully!")
