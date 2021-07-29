from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from turbo_flask import Turbo
from flask_migrate import Migrate
from blog import PostForm
from datetime import datetime
# import statements from prev projects, add/remove as needed
app = Flask(__name__)
turbo = Turbo(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SECRET_KEY'] = '525901fece4e62b2eb11fa3c1a302835'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    
# basic homepage, to be edited as needed with layout.html and main.css
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',
                           subtitle='Home Page',
                           text='Welcome to Climate Change project!')

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
    
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
