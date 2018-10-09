"""Cupcake API"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake
from flask_wtf import FlaskForm
from flask_debugtoolbar import DebugToolbarExtension
from secret import SECRET_KEY

# from cupcakefunctions import

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

app.config['SECRET_KEY'] = SECRET_KEY
debug = DebugToolbarExtension(app)

# HOME PAGE


@app.route('/')
def home():
    """Renders home page with list of cupcakes
       and form to add a new cupcake"""

    return render_template('index.html')


@app.route('/cupcakes')
def get_cupcakes():
    """Return JSON that represents an array of dictionaries

       Each dictionary represents a cupcake
    """

    if request.args.get('search'):
        cupcakeInstances = Cupcake.query.filter(
            Cupcake.flavor.like(f"%{request.args.get('search')}%")).all()
        cupcakeInstances.extend(Cupcake.query.filter(
            Cupcake.size.like(f"%{request.args.get('search')}%")).all())
    else:
        cupcakeInstances = Cupcake.query.all()

    cupcakes = []

    for cupcake in cupcakeInstances:
        cupcakes.append({
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        })

    return jsonify(response=cupcakes)


@app.route('/cupcakes', methods=["POST"])
def add_cupcake():
    """Allow a user to create a cupcake by providing data in JSON

       Return JSON that contains the newly created values including the id
    """

    new_cupcake_request = request.get_json()

    new_cupcake_request['flavor'] = new_cupcake_request['flavor'].lower()
    new_cupcake_request['size'] = new_cupcake_request['size'].lower()
    new_cupcake = Cupcake(**new_cupcake_request)

    db.session.add(new_cupcake)
    db.session.commit()

    # Serialize new data row as dict to JSON
    serialized_cupcake = {
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image
    }

    return jsonify(response=serialized_cupcake)


@app.route('/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Allow a user to update a cupcake by providing data in JSON

       Return JSON that contains the data of the updated cupcake
    """

    cupcake_to_update = Cupcake.query.get_or_404(cupcake_id)
    update_cupcake_request = request.get_json()

    # reasssign cupcake instance fields
    cupcake_to_update.flavor = update_cupcake_request.get(
        "flavor", cupcake_to_update.flavor)
    cupcake_to_update.size = update_cupcake_request.get(
        "size", cupcake_to_update.size)
    cupcake_to_update.rating = update_cupcake_request.get(
        "rating", cupcake_to_update.rating)
    cupcake_to_update.image = update_cupcake_request.get(
        "image", cupcake_to_update.image)

    db.session.commit()

    # Serialize new data row as dict to JSON
    serialized_cupcake = {
        "id": cupcake_to_update.id,
        "flavor": cupcake_to_update.flavor,
        "size": cupcake_to_update.size,
        "rating": cupcake_to_update.rating,
        "image": cupcake_to_update.image
    }

    return jsonify(response=serialized_cupcake)


@app.route('/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a cupcake based on id supplied by user"""

    cupcake_to_delete = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake_to_delete)
    db.session.commit()

    return jsonify(response={
        "message": "deleted"
    })


@app.route('/cupcakes/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    """Shows cupcake details and a form to delete it"""

    cupcake_to_edit = Cupcake.query.get_or_404(cupcake_id)

    return render_template('cupcake_details.html', cupcake=cupcake_to_edit)
