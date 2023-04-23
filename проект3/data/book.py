from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class LBookForm(FlaskForm):
    text = StringField('Напишите что-нибудь', validators=[DataRequired()])
    
    submit = SubmitField('Submit')