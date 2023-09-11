import os

from flask import Flask, render_template


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

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def song_list():
        songs = [
            ("a-celui-qui-nous-aime", "À celui qui nous aime"),
            ("a-dieu-soit-la-gloire", "À Dieu soit la gloire"),
            ("beni-soit-le-lien", "Béni soit le lien"),
            (
                "beni-l-eternel-mon-ame",
                "Béni l'Éternel, mon âme",
            ),
        ]
        return render_template("songs_list.html", songs=songs)

    return app
