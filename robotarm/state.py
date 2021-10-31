#!/usr/bin/python3
"""
State object class Module for the Robotarm package
"""

import json

class State:
    """
    State object class

    Attributes:
        __project_root: Project Root Directory
        __project_name[str]: Name of project
        __project_version[str]: Project Version
        __language:[str]: Language Robotarm should be initialized to
        __framework_library[str]: Framework or library utilized by the project
        __enable_git:bool
        __database:str
        __setup_env:str
        __requirements:str
    """
    __project_root = '.'
    __project_name = '.'
    __project_version = '0.0.1'
    __language = ''
    __framework_library = ''
    __enable_git = True
    __database = ''
    __setup_env = False
    __requirements = ''

    def __init__(
        self,
        language,
        framework_library=None,
        project_name=None,
        project_root=None,
        project_version=None,
        enabled_git=True,
        database=None,
        requirements=None
        ):
        pass
