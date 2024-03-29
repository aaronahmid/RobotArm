#!/usr/bin/python3
"""
States API modules
"""
from robotarm import states
import json
from robotarm.handlers.state_handler import StateHandler
from flask import (
    jsonify,
    make_response,
    request
)
from robotarm.armservice.views import api_views
import asyncio

# TODO: deactivate state api
# TODO: delete state api
# TODO: list states api


@api_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieves states from filestorage
    """
    states = StateHandler().all_states()
    return make_response(jsonify(states), 200)


@api_views.route('/states/create/', methods=['POST'], strict_slashes=False)
async def create_state():
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
    except TypeError as error:
        return make_response(jsonify(error))
        # return "Not a JSON", 400

    return make_response(jsonify(state.to_dict()), 201)


@api_views.route('/states/<state_id>/activate/',
                 methods=['PUT'], strict_slashes=False)
def activate_state(state_id):
    """
    activates a state
    """
    if state_id is None:
        return "Missing state_id", 400

    state = StateHandler().activate(state_id)
    return make_response(str(state), 200)

@api_views.route('/states/get_working_dir/',
                 methods=['GET'], strict_slashes=False)
def working_dir():
    """
    returns test folder
    """
    state = StateHandler().getCurrentState()
    return make_response(jsonify({
        'working_dir': state.working_dir
    }), 200)


@api_views.route('/states/get_test_folder/',
                 methods=['GET'], strict_slashes=False)
def get_test_folder():
    """
    returns test folder
    """
    state = StateHandler().getCurrentState()
    return make_response(jsonify({'test_folder': state.test_dir}), 200)
