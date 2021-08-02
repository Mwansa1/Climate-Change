from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from turbo_flask import Turbo

import requests
from weatherAPI import search
# from weatherAPI import 
# import statements from prev projects, add/remove as needed

from forms import RegistrationForm, LoginForm, SuggestionForm
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

login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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

    posts = db.relationship('Posts', backref='author', lazy=True)

    def is_active(self):
        """True, all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, anonymous users aren't supported."""
        return False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class FoodSuggestion(db.Model):
    __tablename__ = 'food_suggestion'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    
    def __repr__(self):
        return f"FoodSuggestion('{self.id}', '{self.content}')"

class TravelSuggestion(db.Model):
    __tablename__ = 'travel_suggestion'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    
    def __repr__(self):
        return f"TravelSuggestion('{self.id}', '{self.content}')"

class EnergySuggestion(db.Model):
    __tablename__ = 'energy_suggestion'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    
    def __repr__(self):
        return f"EnergySuggestion('{self.id}', '{self.content}')"
    
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
            flash(f'Username or email account already exists!', 'danger')
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
                flash(f'Account logged in!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", form=form)

# potentially the logout feature
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
# @app.route("/more")
# def second_page():

@app.route("/suggestions", methods=['GET', 'POST'])
def suggestions():
    # food suggestions
    food_suggestions = [
        {'id': 0, 'content': 'Avoid overly processed foods. These foods have a high carbon footprint due to manufacuring, traveling, and distribution.'},
        {'id': 1, 'content': 'Buy locally made food, your carbon footprint will decrease as a result.'},
        {'id': 2, 'content': 'Eat less red meat to reduce your carbon footprint.'},
        {'id': 3, 'content': 'Buy fair trade products to reduce your carbon footprint.'},
        {'id': 4, 'content': 'Grow your own food to save natural resources in mass production.'}
    ]
    
    travel_suggestions = [
        {'id': 0, 'content': 'Ride a bike or walk to places that are close by instead of driving.'},
        {'id': 1, 'content': 'Use public transportation instead of driving.'},
        {'id': 2, 'content': 'Mitigate the negative impact of air travel by flying less often.'},
        {'id': 3, 'content': 'Don’t speed! Gas mileage declines rapidly above 60 mph. Each 5 mph increase above 60 is like paying an additional 10 cents a gallon for gasoline.'},
        {'id': 4, 'content': 'Drive hybrid or electric vehicles to reduce pollution from exhaust.'}
    ]
    
    energy_suggestions = [
        {'id': 0, 'content': 'Unplug electronics you are not using to save energy.'},
        {'id': 1, 'content': 'Replace your light bulb with LED ones, they save 75% more energy!'},
        {'id': 2, 'content': 'Turn off the lights in rooms you are not in.'},
        {'id': 3, 'content': 'Avoid turning on the light when you can use sunlight instead.'},
        {'id': 4, 'content': 'Use dimmers in common areas of your house to save a significant amount of energy'}
    ]
    
    # populate food suggestion table
    for fs in food_suggestions:
        suggestion = FoodSuggestion(id=fs['id'], content=fs['content'])
        try:
            db.session.add(suggestion)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
    
    # populate travel suggestion table
    for ts in travel_suggestions:
        suggestion = TravelSuggestion(id=ts['id'], content=ts['content'])
        try:
            db.session.add(suggestion)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            
    # populate energy suggestion table
    for es in energy_suggestions:
        suggestion = EnergySuggestion(id=es['id'], content=es['content'])
        try:
            db.session.add(suggestion)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
    
    # form for selecting suggestion type
    form = SuggestionForm()
    if form.validate_on_submit():
        suggestion = form.suggestion.data
        
        # get relevant list of suggestions
        suggestions = []
        
        if form.suggestion.data == 'food_suggestion':
            for i in range(5):
                suggestions.append(FoodSuggestion.query.get(i).content)
            return render_template('suggestionResults.html', suggestions=suggestions)
        
        elif form.suggestion.data == 'travel_suggestion':
            for i in range(5):
                suggestions.append(TravelSuggestion.query.get(i).content)
            return render_template('suggestionResults.html', suggestions=suggestions)
        
        elif form.suggestion.data == 'energy_suggestion':
            for i in range(5):
                suggestions.append(EnergySuggestion.query.get(i).content)
            return render_template('suggestionResults.html', suggestions=suggestions)
    
    return render_template("suggestions.html", form=form)

@app.route("/community")
def community():
    return render_template("community.html")


# create post feature
@app.route("/create", methods=['GET', 'POST'])
@login_required
def createpost():
    form = PostForm()
    user = current_user
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=user)
        # clear form
        form.title.data = ''
        form.content.data = ''
        # Add post to databasse
        db.session.add(post)
        db.session.commit()
        
        # Return message
        flash('Blog Post added', 'success')
        return redirect(url_for('posts'))
    return render_template('create.html',
                           form=form,
                           text='Welcome to Climate Change project!',
                           title='Blog' , legend='New Post')

# displays post based on the id provided
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# displays all post in descending order
@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template('posts.html',
                           posts=posts,
                           text='Lets make some change')
 
# gives user the option to update there posts
@app.route("/post/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    # insures the user is fixing there post and not anyone else
    post = Posts.query.get_or_404(id)
    if post.author != current_user:
       abort(403)
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
    return render_template('create.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:id>/delete", methods=['POST'])
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    # insures the user is fixing there post and not anyone else
    if post.author != current_user:
        abort(403)
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
    db.create_all()
    app.run(debug=True, host="0.0.0.0")