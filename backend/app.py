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
