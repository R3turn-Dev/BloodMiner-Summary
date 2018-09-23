from flask import render_template_string, Blueprint, jsonify

from db import DBConnector
from settings import Config

ConfDatabase = Config().get("Database")
ApiDatabase = DBConnector(ConfDatabase)


def render_graph(contents: list, **kwargs):
    return render_template_string(
        open(r"templates/single_graph.html", encoding="UTF-8").read(),
        data_options=contents,
        **kwargs
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
            t.timestamp() * 1e3,
            #int(t.timestamp() // 1e5 * 1e9),  # Drop under seconds
            v
        ] for t, v in data
    ]

    return jsonify(data)
