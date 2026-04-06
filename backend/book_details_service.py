from flask import request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from app import app
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.environ.get("DB_URL")
SUPABASE_KEY = os.environ.get("DB_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Tables
BOOKS_TABLE = "books"
AUTHORS_TABLE = "authors"

# Get book details from isbn.
@app.route("/books/<string:book_isbn>", methods=["GET"])
def get_book_details(book_isbn):
    try:
        response = supabase.table(BOOKS_TABLE).select("*").eq("isbn", book_isbn).execute()

        if not response.data:
            return jsonify({"message": "Book not found"}), 404

        return jsonify(response.data[0]), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Administrator post book with details.
@app.route("/books", methods=["POST"])
def post_book():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_details = ["isbn", "title", "author", "price"]
        for detail in required_details:
            if detail not in data:
                return jsonify({"error": f"{detail} is missing"}), 400

        book = {
            "isbn": data.get("isbn"),
            "title": data.get("title"),
            "author": data.get("author"),
            "author_id": data.get("author_id"),
            "description": data.get("description"),
            "price": data.get("price"),
            "genre": data.get("genre"),
            "publisher": data.get("publisher"),
            "year_published": data.get("year_published"),
            "copies_sold": data.get("copies_sold", 0)
        }

        book = {k: v for k, v in book.items() if v is not None}

        response = supabase.table(BOOKS_TABLE).insert(book).execute()

        return jsonify({
            "message": "Book created successfully",
            "data": response.data
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Administrator POST author with details.
@app.route("/authors", methods=["POST"])
def post_author():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_details = ["first_name", "last_name"]
        for detail in required_details:
            if detail not in data:
                return jsonify({"error": f"{detail} is missing"}), 400

        author = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "biography": data.get("biography"),
            "publisher": data.get("publisher"),
        }

        author = {k: v for k, v in author.items() if v is not None}

        response = supabase.table(AUTHORS_TABLE).insert(author).execute()

        return jsonify({
            "message": "Author created successfully",
            "data": response.data
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get list of books by author ID.
@app.route("/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author(author_id):
    try:
        # First check if author exists
        author_response = supabase.table(AUTHORS_TABLE).select("*").eq("id", author_id).execute()

        if not author_response.data:
            return jsonify({"error": "Author not found"}), 404

        # Get all books by this author
        books_response = supabase.table(BOOKS_TABLE).select("*").eq("author_id", author_id).execute()

        return jsonify({
            "author": author_response.data[0],
            "books": books_response.data,
            "count": len(books_response.data)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

