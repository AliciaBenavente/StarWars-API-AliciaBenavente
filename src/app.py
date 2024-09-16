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
from models import db, Users, Characters, Planets, Favorite_Character, Favorite_Planet
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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


# USERS
@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.order_by(Users.name).all()
    result = list(map(lambda users: users.serialize(), users))

    return jsonify(result), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify("ERROR: This is not the User you are looking for"), 404
    else:
        return jsonify(user.serialize()), 200

#  CHARACTERS
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.order_by(Characters.name).all()
    result = list(map(lambda characters: characters.serialize(), characters))

    return jsonify(result), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(id=character_id).first()
    if character is None:
        return jsonify("ERROR: This is not the Character you are looking for"), 404
    else:
        return jsonify(character.serialize()), 200

# PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.order_by(Planets.name).all()
    result = list(map(lambda planets: planets.serialize(), planets))

    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify("ERROR: This is not the Planet you are looking for"), 404
    else:
        return jsonify(planet.serialize()), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify("ERROR: This is not the User you are looking for"), 404
    
    favorite_characters = Favorite_Character.query.filter_by(user_id=user_id).all()
    favorite_planets = Favorite_Planet.query.filter_by(user_id=user_id).all()

    favorite_characters_data = []
    for favorite_character in favorite_characters:
        character = Characters.query.filter_by(id=favorite_character.character_id).first()
        favorite_characters_data.append(character.serialize())

    favorite_planets_data = []
    for favorite_planet in favorite_planets:
        planet = Planets.query.filter_by(id=favorite_planet.planet_id).first()
        favorite_planets_data.append(planet.serialize())

    return jsonify({
        "characters": favorite_characters_data,
        "planets": favorite_planets_data,
    }), 200


@app.route('/favorite/character', methods=['POST'])
def add_favorite_character():

    body = request.get_json()

    user = Users.query.get(body["user_id"])
    if user is None:
        return jsonify("ERROR: user_id does not exist"), 400

    character = Characters.query.get(body["characters_id"])
    if character is None:
        return jsonify("ERROR: character_id does not exist"), 400

    favorite_exist = Favorite_Character.query.filter_by(user_id=body["user_id"], characters_id=body["characters_id"]).first()
    if favorite_exist:
        return jsonify("ERROR: this character is already a favorite"), 400

    new_favorite = Favorite_Character (
        user_id = body["user_id"],
        characters_id = body ["characters_id"],
        user_characteristics = f'{user.name} likes {character.name}'
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200

@app.route('/favorite/planet', methods=['POST'])
def add_favorite_planet():

    body = request.get_json()

    user = Users.query.get(body["user_id"])
    if user is None:
        return jsonify("ERROR: user_id does not exist"), 400

    planet = Planets.query.get(body["planets_id"])
    if planet is None:
        return jsonify("ERROR: planet_id does not exist"), 400

    favorite_exist = Favorite_Planet.query.filter_by(user_id=body["user_id"], planets_id=body["planets_id"]).first()
    if favorite_exist:
        return jsonify("ERROR: this planet is already a favorite"), 400

    new_favorite = Favorite_Planet (
        user_id = body["user_id"],
        planets_id = body ["planets_id"],
        user_characteristics = f'{user.name} likes {planet.name}'
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
