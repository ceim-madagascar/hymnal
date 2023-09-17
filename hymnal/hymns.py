from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.exceptions import abort
from hymnal.db import get_db    
from hymnal.utils import slugify

bp = Blueprint("hymns", __name__)

@bp.route('/')
def hymn_list():
    db = get_db()
    songs = db.execute(
        "SELECT title, slug, content FROM hymns ORDER BY title ASC"
    ).fetchall()
    return render_template("hymn_list.html", songs=songs)


@bp.route("/new", methods=["POST", "GET"])
def create_hymn():
    error = None
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"] or ""

        if not title:
            error = "Title is required."
        slug = slugify(title)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # TODO : check if a hymn w/ similar slug already exists
            db.execute(
                'INSERT INTO hymns (title, slug, content) VALUES (?, ?, ?)',
                (title, slug, content)
            )
            db.commit()
            return redirect(url_for("hymns.hymn_list"))
    return render_template("create_hymn.html")
