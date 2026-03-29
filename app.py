<<<<<<< HEAD
from flask import Flask
from wishlist_service import wishlist_bp

app = Flask(__name__) # Creates an instance of the Flask object

app.register_blueprint(wishlist_bp)

@app.route("/") # This is the API route. Whenever "/" is requested, it's going to run the function below it
def home(): # This function will run when the route "/" is visited
    return "Server is Running! Yayyyy!!"

# Runs the server
if __name__ == "__main__":
    app.run()
=======
from flask import Flask, jsonify
from book_browsing import book_browsing_bp

app = Flask(__name__)

app.register_blueprint(book_browsing_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "GeekText API is running"}), 200

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
>>>>>>> 08c158f (Add book browsing feature)
