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
from models import db, User, Planet, Starship, Character
from sqlalchemy import select
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
def get_users():

    all_users = User.query.all()
    results = list(map(lambda user: user.serialize(), all_users))

    response_body = {
        "users": results
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planets():

    all_planets = Planet.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))

    response_body = {
        "planets": results
    }

    return jsonify(response_body), 200

@app.route('/starship', methods=['GET'])
def get_starships():

    all_starships = Starship.query.all()
    results = list(map(lambda ship: ship.serialize(), all_starships))

    response_body = {
        "starships": results
    }

    return jsonify(response_body), 200

@app.route('/character', methods=['GET'])
def get_characters():

    all_characters = Character.query.all()
    results = list(map(lambda ship: ship.serialize(), all_characters))

    response_body = {
        "characters": results
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = db.session.get(User, user_id)

    response_body = {
        "user": user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = db.session.get(Planet, planet_id)

    response_body = {
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):

    starship = db.session.get(Starship, starship_id)

    response_body = {
        "starship": starship.serialize()
    }

    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = db.session.get(Character, character_id)
   

    response_body = {
        "characters": character.serialize()
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
