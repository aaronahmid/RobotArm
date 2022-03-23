"""
Test Controller module
"""

from controllers import proxy_url
import requests


class TestController:
    """
    communicates with appropiate api service

    actions:

    """

    def runTests(self, args=None):
        """
        sends a request to the run test api service
        """
        if args:
            print(args)