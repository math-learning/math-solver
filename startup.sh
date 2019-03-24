#!/bin/bash
gunicorn -w 4 app:run_app