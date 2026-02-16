from flask import Flask
group2 = Flask(__name__) #start website
@group2.route("/get") #creates URL
def my_route(): #define what happens when someone visits the URL
    return {"message": "This is my GET route for Sprint 2"}
  
if __name__ == "__main__":
  get.run(debug=True)
