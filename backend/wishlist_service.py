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

# Table names
WISHLIST_TABLE = "wishlist"
WISHLIST_BOOKS_TABLE = "wishlist_books"  # Junction table for books in wishlists


@app.route('/wishlist', methods=['POST'])
def create_wishlist():
    """
    Create a new wishlist for a user.
    
    Expected JSON body:
    {
        "user_id": "uuid",
        "wishlist_name": "My Wishlist"
    }
    
    Response: None (just status code)
    """
    data = request.get_json()
    user_id = data.get("user_id") if data else None
    wishlist_name = data.get("wishlist_name") if data else None

    if not user_id or not wishlist_name:
        return jsonify({"error": "user_id and wishlist_name are required"}), 400

    try:
        # Check that user doesn't already have 3 wishlists
        existing = supabase.table("wishlists").select("id").eq("user_id", user_id).execute()
        if len(existing.data) >= 3:
            print(f"[ERROR] Maximum number of wishlists (3) already reached")
            return jsonify({"error": "User already has the maximum of 3 wishlists"}), 400

        # Check that wishlist name is unique for this user
        name_check = supabase.table("wishlists").select("id").eq("user_id", user_id).eq("name", wishlist_name).execute()
        if name_check.data:
            print(f"[ERROR] Wishlist with name {wishlist_name} already exists")
            return jsonify({"error": "A wishlist with that name already exists"}), 400

        supabase.table("wishlists").insert({"user_id": user_id, "name": wishlist_name}).execute()
        print(f"[DEBUG] Created wishlist {wishlist_name} for user id {user_id}")
        return jsonify({"message": "Wishlist created successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/wishlist/<int:wishlist_id>/books', methods=['POST'])
def add_book_to_wishlist(wishlist_id):
    """
    Add a book to a user's wishlist.
    
    Expected JSON body:
    {
        "book_id": 123
    }
    
    Response: None (just status code)
    """
    data = request.get_json()
    book_id = data.get("book_id") if data else None

    if not book_id:
        return jsonify({"error": "book_id is required"}), 400

    try:
        # Verify the wishlist exists
        wishlist_response = supabase.table("wishlists").select("id").eq("id", wishlist_id).execute()
        if not wishlist_response.data:
            return jsonify({"error": "Wishlist not found"}), 404

        # Verify the book exists
        book_response = supabase.table("books").select("id").eq("id", book_id).execute()
        if not book_response.data:
            return jsonify({"error": "Book not found"}), 404

        # Check if book is already in this wishlist
        existing = supabase.table("wishlist_books").select("id").eq("wishlist_id", wishlist_id).eq("book_id", book_id).execute()
        if existing.data:
            return jsonify({"error": "Book is already in this wishlist"}), 400

        # Insert book into wishlist
        supabase.table("wishlist_books").insert({"wishlist_id": wishlist_id, "book_id": book_id}).execute()
        print(f"[DEBUG] Added book {book_id} to wishlist {wishlist_id}")
        return jsonify({"message": "Book added to wishlist successfully."}), 201

    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/wishlist/<int:wishlist_id>/books/<int:book_id>', methods=['DELETE'])
def remove_book_from_wishlist(wishlist_id, book_id):
    """
    Remove a book from a user's wishlist.
    
    URL Parameters:
    - wishlist_id: ID of the wishlist
    - book_id: ID of the book to remove
    
    Response: None (just status code)
    """
    try:
        # Verify the wishlist exists
        wishlist_response = supabase.table("wishlists").select("id").eq("id", wishlist_id).execute()
        if not wishlist_response.data:
            return jsonify({"error": "Wishlist not found"}), 404

        # Verify the book is in the wishlist
        existing = supabase.table("wishlist_books").select("id").eq("wishlist_id", wishlist_id).eq("book_id", book_id).execute()
        if not existing.data:
            return jsonify({"error": "Book not found in wishlist"}), 404

        # Remove the book from the wishlist
        supabase.table("wishlist_books").delete().eq("wishlist_id", wishlist_id).eq("book_id", book_id).execute()
        print(f"[DEBUG] Removed book {book_id} from wishlist {wishlist_id}")
        return jsonify({"message": "Book removed from wishlist successfully."}), 200

    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/wishlist/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(wishlist_id):
    """
    Delete an entire wishlist and all books associated with it.

    URL Parameters:
    - wishlist_id: ID of the wishlist

    Response: None (just status code)
    """
    try:
        # Verify the wishlist exists
        wishlist_response = supabase.table("wishlists").select("id").eq("id", wishlist_id).execute()
        if not wishlist_response.data:
            return jsonify({"error": "Wishlist not found"}), 404

        # Remove all books from the wishlist first
        supabase.table("wishlist_books").delete().eq("wishlist_id", wishlist_id).execute()

        # Delete the wishlist itself
        supabase.table("wishlists").delete().eq("id", wishlist_id).execute()
        print(f"[DEBUG] Deleted wishlist {wishlist_id}")
        return jsonify({"message": "Wishlist deleted successfully."}), 200

    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/wishlist/<int:wishlist_id>/books', methods=['GET'])
def list_books_in_wishlist(wishlist_id):
    """
    List all books in a user's wishlist.
    
    URL Parameters:
    - wishlist_id: ID of the wishlist
    
    Response: JSON list of books in the wishlist
    """
    try:
        print(f"[DEBUG] Received request to list books for wishlist_id: {wishlist_id}")
        
        # Verify the wishlist exists
        wishlist_response = supabase.table("wishlists").select("*").eq("id", wishlist_id).execute()
        print(f"[DEBUG] Wishlist query response: {wishlist_response.data}")
        
        if not wishlist_response.data:
            print(f"[DEBUG] Wishlist not found for id: {wishlist_id}")
            return jsonify({"error": "Wishlist not found"}), 404
        
        print(f"[DEBUG] Wishlist found: {wishlist_response.data[0]}")
        
        # Query all book IDs associated with this wishlist
        wishlist_books_response = supabase.table("wishlist_books").select("book_id").eq("wishlist_id", wishlist_id).execute()
        print(f"[DEBUG] Wishlist books junction query response: {wishlist_books_response.data}")
        
        if not wishlist_books_response.data:
            print(f"[DEBUG] No books found in wishlist {wishlist_id}")
            return jsonify([]), 200
        
        # Extract book IDs
        book_ids = [item["book_id"] for item in wishlist_books_response.data]
        print(f"[DEBUG] Book IDs in wishlist: {book_ids}")
        
        # Fetch the actual book details
        books_response = supabase.table("books").select("*").in_("id", book_ids).execute()
        print(f"[DEBUG] Books query response: {books_response.data}")
        
        print(f"[DEBUG] Returning {len(books_response.data)} books")
        return jsonify(books_response.data), 200
        
    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


