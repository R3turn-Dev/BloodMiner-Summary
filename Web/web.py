from flask import Flask

from settings import Config


_config = Config()
_web_config = _config.get("Web")
_db_config = _config.get("Database")


app = Flask("BloodCoinGrapher")


import root
import graph

app.register_blueprint(root.page)
app.register_blueprint(graph.graph_api)


app.run(
    **_web_config
)
