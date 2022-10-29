#!/usr/bin/python3
"""
    Script for handling all the new default RESTFul API views actions
    for the city objects 
"""
from .common_functions import Classes
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage

State = Classes.get("State")
City = Classes.get("City")
cities = storage.all(City)

@app_views.route('/states/<state_id>/cities')
@app_views.route('/states/<state_id>/cities/')
def get_cities_list(state_id):
    """ Function for retreiving the lists of states """
    cities = storage.all(City)
    state = storage.get(State, state_id)
    if state:
        new_cities = [value.to_dict() for value in cities.values()
                if value.state_id == state.id]
        if new_cities:
            return jsonify(new_cities)
    return abort(404)

@app_views.route('/cities/<city_id>')
@app_views.route('/cities/<city_id>/')
def get_city_individual(city_id):
    """ Function for getting the individual city """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'])
@app_views.route('/cities/<city_id>/', methods=['DELETE'])
def delete_city_individual(city_id):
    """ Function for deleteing the individual part of the city """
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    return abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_new_city(state_id):
    """ Function that creates a new city using a state id """
    state = storage.get(State, state_id)
    if not(state):
        return abort(404)
    if isinstance(request.get_json(), dict):
        ring = request.get_json()
        if ring['name']:
            ring['state_id'] = state_id
            city = City(**ring)
            city.save()
            return jsonify(city.to_dict())
        return jsonify({"error": "Missing name"}), 400
    return jsonify({'error':"Not a JSON"}), 400

@app_views.route('cities/<city_id>', methods=['PUT'])
@app_views.route('cities/<city_id>/', methods=['PUT'])
def update_city_individual(city_id):
    """ Function for updating an already existing city id """
    city = storage.get(City, city_id)
    if city:
        if isinstance(request.get_json(), dict):
            for key, value in request.get_json().items():
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return abort(404)
