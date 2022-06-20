#!/usr/bin/python3
'''
start_arm_api
'''
import os

def main():
    os.system('gunicorn -b 0.0.0.0:5555 armservice.app:app')

if __name__ == '__main__':
    main()