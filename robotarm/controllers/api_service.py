#!/usr/bin/python3
"""
State Controller Module
"""
import subprocess
from robotarm.controllers import proxy_url
import requests
import pathlib
import psutil

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
#print(BASE_DIR)

class APIServiceController():
    """
    contolls api service

    actions:
        health_check: checks api status
    """
    __api_start_script = 'start_arm_api.py'
    __base_api = proxy_url + '/status'
    __pid: int

    def start_service(self):
        """
        starts the api service process
        """
        try:
            dir = f'{BASE_DIR}/scripts'
            with open(f'{BASE_DIR}/logfile', mode='w', encoding='utf8') as file:
                subprocess.Popen(
                    ['python3', f'./scripts/{self.__api_start_script}'], stderr=file, cwd=BASE_DIR)
        except Exception as error:
            raise Exception({'error': 'could not start api server',
                             'details': error})

    def stop_service(self):
        """
        stops the api service process
        """
        try:
            p_name = 'gunicorn'
            for proc in psutil.process_iter(['pid', 'name']):
                if p_name == proc.name():
                    script_process = proc
                    script_process.kill()
        except ProcessLookupError:
            raise Exception(f'process with name {p_name} could not be found')


    def health_check(self):
        """
        sends a request to the /states/create endpoint to create a new
        development environment state

        Example:
        curl -H "Content-Type" -X GET \
            http://127.0.0:5555/api/status/

        Args:
            args (list): argument list

        Return:
            running: OK
        """
        print('performing api health check\n==========================================================')
        headers = {'content-type': 'application/json'}
        url = self.__base_api

        try:
            request = requests.get(url, headers=headers).json()
            status = request.get('status')
            
            if status == 'OK':
                print('STATUS: APIs Are Running :)')
            else:
                print("well I'm confused :(")
        except Exception as e:
            print("APIs aren't running, are you sure you started robotarm :(")
            return False
        
        print('==========================================================\nchecks complete')
        return True
