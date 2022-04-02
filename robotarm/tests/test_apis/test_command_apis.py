"""
"""
import json
import unittest
import subprocess
import pathlib
from wsgiref import headers
import requests
from controllers import proxy_url

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)

class TestCommandApis(unittest.TestCase):
    """
    """
    base_api = '/commands/'

    def setUp(self):
        """
        starts the arm services
        """
        try:
            with open('test_logfile', mode='w+', encoding='utf8') as file:
                self.server = subprocess.Popen([
                    'gunicorn',
                    '-b',
                    '0.0.0.0:5555',
                    'armservice.app:app'], stdout=file, stderr=file,
                    cwd=BASE_DIR)
        except Exception as e:
            raise(e)

    def testEntryCommandApi(self):
        """
        tests the entry_command api
        must return a dictonary containing
        [
            key['entry_command'],
            key['working_dir']
        ]
        """
        url = proxy_url + self.base_api + 'get_entry_command/'
        headers = {
            'content-type': 'application/json'
        }
        res = requests.get(url, headers=headers)
        dict_res = dict(res.json())
        keys = []
        for key in dict_res.keys():
            keys.append(key)
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(['entry_command', 'working_dir'], keys)
        
    def tearDown(self):
         self.server.kill()
