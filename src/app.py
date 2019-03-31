from flask import Flask

app = Flask(__name__)

from src.controllers.validate_controller import *

if __name__ == "__main__":
    app.run()