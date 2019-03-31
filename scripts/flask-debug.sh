#!/bin/bash
pip install -r requirements.txt
FLASK_APP=src/server.py FLASK_DEBUG=1 python -m flask run