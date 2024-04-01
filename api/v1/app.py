#!/usr/bin/python3
'''
    This module contains variables and methods used to connect to API
'''
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', '5000'))
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.teardown_appcontext
def teardown_app(code):
    '''
        Handles teardown
    '''
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    '''
        Returns a JSON-formatted error response
    '''
    return jsonify({"error": "Not found"}), 404

# Define a route for the status endpoint
@app.route('/status')
def status():
    # Define the status information
    status_info = {
        "status": "ok",
        "api_version": "1.0",
        "uptime": str(datetime.datetime.now() - app.start_time)
    }
    # Return the status response
    return jsonify(status_info)

if __name__ == "__main__":
    app.start_time = datetime.datetime.now()  # Store the start time of the application
    app.run(host=host, port=port, threaded=True)
