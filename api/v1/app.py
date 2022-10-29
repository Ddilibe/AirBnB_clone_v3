#!/usr/bin/python3
""" Script for launching the flask application """

from flask import Flask, jsonify

app = Flask(__name__)

from models import storage
from api.v1.views import app_views
app.register_blueprint(app_views)

@app.teardown_appcontext
def closeup(exception):
    """ Function for closing up some applications """
    storage.close()

@app.errorhandler(404)
def handles(exception):
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    import os
    host = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
