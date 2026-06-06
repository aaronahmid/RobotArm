#!/usr/bin/python3
"""
controllers initialization
"""
proxy_url = 'http://127.0.0.1:5555/api'

from  robotarm.controllers.api_service import APIServiceController
from  robotarm.controllers.command_controller import CommandController
from  robotarm.controllers.state_controller import StateController
from  robotarm.controllers.test_controller import TestController
