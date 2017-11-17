from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class Reg2Form(Form):
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])

    # Maybe change marital_status, citizenship, and education to dropdown boxes
    marital_status = TextField('Marital Status', validators=[DataRequired()])
    citizenship = TextField('Citizenship', validators=[DataRequired()])
    education = TextField('Education', validators=[DataRequired()])

    occupation = TextField('Occupation', validators=[DataRequired()])

    # Dropdown box
    religion = TextField('Religion', validators=[DataRequired()])
    ethnic_origin = TextField('Ethnic Origin', validators=[DataRequired()])

    address1 = TextField('Address Line 1', validators=[DataRequired()])
    address2 = TextField('Address Line 2', validators=[DataRequired()])
    city = TextField('City', validators=[DataRequired()])
    region = TextField('State/Province/Region', validators=[DataRequired()])
    postal_code = IntegerField('Zip/Postal Code', validators=[DataRequired()])

    # Dropdown box
    country = TextField('Country', validators=[DataRequired()])
