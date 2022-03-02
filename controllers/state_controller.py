"""
State Controller Module
"""
from email import header
from controllers import proxy_url
import requests

class StateController:
    """
    Performs requests to the states API endpoints

    actions:
        create: accepts a <file_name>, sends a requests to the /states/create endpoint
        load: accepts a <state_id>, sends a request to the /states/reload endpoint
        delete: accepts a <state_id>, sends a request to the /states/delete endpoint
        stop: accepts a <state_id>, sends a request to the /statest/stop
    """

    __base_api = proxy_url + '/api/states/'

    def create(self, args):
        """
        sends a request to the /states/create endpoint to create a new
        development environment state

        Example:
        curl -H "Content-Type" -X POST -d '{"file_name": "armfile"}' \
            http://127.0.0:5000/api/states/create/

        Args:
            args (list): argument list

        Return:
            success: 'created' if status code is 201
        """
        file_name = args[1]

        data = {'file_name': file_name}
        headers = {'content-type': 'application/json'}
        url += self.__base_api + 'create/'
        request = requests.post(url, data=data, headers=headers)

        if request.status_code == 201:
            d = request.json()
            print('created', d.get('name'))
        else:
            exit('not created')
        

    def load(self, args):
        """
        sends a request to the /states/load endpoint to load up an environment

        Example:
        curl -H "Content-Type" -X POST -d '{"state_id": "b24f3x"}' \
            http://127.0.0:5000/api/states/load/

        Args:
            args (list): argument list

        Return:
            success: 'loaded' if status code is 200)
        """
        state_id = args[1]

        data = {'state_id': state_id}
        headers = {'content-type': 'application/json'}
        url = self.__base_api + 'load/'
        request = requests.post(url, data=data, headers=headers)

        if request.status_code == 200:
            print('loaded', state_id)


    def stop(self, args):
        """
        sends a request to the /states/stop endpoint to stop environment specified

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
        sends a request to the /states/delete endpoint to delete environment specified

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