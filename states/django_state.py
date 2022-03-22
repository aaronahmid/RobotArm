#!/usr/bin/python3
"""
contains Django State
"""
from click import command
from states.base_state import BaseState


class DjangoState(BaseState):
    """
     A django State
    """
    entry_command = 'manage.py'
    commands = {
        "runserver": ['runserver', 'spinning up development server'],
        'makemigrations': ['makemigrations', 'creating migrations'],
        'migrate': ['migrate', 'migrating your data',],
        'shell': ['shell', 'starting shell'],
        'make_superuser': ['createsuperuser', 'creating a super user'],
    }

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
