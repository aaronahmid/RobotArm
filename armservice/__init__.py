"""
some configs
"""

try:
    from decouple import config as getenv
except ImportError:
    from os import getenv