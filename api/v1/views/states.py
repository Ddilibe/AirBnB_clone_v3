#!/usr/bin/python3
"""
    Script for handling all the new default RESTFul API views actions
    for the state objects 
"""
from .common_functions import Classes
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage

State = Classes.get("State")
states = storage.all(State)

@app_views.route('/states')
@app_views.route('/states/')
def get_state_list():
    """ Function for retreiving the lists of states """
    new_states = [value.to_dict() for value in states.values()]
    return jsonify(new_states)

@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states/<state_id>/', methods=['GET'])
def get_states_individual(state_id):
    """ Function to for querying the data base to get the individual state """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    return abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
@app_views.route('/states/<state_id>/', methods=['DELETE'])
def delete_states_indiviual(state_id):
    """ Function to query the database to delete an individual state """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    return abort(404)

@app_views.route('/states', methods=['POST'])
@app_views.route('/states/', methods=['POST'])
def create_state():
    """ Function to create a new state instance """
    if isinstance(request.get_json(), dict):
        if request.get_json()['name']:
            state = State(request.get_json())
            state.save()
            return jsonify(state.to_dict())
        return jsonify({"error": "Missing name"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/states/<state_id>', methods=['PUT'])
@app_views.route('/states/<state_id>/', methods=['PUT'])
def update_state_individual(state_id):
    """ Function for updating the properties of a state individual """
    state = storage.get(State, state_id)
    if state:
        if isinstance(request.get_json(), dict):
            for key, value in request.get_json().items():
                setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict())
        return jsonify({"error": "Not a JSON"}), 400
    return abort(404)
