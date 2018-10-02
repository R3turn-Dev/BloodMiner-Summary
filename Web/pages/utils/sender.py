from os import listdir
from os.path import realpath
from time import time
from flask import render_template_string, send_from_directory, session


def rpath(cls):
    return realpath(cls.parent.template_folder)


def render_template(cls, template_name, **kwargs):
    if isinstance(cls, str):
        return render_template_string(
            open(f"{cls}/{template_name}", "r", encoding="UTF-8").read(),
            debugstring="",
            session=session,
            get_global=get_global_file,
            **kwargs
        )
    else:
        return render_template_string(
            open(f"{rpath(cls)}/{template_name}", "r", encoding="UTF-8").read(),
            debugstring=time() if cls.is_debugging() else "",
            session=session,
            get_global=get_global_file,
            **kwargs
        )


def send_raw(folder, _filename):
    return send_from_directory(folder, _filename)


def get_global_file(filename, **kwargs):
    if filename in listdir("pages/global/"):
        return render_template("pages/global/", filename, **kwargs)
    else:
        return ""
