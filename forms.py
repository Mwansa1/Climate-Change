from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')
    
class SuggestionForm(FlaskForm):
    
    suggestion = SelectField(
        'Sustainable Suggestions',
        choices=[
            ('food_suggestion', 'Food'),
            ('travel_suggestion', 'Travel'),
            ('energy_suggestion', 'Energy')
        ]
    )
    
    submit = SubmitField('Submit')