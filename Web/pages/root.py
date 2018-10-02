from flask import Blueprint
from .utils import sender


class Root:
    def is_debugging(self):
        return self.engine.debug

    def __init__(self, engine, path="./pages/root"):
        self.engine = engine

        self.parent = Blueprint(
            "Root",
            __name__,
            url_prefix="/",
            template_folder=path
        )
        self.mobile_platform = ['android', 'iphone', 'blackberry']

        @self.parent.route('/')
        def root(*_, **__):
            return sender.render_template(
                self,
                "index.html"
            )

        @self.parent.route("/<any(css, img, js, media):folder>/<path:filename>")
        def statics(folder, filename):
            print(f"{path}/", f"{folder}/{filename}")
            return sender.send_raw(f"{path}/", f"{folder}/{filename}")


def setup(engine):
    engine.register_blueprint(Root(engine).parent)