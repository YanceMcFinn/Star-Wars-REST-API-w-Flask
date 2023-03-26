from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<Person %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period= db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity
            }

class FavoritePerson(db.model):
    id = db.Column(db.Integer, primary_key=true)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    person_id = db.Column(db.Integer, ForeignKey('Person.id'))
    user = db.relationship('User')
    person = db.relationship('Person')

    def __repr__(self):
        return '<Favorite_Person %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id
            }

class FavoritePlanet(db.model):
    id = db.Column(db.Integer, primary_key=true)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, ForeignKey('Planet.id'))
    user = db.relationship('User')
    planet = db.relationship('Planet')

    def __repr__(self):
        return '<Favorite_Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
            }

