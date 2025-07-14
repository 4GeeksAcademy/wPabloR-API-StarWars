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
from models import db, User, Planet, Starship, Character, FavoritePlanet, FavoriteCharacter, FavoriteStarship
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

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = db.session.get(User, user_id)


    response_body = {
        "user": user_id,
        "planets_favs": [f.serialize() for f in user.favorite_planets], 
        "characters_favs": [f.serialize() for f in user.favorite_characters] , 
        "starships_favs" : [f.serialize() for f in user.favorite_starships]
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404

    new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)

    existing_fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_fav:
        return jsonify({"message": "This planet is already in favorites"}), 409

    db.session.add(new_favorite)
    db.session.commit()
    
    response_body = {
        "message": f"Planet {planet.name} added to user {user.username}'s favorites",
        "favorite": new_favorite.serialize() 
    }

    return jsonify(response_body), 201

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404

    new_favorite = FavoriteCharacter(user_id=user_id, character_id=character_id)

    existing_fav = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_fav:
        return jsonify({"message": "This character is already in favorites"}), 409


    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "message": f"Character {character.name} added to user {user.username}'s favorites",
        "favorite": new_favorite.serialize() 
    }

    return jsonify(response_body), 201

@app.route('/user/<int:user_id>/favorites/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    
    user = db.session.get(User, user_id)
    starship = db.session.get(Starship, starship_id)

    if not user or not starship:
        return jsonify({"error": "User or Starship not found"}), 404


    new_favorite = FavoriteStarship(user_id=user_id, starship_id=starship_id)

    existing_fav = FavoriteStarship.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if existing_fav:
        return jsonify({"message": "This starship is already in favorites"}), 409


    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "message": f"Starship {starship.name} added to user {user.username}'s favorites",
        "favorite": new_favorite.serialize() 
    }

    return jsonify(response_body), 201


@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404


    existing_fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if not existing_fav:
        return jsonify({"error": "Favorite not found"}), 404
    
    favorite_data = existing_fav.serialize()
   
    db.session.delete(existing_fav)
    db.session.commit()
    
    response_body = {
        "message": f"Planet {planet.name} removed from {user.username}'s favorites",
        "favorite": favorite_data
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404


    existing_fav = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()

    if not existing_fav:
        return jsonify({"error": "Favorite not found"}), 404
    
    favorite_data = existing_fav.serialize()
   
    db.session.delete(existing_fav)
    db.session.commit()

    response_body = {
        "message": f"Character {character.name} removed from {user.username}'s favorites",
        "favorite": favorite_data
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/starship/<int:starship_id>', methods=['DELETE'])
def remove_favorite_starship(user_id, starship_id):
    
    user = db.session.get(User, user_id)
    starship = db.session.get(Starship, starship_id)

    if not user or not starship:
        return jsonify({"error": "User or Starship not found"}), 404


    existing_fav = FavoriteStarship.query.filter_by(user_id=user_id, starship_id=starship_id).first()

    if not existing_fav:
        return jsonify({"error": "Favorite not found"}), 404
    
    favorite_data = existing_fav.serialize()
   
    db.session.delete(existing_fav)
    db.session.commit()
    
    response_body = {
        "message": f"Starship {starship.name} removed from {user.username}'s favorites",
        "favorite": favorite_data
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
