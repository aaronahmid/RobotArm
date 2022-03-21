"""
States API modules
"""
import states
import json
from handlers.state_handler import StateHandler
from flask import (
    jsonify,
    make_response,
    request
)
from armservice.views import api_views

@api_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieves states from filestorage
    """
    states = StateHandler().all_states()
    return make_response(jsonify(states), 200)


@api_views.route('/states/create/', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new state object from a yaml file
    """
    if request.get_json():
        kwargs = request.get_json()
    else:
        return "Not a JSON", 400

    if kwargs:
        if 'file' not in kwargs.keys():
            return 'Missing file', 400
    try:
        state = StateHandler().createState(**kwargs)
    except TypeError:
        return "Not a JSON", 400
    
    return make_response(jsonify(state.to_dict()), 201)

@api_views.route('/states/<state_id>/activate/', methods=['PUT'], strict_slashes=False)
def activate_state(state_id):
    if state_id is None:
        return "Missing state_id", 400
    
    state = StateHandler().activate(state_id)
    return make_response(str(state), 200)
