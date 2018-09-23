from flask import Flask

from settings import Config


_config = Config()
_web_config = _config.get("Web")
_db_config = _config.get("Database")


app = Flask("BloodCoinGrapher")


from graph import graph_api
app.register_blueprint(graph_api)


app.run(
    **_web_config
)
