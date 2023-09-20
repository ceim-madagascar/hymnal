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
        "SELECT title, slug, content, substr(title, 1, 1) as initial FROM hymns ORDER BY title ASC"
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
    return render_template("create_edit_hymn.html", hymn={})


@bp.route("/<string:slug>/edit", methods=["POST", "GET"])
def edit_hymn(slug: str):
    db = get_db()
    error = None
    hymn = db.execute(
        "SELECT title, slug, content FROM hymns WHERE slug = ?", (slug,)
    ).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"] or ""

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            # update hymn
            db.execute(
                'UPDATE hymns SET title = ?, content = ? WHERE slug = ?',
                (title, content, slug)
            )
            db.commit()
            return redirect(url_for("hymns.hymn_list"))
    return render_template("create_edit_hymn.html", edit=True, hymn=hymn)


@bp.route("/slide/<string:slug>", methods=["GET"])
def slide(slug: str):
    db = get_db()
    song = db.execute(
        "SELECT title, slug, content FROM hymns WHERE slug = ?", (slug,)
    ).fetchone()
    if song is None:
        abort(404, f"Hymn {slug} doesn't exist.")
    slides = []
    current_slide = []
    for line in song["content"].split("\n"):
        line = line.strip()
        if line == "":
            if current_slide:
                slides.append(current_slide)
            current_slide = []
        else:
            current_slide.append(line)

    return render_template("slide.html", song=song, slides=slides)
