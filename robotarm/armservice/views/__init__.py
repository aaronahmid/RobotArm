#!/usr/bin/python3
"""
Blueprint initialization
"""
from flask import Blueprint

# create blueprint to register/mount
api_views = Blueprint('api_views', __name__, url_prefix='/api')

# TDOD: 

# api endpoints
from robotarm.armservice.views.index import *
from robotarm.armservice.views.state import *
from robotarm.armservice.views.command import *
