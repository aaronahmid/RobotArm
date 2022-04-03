#!/usr/bin/python3
"""
State Controller Module
"""
from controllers import proxy_url
import requests


class StateController:
    """
    Performs the following actions by triggering the right api states service

    actions:
        create: accepts a <file_name>, sends a requests to the /states/create endpoint
        load: accepts a <state_id>, sends a request to the /states/reload endpoint
        delete: accepts a <state_id>, sends a request to the /states/delete endpoint
        stop: accepts a <state_id>, sends a request to the /statest/stop
    """

    __base_api = proxy_url + '/states/'

    def create(self, args):
        """
        performs a create action by triggering the /states/create endpoint
        to create a new development environment state

        Example:
        curl -H "Content-Type" -X POST -d '{"file_name": "armfile"}' http://127.0.0:5000/api/states/create/

        Args:
            args (list): argument list

        Return:
            success: 'created' if status code is 201
        """
        try:
            file_name = args[1]
        except IndexError:
            exit('file name/path not supplied')

        data = {"file": f"{file_name}"}
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'create/'
        request = requests.post(url, json=data, headers=headers)

        if request.status_code == 201:
            jres = request.json()
            print(f"created new state [project_name: {jres.get('project_name')}, id: {jres.get('id')}]'",
                  f"\nrun 'arm -s activate {jres.get('id')}' and 'source scripts/env' load environmental vairables")
        else:
            print(request.text)

    def activate(self, args):
        """
        performs the activate action by triggering the /states/activate endpoint
        to avtivate up an environment

        Example:
        curl -H "Content-Type" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/load/

        Args:
            args (list): argument list

        Return:
            success: 'loaded' if status code is 200)
        """
        state_id = args[1]
        headers = {'content-type': 'application/json'}
        url = self.__base_api + f'{state_id}/activate/'
        request = requests.put(url, headers=headers)

        if request.status_code == 200:
            if request.text != 'None':
                print('activated', state_id)
                print("run 'source scripts/env' to activate and load venv")
                print("run 'activate' or 'deactivate'")
            else:
                print('state does not exist')

    def stop(self, args):
        """
        performs a stop action by triggering the /states/stop endpoint to stop environment specified

        Example:
        curl -H "Content-Type" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/stop/

        Args:
            args (list): argument list

        Return:
            success: 'stopped' if status code is 200

        """
        state_id = args[1]

        data = {'state_id': state_id}
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'stop/'
        request = requests.post(url, data=data, headers=headers)

        if request.status_code == 200:
            print('stopped', state_id)

    def delete(self, args):
        """
        performs a delete action by triggering the /states/delete endpoint to delete environment specified

        Example:
        curl -H "Content-Type" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/delete/

        Args:
            args (list): argument list

        Return:
            success: 'deleted' if status code is 200
        """
        state_id = args[1]

        data = {'state_id': state_id}
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'deleted/'
        request = requests.post(url, data=data, headers=headers)

        if request.status_code == 200:
            print('deleted', state_id)

    def list(self, args):
        """
        performs a list action by triggering the states/list/
        """
        del(args)

        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'list/'
        request = requests.get(url, headers=headers)

        if request.status_code == 200:
            rd = dict(request.json())
            print(f'{len(rd.keys())} states')
            print(rd)
