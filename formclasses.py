from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, InputRequired, AnyOf, URL, NumberRange


class AddPetForm(FlaskForm):
    """Form class for adding a pet"""

    name = StringField('Pet Name')
    # make this a dropdown (species)
    species = StringField('Pet Species', validators=[
                          InputRequired(), AnyOf(['dog', 'cat', 'porcupine', 'pickle'])])
    photo_url = StringField('Pet Photo Url', validators=[
                            InputRequired(), URL()])
    age = IntegerField('Pet Age', validators=[InputRequired(
    ), NumberRange(0, 30, "Age must be between 0 and 30")])
    notes = TextAreaField('Notes')


class EditPetForm(FlaskForm):
    """"Form class for editing pets"""

    photo_url = StringField('Pet Photo Url', validators=[
                            InputRequired(), URL()])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')
