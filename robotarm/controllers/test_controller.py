#!/usr/bin/python3
"""
Test Controller module
"""
import subprocess
from  robotarm.controllers import proxy_url
import requests
import shlex

class TestController():
    """
    communicates with appropiate api test service
    and performs several test actions

    actions:
    get_tests_folder:
        Args: [None]
        Description: sends a get request to /states/get_test_folder/
        Returns: string containing test folder name

    get_working_dir:
        Args: [None]
        Description: sends a get request to /states/get_test_folder/
        Returns: string containing test folder name

    run:
        Args: args[list]
        Description: runs a test specified test method
        Returns: None

    test_module:
        Args: module[str], cwd[str]
        Description: runs a test module
        Returns: None

    test_dir:
        Args: cwd[str], dir[str]
        Description: discovers tests in a given directory
        Returns: None
    """

    def get_tests_folder(self):
        """
        gets the tests folder from endpoint
        """
        # build url endpoint
        # and headers
        url = proxy_url + '/states/get_test_folder/'
        headers = {
            'content-type': 'application/json'
        }

        # send get request
        response = requests.get(url, headers=headers)

        # check status_code
        if response.status_code == 200:
            return response.json().get('test_folder')
        return False

    def get_working_dir(self):
        """
        gets the project working directory
        """
        # build url endpoint
        # and headers
        url = proxy_url + '/states/get_working_dir/'
        headers = {
            'content-type': 'application/json'
        }

        # send get request to endpoint
        response = requests.get(url, headers=headers)
        
        # check status code
        if response.status_code == 200:
            return response.json().get('working_dir')
        return False

    def run(self, args):
        """
        runs tests specified

        run_options:
            -m, --test_module:
                Args: module[str], cwd[str]
                Description: runs a single test module
                Returns: None

            -d, --dir:
                Args: dir[str], cwd[str]
                Description: tries to discover tests in specified directory
                Return: None
            
            -D, --test_dir:
                Args: dir[None], cwd[str]
                Description: tries to discover tests in test folder specified in
                             state.
                Return: None


        """
        # deletes the run command not needed
        del(args[0])

        # get working directory
        working_dir = self.get_working_dir()

        run_options = {
            ('-m', '--test_module'): 'self.test_module',
            ('-d', '--dir'): 'self.test_dir',
            ('-D', '--test_dir'): 'self.test_dir'
        }

        # if arguments were supplied handle it
        if args:

            # expects a test option
            try:
                run_option = args[0]
            except IndexError:
                exit('error: expected a run option')
            
            # tries to map and run
            # a test option
            try:
                extra_arg = args[1]
                for keyword_options in run_options.keys():
                    if run_option in keyword_options:
                        eval(run_options[keyword_options])(args[1], working_dir)
            except IndexError:
                exit('error: expected extra argument')
        else:
            subprocess.run(['python3', '-m', 'unittest', 'discover'], cwd=working_dir)

    def test_module(self, module:str, cwd:str):
        """
        tries to run a test module
        """
        if module is None:
            raise(TypeError, 'please provide a module to run')

        subprocess.run(['python3', '-m', 'unittest', f'{module}'], cwd=cwd)

    def test_dir(self, cwd:str, dir=None):
        """
        tries to discover tests in giving directory
        """
        if dir:
            subprocess.run(['python3', '-m', 'unittest', '-s', f'{dir}'], cwd=cwd)
            exit('test run completed')
        
        test_folder = self.get_tests_folder()
        subprocess.run(['python3', '-m', 'unittest', '-s', f'{test_folder}'], cwd=cwd)
        
