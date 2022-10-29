#!/usr/bin/python3
""" Script for Revies object that handles all default RESTFul API actions """

from models import storage
from . import app_views
from .common_functions import Classes
from flask import request, jsonify, abort

Place = Classes.get("Place")
Review = Classes.get("Review")
User = Classes.get("User")

@app_views.route('/places/<place_id>/reviews')
def get_all_reviews(place_id):
    """ Functions for retrieving all Review objects of a place """
    place = storage.get(Place, place_id)
    if place:
        reviews = [ace.to_dict() for ace in storage.all(Review).values() 
                if ace.place_id == place_id]
        return jsonify(reviews)
    return abort(404)

@app_views.route('/reviews/<review_id>')
def retrieve_review_individual(review_id):
    """ Function for retrieving an individual instance of a review object """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    return abort(404)

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_individual(review_id):
    """ Function for retrieving an individual instance of a review object """
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify([]), 200
    return abort(404)

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review_instance(place_id):
    """
        Function for creating a review instance from a place instance variable
    """
    ring = request.get_json()
    place = storage.get(Place, place_id)
    if place:
        if isinstance(ring, dict):
            if ring.get('user_id'):
                user = storage.get(User, ring.get('user_id'))
                if user:
                    if ring.get('text'):
                        ring['place_id'] = place_id
                        review = Review(**ring)
                        review.save()
                        return jsonify(review.to_dict())
                    return jsonify({'Error': "Missing text"}), 400
                return abort(404)
            return jsonify({"Error": "Missing user_id"}), 400
        return jsonify({"Error": "Not  a JSON"}), 400
    return abort(404)

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_reviews_individual(review_id):
    """ Function for update data in the review instance """
    review = storage.get(Review, review_id)
    ring = request.get_json()
    if review:
        if isinstance(ring, dict):
            for key, value in ring.items():
                setattr(review, key, value)
            review.save()
            return jsonify(review.to_dic()), 200
        return jsonify({"Error": "Not a JSON"}), 400
    return abort(404)
