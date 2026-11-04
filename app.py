
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "online-book-catalog-secret"

DATABASE = os.path.join(os.path.dirname(__file__), "books.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    search = request.args.get("search", "").strip()

    conn = get_db_connection()

    if search:
        books = conn.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    else:
        books = conn.execute(
            "SELECT * FROM books ORDER BY id DESC"
        ).fetchall()

    conn.close()
    return render_template("index.html", books=books, search=search)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    genre = request.form.get("genre", "").strip()
    year = request.form.get("year", "").strip()

    if not all([title, author, isbn, genre, year]):
        flash("All fields are required.")
        return redirect(url_for("index"))

    try:
        year = int(year)
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO books (title, author, isbn, genre, year)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, isbn, genre, year))
        conn.commit()
        conn.close()
        flash("Book added successfully!")

    except sqlite3.IntegrityError:
        flash("A book with this ISBN already exists.")
    except ValueError:
        flash("Publication year must be a number.")

    return redirect(url_for("index"))


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    flash("Book deleted successfully!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
