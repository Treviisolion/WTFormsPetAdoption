"""Pet Adoption Application"""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, Pet
from forms import NewPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = 'JohnathonAppleseed452'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
# debug = DebugToolbarExtension(app)

db.create_all()

@app.route('/')
def show_main_page():
    """Shows the main page which is a list of pets"""

    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def show_new_pet_form():
    """Shows the form for a new pet and handles adding a new pet"""

    form = NewPetForm()

    if form.validate_on_submit():
        new_pet = Pet(name=form.name.data.capitalize(), species=form.species.data.capitalize(), photo_url=form.photo_url.data, age=form.age.data, notes=form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Pet {new_pet.name} added!")
        return redirect('/')
    else:
        return render_template('new_pet.html', form=form)

@app.route('/<int:petid>', methods=['GET', 'POST'])
def show_pet(petid):
    """Shows details about the specified pet and allows editing those details"""

    pet = Pet.query.get_or_404(petid)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        if request.form['btn'] == 'Edit Info':
            pet.name = form.name.data.capitalize()
            pet.species = form.species.data.capitalize()
            pet.available = form.available.data
            pet.photo_url = form.photo_url.data
            pet.age = form.age.data
            pet.notes = form.notes.data
            db.session.commit()
            flash(f"{pet.name} data edited!")
            return redirect(f"/{petid}")
        elif request.form['btn'] == 'Delete':
            db.session.delete(pet)
            db.session.commit()
            flash(f"{pet.name} deleted")
            return redirect('/')
        else:
            flash(f"Weird submit was detected")
            return redirect('/')
    else:
        return render_template('pet.html', pet=pet, form=form)
