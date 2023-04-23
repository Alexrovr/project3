from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class IndexForm(FlaskForm):
    fbook = StringField('Название книги', validators=[DataRequired()])
    
    submit = SubmitField('Найти')