from flask import Blueprint, jsonify
from .utils import sender

from db import DBConnector
from settings import Config


class API:
    def is_debugging(self):
        return self.engine.debug

    def __init__(self, engine, path="./pages/root"):
        self.engine = engine

        self.parent = Blueprint(
            "API",
            __name__,
            url_prefix="/api",
            template_folder=path
        )

        ConfigDatabase = Config().get("Database")
        self.ApiDatabase = DBConnector(ConfigDatabase)


        @self.parent.route("/data/<ColumnTargets>")
        def API_GetColumnData(ColumnTargets):
            cols = ColumnTargets.split(",")

            Returns = {}
            for column in cols:
                err, DBData = self.ApiDatabase.fetch_column(column)

                if err:
                    return jsonify(
                        {
                            "error": "An error was occured while processing your request."
                        }
                    )

                Returns[column] = [
                    [
                        t.timestamp() * 1e3,
                        #int(t.timestamp() // 1e5 * 1e9),  # Drop under seconds
                        v
                    ] for t, v in DBData
                ]

            return jsonify(Returns)


def setup(engine):
    engine.register_blueprint(API(engine).parent)