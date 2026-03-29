#Sprint 2:
#from flask import Flask
#group2 = Flask(__name__) #start website
#@group2.route("/get") #creates URL
#def my_route(): #define what happens when someone visits the URL
 #   return {"message": "This is my get route for Sprint 2"}
  
#if __name__ == "__main__":
#  group2.run(debug=True)

from flask import Flask, jsonify, request

group2 = Flask(__name__)  # start website

# Sample user data simulating your database
users = {
    "joseph56": {
        "username": "joseph56",
        "name": "Joseph",
        "email": "josephpbr@gmail.com",
        "home_address": "456 Blue st."
    }
}

@group2.route("/user", methods=["GET"])
def get_user():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username parameter is required"}), 400
    user = users.get(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "user not found"}), 404

if __name__ == "__main__":
    group2.run(debug=True)
