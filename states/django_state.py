#!/usr/bin/python3
"""
contains Django State
"""
from ast import arg
from states.base_state import BaseState


class DjangoState(BaseState):
    """
     A django State
    """
    commands = {
        "runserver": 'spinning up development server',
        'makemigrations': 'creating migrations',
        'migrate': 'migrating your data',
        'shell': 'starting shell'
    }
    entry_command = 'manage.py'

    def __init__(self, *args, **kwargs):
        """
        Initializes Django State
        """
        super().__init__(*args, **kwargs)

    def perform_migration(self):
        """
        would perform makemigration and migrate
        """
        pass