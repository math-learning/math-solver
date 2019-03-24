#!/bin/bash
rm -r static
cd ..
cd front-demo
npm run build
cp -r ./build ../server/static
cd ../server
pip install -r requirements.txt
FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run