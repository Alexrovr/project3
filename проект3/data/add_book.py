from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Submit')
