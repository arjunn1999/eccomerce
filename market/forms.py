from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from market.models import User
class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username aldready exists please use differnet username')
    def validate_email(self,email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email aldready exists')
    username=StringField(label="User Name",validators=[Length(min=3,max=30),DataRequired()])
    email = StringField(label="Email",validators=[Email(),DataRequired()])
    password=PasswordField(label="Password",validators=[Length(min=4),DataRequired()])
    confirm_password=PasswordField(label="Confirm Password",validators=[EqualTo('password'),DataRequired()])
    name = StringField(label="Name",validators=[DataRequired()])
    submit = SubmitField(label='CREATE ACCOUNT')


class LoginForm(FlaskForm):
    email = StringField(label="Email",validators=[Email(),DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField(label='Login')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Yes")


class SellItemForm(FlaskForm):
    submit = SubmitField(label="Yes")