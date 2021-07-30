from flask import Flask, render_template, url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from turbo_flask import Turbo

import requests
from weatherAPI import search
# from weatherAPI import 
# import statements from prev projects, add/remove as needed

from forms import RegistrationForm, LoginForm
from sqlalchemy import exc, text
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user

from flask_migrate import Migrate
from blog import PostForm
from datetime import datetime

# import statements from prev projects, add/remove as needed
app = Flask(__name__)
turbo = Turbo(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '525901fece4e62b2eb11fa3c1a302835'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
    """An admin user capable of viewing reports.
    :param str username: username of user
    :param str email: email address of user
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user'

    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, anonymous users aren't supported."""
        return False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    
# basic homepage, to be edited as needed with layout.html and main.css
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# add more pages as needed
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = (bcrypt.generate_password_hash(form.password.data)
                    .decode('utf-8'))
        user = User(username=form.username.data,email=form.email.data,
                    password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash(f'Username or email account already exists!', 'success')
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for("home"))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("home"))
    return render_template("login.html", form=form)

# @app.route("/more")
# def second_page():

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data)
        # clear form
        form.title.data = ''
        form.content.data = ''
        # Add post to databasse
        db.session.add(post)
        db.session.commit()
        
        # Return message
        flash('Blog Post added', 'success')
        return redirect(url_for('home'))
    return render_template('blog.html',
                           form=form,
                           subtitle='Blog',
                           text='Welcome to Climate Change project!',
                           title='Blog')

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',
                           posts=posts,
                           subtitle='Post',
                           text='Lets make some change')
 

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
def update_post(id):
    post = Post.query.get_or_404(id)
  #  if post.author != current_user:
  #      abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
   # if post.author != current_user:
   #     abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/search_by_city", methods=["POST"])
def search_by_city():
    city = request.form["city"]
    data = search(city)
    print(data)
    return render_template("home.html", data=data) 
 

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
