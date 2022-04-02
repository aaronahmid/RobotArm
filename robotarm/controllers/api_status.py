"""
State Controller Module
"""
from robotarm.controllers import proxy_url
import requests

class APIStatusController:
    """
    Performs requests to the status API endpoints

    actions:
        health_check: checks api status
    """

    __base_api = proxy_url + '/status'

    def health_check(self, args):
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
            print(e)
            exit("APIs aren't running, Are you sure you started the server")
        print('==========================================================\nchecks complete')


