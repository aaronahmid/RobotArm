#!/usr/bin/python3
"""
initialize the models package
"""
from states.engine.json_storage import JsonFileStorage
storage = JsonFileStorage()
storage.reload()