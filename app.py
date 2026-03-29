from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Use your existing variable names
SUPABASE_URL = os.getenv("DB_URL")
SUPABASE_KEY = os.getenv("DB_KEY")

print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return "Thanks!! :)"

#testing to see if connect
@app.route("/test")
def ping():
    try:
        supabase.table("users").select("*").limit(1).execute()
        return {"connected": True}
    except Exception as e:
        return {"connected": False, "error": str(e)}
    

#retrieve a user by their username
@app.route("/user", methods=["GET"])
def get_user():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username is required"}), 400

    # Query Supabase
    result = supabase.table("users").select("*").eq("username", username).execute()

    if result.data:
        return jsonify(result.data[0]), 200
    else:
        return jsonify({"error": "user not found"}), 404

#create user
@app.route("/user", methods=["POST"])
def create_user():

    #parse JSON 
    data = request.get_json()

    #get user name from input
    username = data.get("username")
    password = data.get("password")

    #verify username n password are provided
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    #checking if username already exists
    existing = supabase.table("users").select("*").eq("username", username).execute()

    #if it exists return error
    if existing.data:
        return jsonify({"error": "username already exists"}), 400

    #insert user into Supabase table
    supabase.table("users").insert({
        "username": username,
        "password": password,
        "name": data.get("name"),
        "email": data.get("email"),
        "home_address": data.get("home_address")
    }).execute()

    return '', 201

if __name__ == "__main__":
    app.run(debug=True)
