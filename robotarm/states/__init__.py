#!/usr/bin/python3
"""
states initialization settings
"""
from robotarm.states.json_storage.json_storage import StateJsonStorage

storage = StateJsonStorage()
try:
    state = storage.reload()
except FileExistsError or FileNotFoundError:
    print("Not state to load...")
