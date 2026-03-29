from flask import Blueprint, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
import os
from app import app

load_dotenv()

SUPABASE_URL = os.getenv("DB_URL")
SUPABASE_KEY = os.getenv("DB_KEY")



supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "book browsing route works"}), 200

@app.route("/books/top-sellers", methods=["GET"])
def get_top_sellers():
    try:
        response = (
            supabase.table("books")
            .select("*")
            .order("copies_sold", desc=True)
            .limit(10)
            .execute()
        )
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books/genre/<genre>", methods=["GET"])
def get_books_by_genre(genre):
    try:
        response = (
            supabase.table("books")
            .select("*")
            .ilike("genre", genre)
            .execute()
        )
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books/rating/<float:min_rating>", methods=["GET"])
def get_books_by_rating(min_rating):
    try:
        response = (
            supabase.table("books")
            .select("*")
            .gte("average_rating", min_rating)
            .order("average_rating", desc=True)
            .execute()
        )
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books/discount", methods=["PATCH"])
def discount_books_by_publisher():
    try:
        data = request.get_json()
        publisher = data.get("publisher")
        discount_percent = data.get("discount_percent")

        if not publisher or discount_percent is None:
            return jsonify({"error": "publisher and discount_percent are required"}), 400

        if discount_percent < 0 or discount_percent > 100:
            return jsonify({"error": "discount_percent must be between 0 and 100"}), 400

        books_response = (
            supabase.table("books")
            .select("id, price")
            .ilike("publisher", publisher)
            .execute()
        )

        books = books_response.data

        if not books:
            return jsonify({"message": "No books found for that publisher"}), 404

        for book in books:
            old_price = float(book["price"])
            new_price = round(old_price * (1 - discount_percent / 100), 2)

            (
                supabase.table("books")
                .update({"price": new_price})
                .eq("id", book["id"])
                .execute()
            )

        return jsonify({"message": f"Discount applied to books from publisher '{publisher}'"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500