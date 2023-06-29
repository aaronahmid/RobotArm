#!/usr/bin/python3
"""
State Controller Module
"""
from robotarm.controllers import proxy_url
import requests
from tabulate import tabulate

# TODO: Make an Error Handler That provides Error codes, details and a logfile
# TODO: Decide on API request pattern


class StateController():
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
        curl -H "Content-Type: application/json" -X POST -d '{"file_name": "armfile"}' http://127.0.0:5000/api/states/create/

        Args:
            args (list): argument list

        Return:
            success: 'created' if status code is 201
        """
        # expects a filename at index[1]
        try:
            file_name = args[1]
        except IndexError:
            exit('error: file name/path not supplied')

        # builds data json data sent
        # headers
        # and url endpoint
        data = {"file": f"{file_name}"}
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'create/'

        # sends a post request to the url endpoint
        # with above data and headers
        request = requests.post(url, json=data, headers=headers)

        # checks status code
        # collects response data
        # and prints an output
        if request.status_code == 201:
            json_response = request.json()
            proj_name = json_response.get('project_name')
            state_id = json_response.get('id')
            print(f"created new state [project_name: {proj_name}, id: {state_id}]'",
                  f"\nrun 'arm -s activate {state_id}' and then run 'source scripts/env' load environmental vairables")
        else:
            print("error: something went wrong")

    def activate(self, args):
        """
        performs the activate action by triggering the /states/activate endpoint
        to avtivate up an environment

        Example:
        curl -H "Content-Type: application/json" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/load/

        Args:
            args (list): argument list

        Return:
            success: 'activated' if status code is 200)
        """
        # expects an id at index[1]
        try:
            state_id = args[1]
        except IndexError:
            exit('error: environment "state id" not supplied')

        # builds data json data sent
        # headers
        # and url endpoint
        headers = {'content-type': 'application/json'}
        url = self.__base_api + f'{state_id}/activate/'

        # sends a put request to the url endpoint
        # with the following headers above
        request = requests.put(url, headers=headers)

        # checks status code
        # if state exist
        # prints an output
        if request.status_code == 200:
            if request.text != 'None':
                print('activated', state_id)
                print("run 'source scripts/env' to activate and load venv")
                print("then you can run 'activate' or 'deactivate'")
        elif request.status_code == 404:
            print('error: state does not exist')
        else:
            print('error: something is not right')

    # would be removed
    def stop(self, args):
        """
        performs a stop action by triggering the /states/stop endpoint to stop environment specified

        Example:
        curl -H "Content-Type: application/json" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/stop/

        Args:
            args (list): argument list

        Return:
            success: 'stopped' if status code is 200

        """
        # expects an id at index[1]
        try:
            state_id = args[1]
        except IndexError:
            exit('error: environment "state id" not supplied')

        # builds data json data sent
        # headers
        # and url endpoint
        headers = {'content-type': 'application/json'}
        url = self.__base_api + f'{state_id}/stop/'

        # sends a put request to the url endpoint
        # with the following headers above
        request = requests.put(url, headers=headers)

        # checks status code
        # prints an output
        if request.status_code == 200:
            print('stopped', state_id)
        elif request.status_code == 404:
            print('error: state does not exist')
        else:
            print('error: something is not right')

    def delete(self, args):
        """
        performs a delete action by triggering the /states/delete endpoint to delete environment specified

        Example:
        curl -H "Content-Type: application/json" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/delete/

        Args:
            args (list): argument list

        Return:
            success: 'deleted' if status code is 200
        """
        # expects an id at index[1]
        try:
            state_id = args[1]
        except IndexError:
            exit('error: environment "state id" not supplied')

        # builds data json data sent
        # headers
        # and url endpoint
        headers = {'content-type': 'application/json'}
        url = self.__base_api + f'{state_id}/delete/'

        # sends a put request to the url endpoint
        # with the following headers above
        request = requests.post(url, headers=headers)

        # checks status code
        # prints an output
        if request.status_code == 200:
            print('deleted', state_id)
        elif request.status_code == 404:
            print('error: state does not exist')
        else:
            print('error: something is not right')

    def list(self, args):
        """
        performs a list action by triggering the states/
        """
        del(args)

        headers = {'content-type': 'application/json'}
        url = self.__base_api
        request = requests.get(url, headers=headers)

        if request.status_code == 200:
            states = dict(request.json())

            activated = states['current_state']
            del(states['current_state'])
            state_list = []

            for key, value in states.items():
                if key != activated['id']:
                    state_list.append([value['name'], key])
                else:
                    state_list.append([value['name'], key, '*'])

            state_list.insert(0, ['name', 'id', 'activated'])
            print(tabulate(state_list, headers='firstrow'))
