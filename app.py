from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    songs = [
        ('a-celui-qui-nous-aime', "À celui qui nous aime"),
        ('a-dieu-soit-la-gloire', "À Dieu soit la gloire"),
        ('beni-soit-le-lien', "Béni soit le lien"),
        ('beni-l-eternel-mon-ame', "Béni l'Éternel, mon âme",)
    ]
    return render_template('songs_list.html', songs=songs)
