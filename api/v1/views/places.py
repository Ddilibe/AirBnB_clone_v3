#!/usr/bin/python3
"""Script that creates a new view for RESTFul Api actions for place objects"""
from models import storage
from flask import abort, request, jsonify
from .common_functions import Classes
from . import app_views

Place = Classes.get("Place")
City = Classes.get("City")
User = Classes.get("User")

@app_views.route('/cities/<city_id>/places')
def list_all_places(city_id):
    """ Function that lists all the places in a city """
    city = storage.get(City, city_id)
    if city:
        place = storage.all(Place)
        if place:
            places = [gone.to_dict() for gone in place.values() 
                    if gone.city_id == city_id]
            return jsonify(places)
    return abort(404)

@app_views.route('/places/<place_id>')
def get_place_inidividual(place_id):
    """ Function for retrieving an individual instance of a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    return abort(404)

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_individual(place_id):
    """ Function to delete an instance of a place object"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    return abort(404)

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place_individual(city_id):
    """ function for creating a new place instance """
    city = storage.get(City, city_id)
    ring = request.get_json()
    if city:
        if isinstance(ring, dict):
            if ring.get('user_id'):
                user = storage.get(User, ring.get('user_id'))
                if user:
                    if ring.get('name'):
                        ring['city_id'] = city_id
                        place = Place(**ring)
                        place.save()
                        return jsonify(place.to_dict())
                    return jsonify({"Error": "Missing name"}), 400
                return abort(404)
            return jsonify({"Error": "Missing user_id"}), 400
        return jsonify({"Error": "Not a JSON"}), 400
    return abort(404)

@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place_individual(place_id):
    """ Function for updating an place instance """
    place = storage.get(Place, place_id)
    if place:
        ring = request.get_json()
        if isinstance(ring, dict):
            for key, value in ring.items():
                setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200
        return jsonify({"Error": "Not a JSON"}), 400
    return abort(404)
