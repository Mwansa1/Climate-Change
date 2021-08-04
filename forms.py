from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Enter username..."})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Enter email..."})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Enter password..."})
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')], render_kw={
            "placeholder": "Re-enter password..."})
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', render_kw={
            "placeholder": "Enter username..."})
    password = PasswordField(
        'Password', render_kw={
            "placeholder": "Enter password..."})
    submit = SubmitField('Login')


class SuggestionForm(FlaskForm):
    suggestion = SelectField(
        'Sustainable Suggestions',
        choices=[
            ('food_suggestion', 'Food'),
            ('travel_suggestion', 'Travel'),
            ('energy_suggestion', 'Energy')
        ])
    submit = SubmitField('Submit')
