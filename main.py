from flask import Flask, render_template, url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from turbo_flask import Turbo
import requests
from weatherAPI import search
# from weatherAPI import 
# import statements from prev projects, add/remove as needed

app = Flask(__name__)

# basic homepage, to be edited as needed with layout.html and main.css
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
# add more pages as needed
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/search_by_city", methods=["POST"])
def search_by_city():
    city = request.form["city"]
    data = search(city)
    print(data)
    return render_template("home.html", data=data) 

  

    
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
