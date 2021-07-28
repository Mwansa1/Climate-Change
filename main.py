from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from turbo_flask import Turbo
# import statements from prev projects, add/remove as needed

app = Flask(__name__)

# basic homepage, to be edited as needed with layout.html and main.css
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',
                           subtitle='Home Page',
                           text='Welcome to Climate Change project!')
# add more pages as needed
# @app.route("/login")
# def login():
    
# @app.route("/more")
# def second_page():
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
