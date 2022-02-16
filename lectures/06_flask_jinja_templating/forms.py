from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    query = StringField('Your Search term',
                validators=[DataRequired(),Length(min=3, max=15)])