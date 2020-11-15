"""Forms for Pet adoption"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL, Optional, ValidationError
from wtforms.widgets import html_params

VALID_SPECIES = ['Cat', 'Dog', 'Porcupine']
SPECIES_WARNING = ''.join(f"{species}, " if species is not VALID_SPECIES[-1] else f"or {species}." for species in VALID_SPECIES)
MIN_AGE = 0
MAX_AGE = 30

def validate_species(form, species):
    """Makes certain the species is one of the selected few"""
    if species.data.capitalize() not in VALID_SPECIES:
        raise ValidationError(f"Sorry, but the species must be {SPECIES_WARNING}")

def validate_age(form, age):
    """Makes certain the age is between the minimum and maximum age"""
    if age.data is not None:
        if not (MIN_AGE <= age.data <= MAX_AGE):
            raise ValidationError(f"Sorry but the pet must be between {MIN_AGE} and {MAX_AGE} years old")

class NewPetForm(FlaskForm):
    """Form for adding new pets"""

    name = StringField("Pet name", validators=[DataRequired()])
    species = StringField("Pet species", validators=[DataRequired(), validate_species])
    photo_url = StringField("Image of pet", validators=[URL(), Optional()])
    age = IntegerField("Age in years", validators=[Optional(), validate_age])
    notes = TextAreaField("Notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form for editing exiting pets"""

    name = StringField("Pet name", validators=[Optional()])
    species = StringField("Pet Species", validators=[Optional(), validate_species])
    available = BooleanField("Available", validators=[Optional()])
    photo_url = StringField("Image of pet", validators=[Optional()])
    age = IntegerField("Age in years", validators=[Optional(), validate_age])
    notes = TextAreaField("Notes", validators=[Optional()])