#!/usr/bin/python3
"""
command controller module
"""
from robotarm.controllers import proxy_url
import requests
import subprocess
import os

# TODO: create methods to run scritps added in yaml file

class CommandController:
    """
    communicates with appropiate command api service for the
    command handler, performs several command actions

    actions:
    """

    __base_api = proxy_url + '/commands/'

    # TODO: create get_path_entry_command method

    def executeCommand(self, args):
        """
        executes the following arguments passed in

        Args:
            args [list]: list of arguments to be executed

        actions:
            - get the working directory from currently activated state
        """
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'get_entry_command/'
        # should return path to working directory and entry command
        res = requests.get(url, headers=headers)
        
        # check status code
        if res.status_code == 200:
            state_dict = dict(res.json())
            
        # get working dir and entry command
        working_dir = state_dict['working_dir']
        entry_command = state_dict['entry_command']

        args.insert(0, entry_command)   # build the command list
        # execute command but write any error to a logfile
        with open('logfile', 'w+', encoding='utf8') as file:
            subprocess.Popen(args=args, stderr=file, cwd=working_dir)

    # TODO: create listCommands method
    def listCommands(self, args=None):
        """
        lists commands available
        """
        pass
