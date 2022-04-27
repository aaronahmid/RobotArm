#!/usr/bin/python3
"""
API index views module
"""
from robotarm.armservice.views import api_views
from flask import jsonify


@api_views.route('/status')
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
