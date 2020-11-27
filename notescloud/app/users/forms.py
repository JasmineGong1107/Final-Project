from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

"""
Create RegistrationFrom class which is inheritaed from FlaskForm for automatic converstion for html form

"""


class RegistrationForm(FlaskForm):
    """Form Fields Creation: username, email, password, confirm_password"""

    """make sure this is not empty + put limitation on username length"""
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    """make sure this match a email address format"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    """make sure has something entered, not to be left empty"""
    password = PasswordField("Password", validators=[DataRequired()])
    """make sure this field is not left blank + match the previous set password"""
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    """submit button"""
    submit = SubmitField("Sign up")

    """Validate this username has not been documented in the database before"""
    """how to react if the username is taken"""

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is not longer available. Please use another one."
            )

    """how to react if the email is taken"""

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken. Please use another one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Login")


"""Update account info: username, email and profile pic"""


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )

    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )

    submit = SubmitField("Update")

    """make sure the updated info is not going to repeat any existing ones"""

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "This username is not longer available. Please use another one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is taken. Please use another one.")


"""Field to enter email to receive password reset link"""


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    """make sure the email is registered in the system with an account"""

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No account is created with this email address.")


"""Fields show up when a new password will be entered"""


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password.")
