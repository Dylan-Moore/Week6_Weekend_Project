from email.mime import image
from tokenize import Name
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from PIL import Image

from flask_migrate import Migrate

import uuid

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False, default = '')
    password = db.Column(db.String(150), nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    pokemon = db.relationship('Pokemon', backref = 'owner', lazy = True)

    def __init__(self, email, username = '', first_name = '', last_name = '', id='', password='', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    def set_id(self):
        return str(uuid.uuid4())
    def set_password(self, password):
        self.pw_hash=generate_password_hash(password)
        return self.pw_hash
    def __repr__(self):
        return f"User {self.email} has been added to the database"


class Pokemon(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    game_id = db.Column(db.Integer)
    # description = db.Column(db.String(200), nullable = True)
    type = db.Column(db.String(100))
    # nature = db.Column(db.String(100))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    moveset = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, game_id, type, height, weight, moveset, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.game_id = game_id
        # self.description = description
        self.type = type
        # self.nature = nature
        self.height = height
        self.weight = weight
        self.moveset = moveset
        self.user_token = user_token
    def __repr__(self):
            #return f"The following Pokemon has been added: {self.name} {self.type}"
            return f"[{self.name}, {self.type}, {self.game_id}]"
        

    def set_id(self):
        return secrets.token_urlsafe()

class PokemonSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'game_id', 'type', 'height', 'weight', 'moveset']

pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)