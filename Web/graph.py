from flask import render_template_string, Blueprint, Response, jsonify
from json import dumps

from db import DBConnector
from settings import Config

ConfDatabase = Config().get("Database")
ApiDatabase = DBConnector(ConfDatabase)


def render_graph(self, contents: list):
    return render_template_string(
        open(r"templates/single_graph.html", encoding="UTF-8").read(),
        data_options=contents
    )


graph_api = Blueprint(
    "GraphAPI",
    "BP_GraphAPI",
    url_prefix="/api"
)


@graph_api.route("/data/<column>")
def API_GetColumnData(column):
    err, data = ApiDatabase.fetch_column(column)

    if err:
        return jsonify(
            {
                "error": "An error was occured while processing your request."
            }
        )

    data = [
        [
            int(t.timestamp() // 1e5 * 1e5),  # Drop under seconds
            v
        ] for t, v in data
    ]

    return jsonify(data)
