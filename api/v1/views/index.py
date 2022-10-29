#!/usr/bin/python3
""" Script containing the content to the blueprint app_view """

from flask import jsonify
from api.v1.views import app_views
from .common_functions import Classes

@app_views.route('/status')
def status():
    """ Route used to define the status of the code """
    new_dict = {}
    new_dict["status"] = "OK"
    return jsonify(new_dict)

@app_views.route('/stats')
def stats():
    """ Route that counts the number of variables on the database """
    from models import storage
    new_dict = {}
    for keys, values in Classes.items():
        new_dict[keys.lower()] = storage.count(values)
    return jsonify(new_dict)

