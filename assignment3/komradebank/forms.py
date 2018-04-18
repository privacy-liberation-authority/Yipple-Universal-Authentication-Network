from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, FloatField
from wtforms import validators

from komradebank.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[validators.required()])
    password = PasswordField('password', validators=[validators.required()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # Check validation passes (both fields provided)
        if not check_validate:
            print(self.errors)
            return False

        # Check the user exists
        u = User.by_name(self.username.data)
        if not u:
            self.username.errors.append('Invalid username or password')
            return False

        # Check the password matches
        if not u.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[validators.required()])
    password = PasswordField('password', validators=[validators.required()])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # Check validation passes (both fields provided)
        if not check_validate:
            print(self.errors)
            return False

        # Check the user does not exist
        u = User.by_name(self.username.data)
        if u:
            self.username.errors.append('Username already in use')
            return False

        return True


class EditForm(FlaskForm):
    role = SelectField('role',  choices=[
        ('user', 'Customer'), ('staff', 'Employee'), ('admin', 'Administrator')], validators=[validators.optional()])
    username = StringField('username', validators=[validators.optional()])
    password = PasswordField('password', validators=[validators.optional()])
    fullname = StringField('fullname', validators=[validators.optional()])
    phone = StringField('phone', validators=[validators.optional()])
    email = StringField('email', validators=[validators.optional()])

    def validate(self):
        check_validate = super(EditForm, self).validate()

        if not check_validate:
            print(self.errors)
            return False

        return True


class XferForm(FlaskForm):
    src = StringField('From Account', validators=[validators.UUID()])
    dst = StringField('To Account', validators=[validators.UUID()])
    amount = FloatField('Amount', validators=[validators.required()])
    memo = StringField('Memo', validators=[validators.optional()])

    def validate(self):
        check_validate = super(XferForm, self).validate()

        if not check_validate:
            print(self.errors)
            return False

        return True