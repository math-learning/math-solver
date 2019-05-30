from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.INFO)

from src.controllers.step_controller import *
from src.controllers.hints_controller import *
from src.controllers.result_controller import *

if __name__ == "__main__":
    app.run()