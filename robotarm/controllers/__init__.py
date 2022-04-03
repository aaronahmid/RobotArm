#!/usr/bin/python3
"""
controllers initialization
"""
proxy_url = 'http://127.0.0.1:5555/api'

from  controllers.api_service import APIServiceController
from  controllers.command_controller import CommandController
from  controllers.state_controller import StateController
from  controllers.test_controller import TestController
