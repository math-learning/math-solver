from flask import Flask
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

from src.controllers.validate_controller import *
from src.controllers.hints_controller import *

if __name__ == "__main__":
    app.run()