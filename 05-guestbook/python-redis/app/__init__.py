from flask import Flask
from app.config import Config
from flask_debug import Debug

app = Flask(__name__)

app.config.from_object(Config)

from app import routes

