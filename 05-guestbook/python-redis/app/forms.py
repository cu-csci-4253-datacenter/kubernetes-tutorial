from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class BlogForm(FlaskForm):
    msg = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
