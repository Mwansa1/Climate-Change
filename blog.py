from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    ValidationError
)
from wtforms.widgets import TextArea

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()] )
    content = StringField('Post', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Post')
