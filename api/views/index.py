#!/usr/bin/python3
"""
API index views module
"""
from api.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """
    Returns json response of api status

    Returns:
        JSON: json object
    """
    status = {
        "status": "OK"
    }
    return jsonify(status)
