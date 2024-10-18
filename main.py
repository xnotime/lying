from flask import Flask, render_template, request, redirect

from base64 import b64encode
from random import randrange

from game import Game, Speaker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

games = {}

words = [
    ['fight', 'destroy', 'eat', 'drink', 'burn', 'build', 'milk', 'hug', 'smash'],
    [ str(i) for i in range(2, 112) ],
    ['dirty', 'clean', 'yummy', 'gross', 'boring', 'exciting', 'sketchy'],
    ['ovens', 'cows', 'sheep', 'tvs', 'cameras', 'sewers', 'pianos', 'cables'],
]

@app.route('/bad_code.html')
def bad_code():
    return render_template('bad_code.html')

@app.route('/join.html', methods= ['POST'])
def join():
    ne = b64encode((
        request.form['nick']
    ).encode('utf-8')).decode('utf-8')
    if request.form['role'] == 'judge':
        code = '-'.join([
            sub[randrange(0, len(sub))] for sub in words
        ])
        games[code] = Game(code, ne)
        return redirect(f'/joined/{code}/judge/{ne}')
    elif request.form['role'] == 'speaker':
        code = request.form['gamecode']
        if code not in games:
            return redirect('/bad_code.html')
        if request.form['wlink'].startswith('https://'):
            return redirect('/name_not_links_ya_fool.html')
        games[code].add_speaker(
            Speaker(ne, request.form['wlink'])
        )
        return redirect(f'/joined/{code}/speaker/{ne}')
    else:
        raise KeyError('Role doesnt exist')

@app.route('/joined/<code>/<role>/<ne>')
def joined(code: str, role: str, ne: str):
    assert role in ('speaker', 'judge')
    return render_template(f'joined_{role}.html', code= code, ne= ne)

@app.route('/api/<code>/start')
def api_start(code: str):
    return games[code].start_game()
