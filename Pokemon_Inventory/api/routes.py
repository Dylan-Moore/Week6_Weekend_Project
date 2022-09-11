from flask import Blueprint, request, jsonify
from Pokemon_Inventory.helpers import token_required
from Pokemon_Inventory.models import db, Pokemon, pokemon_schema, pokemons_schema

import urllib.request, json

api = Blueprint('api', __name__, url_prefix= '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{'name':'pokemon'}
#Create
@api.route('/pokemon', methods = ['POST'])
@token_required
def create_pokemon(current_user_token):
    name = request.json['name']
    description = request.json['description']
    type = request.json['type']
    nature = request.json['nature']
    height = request.json['height']
    weight = request.json['weight']
    moveset = request.json['moveset']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    pokemon = Pokemon(name, description, type, nature, height, weight, moveset, user_token=user_token)

    db.session.add(pokemon)
    db.session.commit()

    response = pokemon_schema.dump(pokemon)

    return jsonify(response)

#retrieve single
@api.route('/pokemons/<id>', methods = ['GET'])
@token_required
def get_pokemon(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        pokemon = Pokemon.query.get(id)
        response = pokemon_schema.dump(pokemon)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

#retrieve all
@api.route('/pokemons', methods = ['GET'])
@token_required
def get_pokemons(current_user_token):
    owner = current_user_token.token
    pokemons = Pokemon.query.filter_by(user_token = owner).all()
    response = pokemons_schema.dump(pokemons)
    return jsonify(response)

#Update
@api.route('/drones/<id>', methods = ['POST', 'PUT'])
@token_required
def update_pokemon(current_user_token, id):
    pokemon = Pokemon.query.get(id)
    pokemon.name = request.json['name']
    pokemon.description = request.json['description']
    pokemon.type = request.json['type']
    pokemon.nature = request.json['nature']
    pokemon.height = request.json['height']
    pokemon.weight = request.json['weight']
    pokemon.moveset = request.json['moveset']
    pokemon.user_token = current_user_token.token

    db.session.commit()
    response = pokemon_schema.dump(pokemon)
    return jsonify(response)

#Delete
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_pokemon(current_user_token, id):
    pokemon = Pokemon.query.get(id)
    db.session.delete(pokemon)
    db.session.commit()
    response = pokemon_schema.dump(pokemon)
    return jsonify(response)
