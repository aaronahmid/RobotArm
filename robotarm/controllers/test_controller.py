#!/usr/bin/python3
"""
Test Controller module
"""
import subprocess
from  controllers import proxy_url
import requests
import shlex

class TestController:
    """
    communicates with appropiate api test service
    and performs several test actions

    actions:  

    """

    def get_tests_folder(self):
        """
        gets the tests folder from apis
        """
        url = proxy_url + '/states/get_test_folder/'
        headers = {
            'content-type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('test_folder')
        return False

    def get_project_wd(self):
        """
        gets the project working direction
        """
        url = proxy_url + '/states/get_working_dir/'
        headers = {
            'content-type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get('working_dir')

    def run_module(self, module:str):
        """
        runs test module
        """
        pass

    def run(self, args):
        """
        and runs the tests in the following state test folder specified
        """
        del(args[0]) # deletes the run command

        working_dir = self.get_project_wd()

        run_options = {
            ('-m', '--test_module'): 'self.test_module',
            ('-d', '--dir'): 'self.test_dir',
            ('-D', '--test_dir'): 'self.test_dir'
        }
        if args:
            for key in run_options.keys():
                if args[0] in key:
                    eval(run_options[key])(args[1], working_dir)

        else:
            subprocess.run(['python3', '-m', 'unittest', 'discover'], cwd=working_dir)

    def test_module(self, module:str, cwd:str):
        """
        tries to run a test module
        """
        if module is None:
            raise(TypeError, 'please provide a module to run')

        subprocess.run(['python3', '-m', 'unittest', f'{module}'])

    def test_dir(self, cwd:str, dir=None):
        if dir:
            subprocess.run(['python3', '-m', 'unittest', '-s', f'{dir}'], cwd=cwd)
            exit('test run completed')
        
        test_folder = self.get_tests_folder()
        subprocess.run(['python3', '-m', 'unittest', '-s', f'{test_folder}'], cwd=cwd)
        