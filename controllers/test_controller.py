"""
Test Controller module
"""

from controllers import proxy_url
import requests

## TODO: create get test folder method
## TODO: create run test method
## TODO: create discover test method

class TestController:
    """
    communicates with appropiate api test service
    and performs several test actions

    actions:  

    """ 

    def run(self, args=None):
        """
        and runs the tests in the following state test folder specified
        """
        if args:
            print(args)