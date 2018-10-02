from os import urandom
from flask import Flask, session
from pages import blueprints as bps
from exceptions import InvalidModuleException
from settings import Config

conf = Config()
app_config = conf.get("Web")

_temp = app_config.get("secret_key")
if _temp:
    _secret_key = app_config.get("secret_key")
    del app_config["secret_key"]
else:
    _secret_key = urandom(32)

app = Flask(__name__)
app.secret_key = _secret_key


@app.before_request
def make_empty_session(*_, **__):
    if not session.get("credentials"):
        session['credentials'] = {
            "logged_in": False,
            "display_name": "placeholder"
        }


for module in bps:
    if not hasattr(module, "setup"):
        raise InvalidModuleException(f"An improper blueprint module was passed : {module}")

    module.setup(app)

app.run(**app_config)