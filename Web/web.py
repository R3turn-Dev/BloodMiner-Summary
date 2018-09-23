from flask import Flask

from db import DBConnector
from settings import Config


_config = Config()
_web_config = _config.get("Web")
_db_config = _config.get("Database")


app = Flask("BloodCoinGrapher")



app.register_blueprint()