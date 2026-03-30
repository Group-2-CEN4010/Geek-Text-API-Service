from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from app import app
import os

load_dotenv()

SUPABASE_URL = os.environ.get("DB_URL")
SUPABASE_KEY = os.environ.get("DB_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#table name
ShoppingCart = "shopping_cart"

@app.route('/shopping_cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    user_id = data.get("user_id")
    book_id = data.get("book_id")
    
    existing = supabase.table("shopping_cart") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("book_id", book_id) \
        .execute()

    if existing.data:
        # update quantity
        supabase.table("shopping_cart") \
            .update({"quantity": existing.data[0]["quantity"] + 1}) \
            .eq("user_id", user_id) \
            .eq("book_id", book_id) \
            .execute()

        return jsonify({"message": "Quantity updated"}), 200

    else:
        # insert new item
        supabase.table("shopping_cart").insert({
            "user_id": user_id,
            "book_id": book_id,
            "quantity": 1
        }).execute()

        return jsonify({"message": "Book added"}), 201
    
#gets all books in the shopping cart for a specific user, including book details
@app.route('/shopping_cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    response = supabase.table("shopping_cart")\
        .select("*, books(*)")\
        .eq("user_id", user_id)\
        .execute()

    return jsonify(response.data), 200

#deletes a specific book from the shopping cart for a specific user
@app.route('/shopping_cart/delete', methods=['DELETE'])
def delete_from_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    supabase.table("shopping_cart")\
        .delete()\
        .eq("user_id", user_id)\
        .eq("book_id", book_id)\
        .execute()

    return jsonify({"message": "Book removed"}), 200

#calculates the subtotal for all items in the shopping cart for a specific user
@app.route('/shopping_cart/<user_id>/subtotal', methods=['GET'])
def get_subtotal(user_id):
    response = supabase.table(ShoppingCart)\
        .select("quantity, books(price)")\
        .eq("user_id", user_id)\
        .execute()

    subtotal = 0

    for item in response.data:
        price = item["books"]["price"]
        quantity = item["quantity"]
        subtotal += price * quantity

    return jsonify({"subtotal": subtotal}), 200

if __name__ == "__main__":
    app.run(debug=True)