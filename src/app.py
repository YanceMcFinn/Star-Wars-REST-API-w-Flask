"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, FavoritePerson, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = Person.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return (jsonify(all_people), 200)

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return json_text

@app.route('/people/<int:person_id>', methods=['GET'])
def get_single_person(person_id):
    person = Person.query.get(person_id)
    return jsonify(person.serialize()), 200

@app.route('/planets/<int:position>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return (jsonify(all_users), 200)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return (jsonify(user.serialize()), 200)

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favPeople = FavoritePerson.query.filter_by(user_id=user_id)
    favPeople = list(lambda x: x.serialize(), favPeople)
    favPlanets = FavoritePlanet.query.filter_by(user_id=user_id)
    favPlanets = list(lambda x: x.serialize(), favPlanets)
    favs = favPeople.append(favPlanets)

    return (jsonify(favs), 200)

@app.route('/users/<int:user_id>/favorites/people/<int:person_id>', methods=['POST'])
def add_favorite_person(user_id, person_id):
    user = User.query.filter_by(user_id=user_id)
    person = Person.filter_by(person_id=person_id)

    fav = person(user_id=user.id, person_id=person.id)
    db.session.add(fav)
    db.session.commit()



    return (jsonify(fav.serialize()), 200)

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_person(user_id, planet_id):
    user = User.query.filter_by(user_id=user_id)
    planet = Planet.filter_by(planet=planet_id)

    fav = planet(user_id=user.id, planet_id=planet.id)
    db.session.add(fav)
    db.session.commit()



    return (jsonify(fav.serialize()), 200)

@app.route('/users/<int:user_id>/favorites/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(user_id, planet_id):
    user = User.query.filter_by(user_id=user_id)
    person = Person.filter_by(person_id=person_id)

    fav = FavoritePerson.query.filter_by(user_id = user.id, person_id=person.id)
    db.session.delete(fav)
    db.session.commit()



    return (jsonify(fav.serialize()), 200)

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.filter_by(user_id=user_id)
    planet = Planet.query.filter_by(planet_id=planet_id)

    fav = FavoritePlanet.query.filter_by(user_id = user.id, planet_id=planet.id)
    db.session.delete(fav)
    db.session.commit()



    return (jsonify(fav.serialize()), 200)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
