#!/usr/bin/python3
"""
Blueprint initialization
"""
from flask import Blueprint

# create blueprint to register/mount
app_views = Blueprint('api_views', __name__, url_prefix='/api')

# api endpoints
from api.views.index import *
