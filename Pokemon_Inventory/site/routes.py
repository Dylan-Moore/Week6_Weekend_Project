from unicodedata import name
from flask import Blueprint, render_template, redirect, json, request, url_for, jsonify
from flask_login import current_user
import requests as r2
import random
from Pokemon_Inventory.forms import PokemonTeamCreator
from Pokemon_Inventory.helpers import token_required
from Pokemon_Inventory.models import Pokemon, User, db
# from Pokemon_Inventory.models import db, Pokemon, pokemon_schema, pokemons_schema
site = Blueprint('site', __name__, template_folder= 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

# @site.route('/profile')
# def profile():
#     return render_template('profile.html')
@site.route('/Donate')
def Donate():
    return render_template('Donate.html')

@site.route('/profile', methods = ['GET', 'POST'])
def profile():
    form = PokemonTeamCreator()

    try:
        if request.method == "POST" and form.validate_on_submit():
            form_name = form.pokemon_name.data.lower()

            if form_name.lower() == "random":
                r = r2.get(f"https://pokeapi.co/api/v2/pokemon/{random.randint(1,905)}")
            else:
                r = r2.get(f"https://pokeapi.co/api/v2/pokemon/{form_name}")
            print(r)
            if r.status_code == 200:           
                data = r.json()
                name = data['name']
                game_id = data['id']
                type = data['types'][0]['type']['name']
                height = data['height']
                weight = data['weight']
                moveset = ", ".join([data['moves'][i]['move']['name'].title() for i in range(len(data['moves']))])
                poke = Pokemon(name=name, game_id = game_id, type = type, height=height, weight=weight, moveset=moveset, user_token=current_user.token)                
                db.session.add(poke)
                db.session.commit()               
                redirect(url_for('site.profile'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template("profile.html", form=form)







