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
WISHLIST_TABLE = "wishlist"


@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    """
    Add an item to the wishlist.
    
    Expected JSON body:
    {
        "name": "Item name",
        "description": "Optional description",
        "price": 29.99,  # optional
        "url": "https://example.com/item",  # optional
        "user_id": "uuid"  # optional - for when you add auth
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if "name" not in data:
            return jsonify({"error": "Item name is required"}), 400
        
        # Build the item to insert
        item = {
            "name": data.get("name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "url": data.get("url"),
            # Uncomment when you add auth:
            # "user_id": data.get("user_id")
        }
        
        # Remove None values to let Supabase use defaults
        item = {k: v for k, v in item.items() if v is not None}
        
        response = supabase.table(WISHLIST_TABLE).insert(item).execute()
        
        return jsonify({
            "message": "Item added to wishlist",
            "data": response.data
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/wishlist/<int:item_id>', methods=['DELETE'])
def remove_from_wishlist(item_id):
    """
    Remove an item from the wishlist by its ID.
    """
    try:
        # Check if item exists first
        existing = supabase.table(WISHLIST_TABLE).select("id").eq("id", item_id).execute()
        
        if not existing.data:
            return jsonify({"error": "Item not found"}), 404
        
        # Delete the item
        # If you add auth later, add: .eq("user_id", current_user_id)
        response = supabase.table(WISHLIST_TABLE).delete().eq("id", item_id).execute()
        
        return jsonify({
            "message": "Item removed from wishlist",
            "deleted_id": item_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/wishlist', methods=['GET'])
def retrieve_wishlist():
    """
    Retrieve all wishlist items.
    
    Optional query parameters:
    - limit: number of items to return (default: 100)
    - offset: pagination offset (default: 0)
    - user_id: filter by user (for when you add auth)
    """
    try:
        limit = request.args.get("limit", 100, type=int)
        offset = request.args.get("offset", 0, type=int)
        # user_id = request.args.get("user_id")  # Uncomment for auth
        
        query = supabase.table(WISHLIST_TABLE).select("*")
        
        # Uncomment when you add auth:
        # if user_id:
        #     query = query.eq("user_id", user_id)
        
        response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        
        return jsonify({
            "data": response.data,
            "count": len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)