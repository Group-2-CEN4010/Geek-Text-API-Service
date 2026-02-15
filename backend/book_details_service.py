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

@app.route("/books/<string:book_isbn>", methods=["GET"])
def get_book_details(book_isbn):
    try:
        response = supabase.table(BOOKS_TABLE).select("*").eq("isbn", book_isbn).execute()

        if not response.data:
            return jsonify({"message": "Book not found"}), 404

        return jsonify(response.data[0]), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)