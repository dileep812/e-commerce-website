from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length,EqualTo,email,DataRequired
from market.models import User
class RegisterForm(FlaskForm):
        username = StringField(label='User Name:',validators=[length(min=2,max=30),DataRequired()])
        email_address = StringField(label='Email Address:',validators=[email(),DataRequired()])
        password1 = PasswordField(label='Password:',validators=[length(min=6),DataRequired()])
        password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
        submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
        username=StringField(label='User Name',validators=[DataRequired(),length(min=2,max=30)])
        password=PasswordField(label='Password',validators=[DataRequired(),length(min=6)])
        submit=SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
        submit=SubmitField(label='Purchase item!')

class SellItemForm(FlaskForm):
        submit=SubmitField(label='sell this item')