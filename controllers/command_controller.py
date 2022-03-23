"""
command controller module
"""
from controllers import proxy_url
import requests
import subprocess
import os


class CommandController:
    """
    communicates with appropiate api service for the
    command handler

    actions:
    """

    __base_api = proxy_url + '/commands/'

    def executeCommand(self, args):
        """
        """
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'execute/'
        request = requests.get(url, headers=headers) # should return path to working directory and entry command

        state_dict = {}
        if request.status_code == 200:
            state_dict = dict(request.json())

        working_dir = state_dict['working_dir']
        entry_command = state_dict['entry_command']

        # if os.curdir() != working_dir:
        #     os.chdir(working_dir)
        args.insert(0, entry_command)
        with open('logfile', 'w+', encoding='utf8') as file:
            subprocess.run(args=args, stderr=file, cwd=working_dir, start_new_session=False)

    def listCommands(self, args=None):
        """
        """
        pass