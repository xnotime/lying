from flask import Flask, render_template, request, redirect

from base64 import b64encode
from random import randrange

from game import Game, Speaker, Player

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

games = {}

words = [
    ['lick', 'eat', 'drink', 'taste', 'hug', 'befriend', 'deify'],
    [ str(i) for i in range(2, 112) ],
    ['dirty', 'tasty', 'yummy', 'gross', 'sketchy', 'wet', 'crying', 'scary', 'mysterious'],
    ['ovens', 'cows', 'sheep', 'tvs', 'cameras', 'sewers', 'pianos', 'cables', 'pizzas', 'chairs', 'floors', 'tacos', 'trees', 'pigs', 'rats', 'mice', 'trumpets', 'lamps'],
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
        games[code].add_player(Player(
            ne,
            Speaker(request.form['wlink'])
        ))
        return redirect(f'/joined/{code}/speaker/{ne}')
    else:
        raise KeyError('Role doesnt exist')

@app.route('/joined/<code>/<role>/<ne>', methods= ['GET', 'POST'])
def joined(code: str, role: str, ne: str):
    assert role in ('speaker', 'judge')
    assert code in games
    if request.method.upper() == 'POST':
        games[code].attach_desc(ne, request.form['desc'])
    time = games[code].get_time(ne)
    return render_template(f'joined_{role}.html', code= code, ne= ne, time= time)

@app.route('/api/<code>/start')
def api_start(code: str):
    assert code in games
    games[code].start_game()
    return 'ok'

@app.route('/api/<code>/chosen/article')
def api_chosen_article(code: str):
    assert code in games
    return games[code].chosen_article()

@app.route('/api/<code>/status')
def api_status(code: str):
    assert code in games
    return games[code].status()

@app.route('/api/<code>/speakers')
def api_speakers(code: str):
    assert code in games
    return games[code].speakers_json()

@app.route('/api/<code>/guess/<ne>')
def api_guess(code: str, ne: str):
    assert code in games
    return 'green' if games[code].guess(ne) else 'red'
