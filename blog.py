from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    IntegerField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    ValidationError
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField(
        'Post',
        validators=[
            DataRequired()],
        widget=TextArea())
    submit = SubmitField('Post')


class UploadForm(FlaskForm):
    image = FileField('Upload Image', validators=[
                      DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'],
                                                  'Images only!')])
    caption = StringField('caption')
    submit = SubmitField('Upload to Feed')
