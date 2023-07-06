#!/usr/bin/python3
"""
Contains Handler for handling states related funtions
"""
from flask import current_app
from robotarm.states.base_state import BaseState
from robotarm.states.django_state import DjangoState
from robotarm.handlers import helpers
import os
from robotarm import states
import subprocess
import yaml
import asyncio
# TODO: make a database handler
# TODO: implement git init repo method
# TODO: improve provision environment, make it more interactive


class StateHandler:
    """
    handles state related funtions, utilized by state apis

    methods:
        getCurrentSate
        activate
        deactivate
        createState
        deleteState
        all_states
        provisionEnv
    """
    SUPPORTED_FRAMEWORKS = {
        'django': 'states.django_state.DjangoState'
    }

    SUPPORTED_DATABASE = {
        'postgresql': 'helpers.postgresCreate'
    }

    def getCurrentState(self):
        """
        Returns the current state
        """
        id = states.storage.all()['current_state']['id']
        if id != None:
            return states.storage.get(id)
        return None

    def activate(self, id):
        """
        activates a state by setting it as current state

         Args:
            id [uuid]: unique identifier of states object

        Returns:
            None if setCurrentState returns None
        """
        state = states.storage.setCurrentState(id)
        states.storage.save()

        wd = state.wdir
        if os.path.isdir(wd) and os.getcwd() != wd:
            os.chdir(wd)

        vpath = state.virtual_venvs[0]
        try:
            os.mkdir('scripts')
            with open('scripts/env', mode='w', encoding='utf8') as file:
                text = f"#!/bin/bash\nsource {vpath}/bin/activate\nalias activate='source {vpath}/bin/activate'"
                file.write(text)
            subprocess.Popen(['chmod', 'u+x', 'scripts/env'])
        except FileExistsError:
            pass
        return state

    def deactivate(self):
        """
        deactivates the current state
        """
        states.storage.removeCurrentState()

    def createState(self, **kwargs):
        """
        Parses a Yaml File into a python native dictionary objects
        and creats a state

         Args:
            file_name [string]: name of or path to file

        Returns:

        """
        file_name = kwargs['file']
        yaml_dict = self.parseYamlFile(file_name)
        #print(yaml_dict)
        if yaml_dict:
            framework = yaml_dict.get('framework', None)
            print(framework)
            if framework != None:
                if framework in self.SUPPORTED_FRAMEWORKS.keys():
                    state = BaseState(**yaml_dict)
                    state.save()
                    print('---state saved---')

                    # print('activating state...')
                    # state = self.activate(state.id)
                    #print(f'{state.project_name} activated')

                    #print('setting up environment, this may take a few minutes...')
                    #self.provisionEnv(state)
                    #print('done.')

            else:
                state = BaseState(**yaml_dict)
                state.save()
                print('---state saved---')

                # print('activating state...')
                # state = self.activate(state.id)
                #print(f'{state.project_name} activated')

                #print('setting up environment, this may take a few minutes...')
                #self.provisionEnv(state)
                #print('done.')
        return state
                #xit('Unsurppoted framework')

    def deleteState(self, id):
        """
        deletes a state object

         Args:
            id [uuid]: unique identifier of states object

        Returns:
            None if state does not exists
        """
        try:
            states.storage.delete(id)
        except Exception:
            return None

    @staticmethod
    def parseYamlFile(file):
        """
        tries to open and parse a yaml file to dictionary object
        """
        pwd = os.getcwd()
        os.chdir(pwd)
        try:
            with open(f'{file}', mode='r', encoding='utf8') as file:
                yaml_dict = yaml.full_load(file)
                return yaml_dict
        except FileNotFoundError:
            print("file not found")

    @staticmethod
    def all_states():
        """
        retrieves all states objects
        """
        states_objs = states.storage.all()
        state_dict = {}

        for key, value in states_objs.items():
            if key != 'current_state':
                state_dict[key] = {'name': value.project_name, 'version': value.version}
        state_dict['current_state'] = states_objs['current_state']
        
        return state_dict
    
    @staticmethod
    def create_virtual_env(name: str, vpath: str) -> bool:
        try:
            created = helpers.mkVenvLinux(vpath)
        except Exception as error:
            raise Exception({'error': f'an error occured while creating a the virtual environment {name}',
                             'details': error})
        return created
    
    def setup_database(self, type: str, database_config: dict) -> bool:
        try:
            function = eval(self.SUPPORTED_DATABASE[type])
            database_config.pop('type')
            database_config.pop('on_create')
            created = function(**database_config)
        except Exception as error:
            raise Exception({'error': 'an error occured while creating database',
                             'details': error})
        return created

    #@staticmethod
    def provisionEnv(self, state):
        """
        provision a development environment based on state object

        Args:
            state [__class__]: a __class__.BaseState object
        """
        try:
            print('provisioning...')
            wd = state.get('wdir')
            #print(wd)
            if os.path.isdir(wd) and os.getcwd() != wd:
                os.chdir(wd)
            
            if state.get('venvs'):
                venvs = state.get('venvs')
                for venv in venvs:
                    on_create = venv['on_create']
                    #print(on_create)
                    if on_create:
                        name = venv['name']
                        vpath = f'{wd}/{name}'
                        if venv['dir'] != '.':
                            vpath = venv['dir']
                        created = self.create_virtual_env(name, vpath)
                        if created:
                            print(f'created virtual environment at {vpath}')
                    else:
                        pass
            else:
                pass
                    

            if state.get('databases'):
                databases = state.get('databases')
                for database in databases:
                    on_create = database['on_create']
                    if on_create:
                        try:
                            type = database.get('type', None)
                            config = database
                            if type:
                                created = self.setup_database(type, config)
                            else:
                                raise('error: database type must be set')
                        except KeyError:
                            print(f"error: database type {type}, not supported.")
                        if created:
                            print('created database')
                    else:
                        pass
            else:
                pass

        except Exception as error:
            print(f'error: {error}')

