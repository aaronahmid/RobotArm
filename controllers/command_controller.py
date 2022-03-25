"""
command controller module
"""
from controllers import proxy_url
import requests
import subprocess
import os


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

        if res.status_code == 200:
            state_dict = dict(res.json())

        working_dir = state_dict['working_dir']
        entry_command = state_dict['entry_command']

        # if os.curdir() != working_dir:
        #     os.chdir(working_dir)
        args.insert(0, entry_command)
        with open('logfile', 'w+', encoding='utf8') as file:
            subprocess.Popen(args=args, stderr=file, cwd=working_dir)

    # TODO: create listCommands method

    def listCommands(self, args=None):
        """
        """
        pass
