from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class NameForm(FlaskForm):
    fname = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
        Regexp('^[A-Za-z ]*$', message="Only letters and spaces are allowed.")
    ])
    submit = SubmitField('Submit')
