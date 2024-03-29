#!/usr/bin/python3
"""
Command Handler module
"""
from robotarm import states
from robotarm.handlers import StateHandler


class CommandHandler:
    """
    are utilized by the api and returns required state
    information on how to handle commands 
    """

    @staticmethod
    def getEntryCommand():
        """
        gets current activated state and returns it's management
        entry command if available and the current working directory
        """
        current_state = StateHandler().getCurrentState()

        response_dict = {
            'working_dir': current_state.wdir,
            'entry_command': current_state.entry_command
        }
        return response_dict

    @staticmethod
    def getAllCommands():
        pass
