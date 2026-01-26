from flask import Flask

app = Flask(__name__)

@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    # TODO: Create a function to add items to the wishlist => POST

    return "Empty messsage."

@app.route('/wishlist/<int:item_id>', methods=['DELETE'])
def remove_from_wishlist(item_id):
    # TODO: Create a function to remove items from the wishlist => DELETE

    return "Empty messsage."

@app.route('/wishlist', methods=['GET'])
def retrieve_wishlist():
    # TODO: Create a function to retrieve wishlist items => GET

    return "Empty messsage."

