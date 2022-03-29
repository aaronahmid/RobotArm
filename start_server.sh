#!/usr/bin/bash
gunicorn -b 0.0.0.0:5555 armservice.app:app

