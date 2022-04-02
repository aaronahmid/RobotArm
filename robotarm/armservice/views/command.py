"""
command handler apis
"""
from robotarm.armservice.views import api_views
from robotarm import states
from flask import (
    make_response,
    request,
    jsonify
)
from robotarm.handlers import CommandHandler


@api_views.route('/commnds', methods=['GET'], strict_slashes=False)
def list_commands():
    """
    returns all available management command
    """
    response = CommandHandler().getAllCommands()

    return make_response(jsonify(response), 2)


@api_views.route('/commands/get_entry_command', methods=['GET'], strict_slashes=False)
def get_entry_command():
    """
    returns an entry command if available and the
    working directory of the current activated state
    """
    response = CommandHandler().getEntryCommand()

    return make_response(jsonify(response), 200)
