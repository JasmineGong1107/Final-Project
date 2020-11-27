from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

"""Create how the layout looks like when a user posts a note and validate the input is postable"""


class PostForm(FlaskForm):
    title = StringField("Titile", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")