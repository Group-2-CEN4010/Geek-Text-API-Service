from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/") # This is the API route. Whenever "/" is requested, it's going to run the function below it
def home(): # This function will run when the route "/" is visited
    return "Server is Running! Yayyyy!!"



if __name__ == "__main__":
    app.run(debug=True)