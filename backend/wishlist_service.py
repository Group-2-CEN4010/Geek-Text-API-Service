from flask import Flask

app = Flask(__name__)

@app.route('/wishlist/add', methods=['POST'])
def add_to_wishlist():
    # TODO: Create a function to add items to the wishlist => POST

    return "Empty messsage."

@app.route('wishlist/remove', methods=['DELETE'])
def remove_from_wishlist():
    # TODO: Create a function to remove items from the wishlist => DELETE

    return "Empty messsage."

@app.route('wishlist/get', methods=['GET'])
def retrieve_wishlist():
    # TODO: Create a function to retrieve wishlist items => GET

    return "Empty messsage."

