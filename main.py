from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from turbo_flask import Turbo
from forms import RegistrationForm
from sqlalchemy import exc, text
# import statements from prev projects, add/remove as needed

app = Flask(__name__)
turbo = Turbo(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '525901fece4e62b2eb11fa3c1a302835'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    """An admin user capable of viewing reports.
    :param str email: email address of user
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user'

    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
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


# basic homepage, to be edited as needed with layout.html and main.css
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',
                           subtitle='Home Page',
                           text='Welcome to Climate Change project!')
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
            return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)

# @app.route("/more")
# def second_page():
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
