#!/usr/bin/python3
"""
    Script for a view for amenity objects that handles RESTFul API actions
"""

from .common_functions import Classes
from . import app_views
from models import storage
from flask import request, jsonify, abort

Amenity = Classes.get('Amenity')

@app_views.route('/amenities')
@app_views.route('/amenities/')
def list_amenities():
    """ Function for retriving all the list of all Amenity """
    amenities = storage.all(Amenity)
    if amenities:
        amenities = [value.to_dict() for value in amenities.values()]
    return jsonify(amenities)
    
@app_views.route('/amenities/<amenity_id>')
@app_views.route('/amenities/<amenity_id>/')
def get_amenity_individual(amenity_id):
    """ Function for reteriving a single amenity from the database"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
@app_views.route('/amenities/<amenity_id>/', methods=['DELETE'])
def delete_amenity_individual(amenity_id):
    """ Function for deleting an amenity instance """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    return abort(404)

@app_views.route('/amenities', methods=['POST'])
@app_views.route('/amenities/', methods=['POST'])
def create_inidividual_amenity():
    """ Function to create an instance of an amenity """
    ring = request.get_json()
    if isinstance(ring, dict):
        if ring.get('name'):
            amenity = Amenity(**request.get_json())
            amenity.save()
#            return jsonify(amenity.to_dict()), 200
            return jsonify(request.get_json())
        return jsonify({"Error": "Missing name"}), 400
    return jsonify({'Error': "Not a JSON"}), 400

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
@app_views.route('/amenities/<amenity_id>/', methods=['PUT'])
def update_amenity_individual(amenity_id):
    """ Function for updating an individual amenity dataset """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        ring = request.get_json()
        if isinstance(ring, dict):
            for key, value in ring.items():
                setattr(amenity, key, value)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        return jsonify({'Error':'Not a JSON'}), 400
    return abort(404)
