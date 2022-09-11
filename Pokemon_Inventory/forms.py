from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email
from flask import request, json
import random

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit_button = SubmitField()

class PokemonTeamCreator(FlaskForm):
    pokemon_name = StringField('name', validators= [InputRequired()])
    submit_button = SubmitField()