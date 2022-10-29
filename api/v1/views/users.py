#!/usr/bin/python3
"""
    Script for a view for amenity objects that handles RESTFul API actions
"""

from .common_functions import Classes
from . import app_views
from models import storage
from flask import request, jsonify, abort

User = Classes.get('User')

@app_views.route('/users')
@app_views.route('/users/')
def list_users():
    """ Function for retriving all the list of all users """
    users = storage.all(User)
    if users:
        users = [value.to_dict() for value in users.values()]
    return jsonify(users)

@app_views.route('/users/<user_id>')
@app_views.route('/users/<user_id>/')
def get_user_individual(user_id):
    """ Function for reteriving a single user from the database"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
@app_views.route('/users/<user_id>/', methods=['DELETE'])
def delete_user_individual(user_id):
    """ Function for deleting an user instance """
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    return abort(404)

@app_views.route('/users', methods=['POST'])
@app_views.route('/users/', methods=['POST'])
def create_inidividual_user():
    """ Function to create an instance of an user """
    ring = request.get_json()
    if isinstance(ring, dict):
        if ring.get('email'):
            if ring.get('password'):
                user = User(**ring)
                user.save()
                return jsonify(user.to_dict()), 200
            return jsonify({"Error": "Missing password"}), 400
        return jsonify({"Error": "Missing name"}), 400
    return jsonify({'Error': "Not a JSON"}), 400

@app_views.route('/users/<user_id>', methods=['PUT'])
@app_views.route('/users/<user_id>/', methods=['PUT'])
def update_user_individual(user_id):
    """ Function for updating an individual user dataset """
    user = storage.get(User, user_id)
    if user:
        ring = request.get_json()
        if isinstance(ring, dict):
            for key, value in ring.items():
                setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200
        return jsonify({'Error':'Not a JSON'}), 400
    return abort(404)
