from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Table name
BOOKS_TABLE = "books"

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

if __name__ == "__main__":
    app.run(debug=True)