import os

from flask import Flask, render_template


STATIC_FOLDER = os.getenv("STATIC_FOLDER", None)  # absolute path to static folder


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",  # TODO: this should be loaded from env var and be different on prod
        DATABASE=os.path.join(app.instance_path, "hymnal.sqlite"),  # same here
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    if STATIC_FOLDER is not None:
        app.static_folder = STATIC_FOLDER

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db, commands
    db.init_app(app)
    commands.init_app(app)

    from . import hymns

    app.register_blueprint(hymns.bp)
    app.add_url_rule("/", endpoint="hymn_list")

    return app
