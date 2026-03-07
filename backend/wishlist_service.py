from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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
    # TODO: Get user_id and wishlist_name from request JSON
    # TODO: Validate that both fields are provided
    # TODO: Check that user doesn't already have 3 wishlists
    # TODO: Check that wishlist name is unique for this user
    # TODO: Insert new wishlist into database
    # TODO: Return appropriate status code
    pass


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
    # TODO: Get book_id from request JSON
    # TODO: Validate that book_id is provided
    # TODO: Verify the wishlist exists
    # TODO: Verify the book exists
    # TODO: Check if book is already in this wishlist
    # TODO: Insert book into wishlist
    # TODO: Return appropriate status code
    pass


@app.route('/wishlist/<int:wishlist_id>/books/<int:book_id>', methods=['DELETE'])
def remove_book_from_wishlist(wishlist_id, book_id):
    """
    Remove a book from a user's wishlist (and add to shopping cart).
    
    URL Parameters:
    - wishlist_id: ID of the wishlist
    - book_id: ID of the book to remove
    
    Response: None (just status code)
    """
    # TODO: Verify the wishlist exists
    # TODO: Verify the book is in the wishlist
    # TODO: Remove the book from the wishlist
    # TODO: (Optional) Add the book to user's shopping cart
    # TODO: Return appropriate status code
    pass


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


if __name__ == "__main__":
    app.run(debug=True)