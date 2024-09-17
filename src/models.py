from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    region = db.Column(db.String(120), nullable=True)
    sector = db.Column(db.String(120), nullable=True)
    system = db.Column(db.String(120), nullable=True)
    inhabitants = db.Column(db.Integer, nullable=True)
    capital_city = db.Column(db.String(120), nullable=True)
    coordinates = db.Column(db.Integer, nullable=True)
    db.relationship("Favorite_Planet", backref="planets", lazy=True)
    db.relationship("Characters", backref="planets", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region,
            "sector": self.sector,
            "system": self.system,
            "inhabitants": self.inhabitants,
            "capital_city": self.capital_city,
            "coordinates": self.coordinates,
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    species = db.Column(db.String(120), nullable=True)
    homeplanet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    homeplanet = db.relationship(Planets, backref='characters', lazy=True)
    gender = db.Column(db.String(120), nullable=True)
    db.relationship("Favorite_Character", backref="characters", lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "homeplanet_name": self.homeplanet.name if self.homeplanet else None,
            "gender": self.gender,
        }

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_character = db.relationship("Favorite_Character", backref="users", lazy=True)
    favorite_planet = db.relationship("Favorite_Planet", backref="users", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user_characteristics = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return '<Favorite_Character user_id=%r, characters_id=%r>' % (self.user_id, self.characters_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            "user_characteristics" : self.user_characteristics,           
        }

class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user_characteristics = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return '<Favorite_Planet user_id=%r, planets_id=%r>' % (self.user_id, self.planets_id)

    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "user_characteristics" : self.user_characteristics,           
        }