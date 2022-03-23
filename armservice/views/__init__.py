#!/usr/bin/python3
"""
Blueprint initialization
"""
from flask import Blueprint

# create blueprint to register/mount
api_views = Blueprint('api_views', __name__, url_prefix='/api')

# api endpoints
from armservice.views.index import *
from armservice.views.state import *
from armservice.views.command import *
