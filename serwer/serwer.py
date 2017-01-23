#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from math import sin, cos, fabs

# Aby uruchomic nalezy zainstalowac modul "flask" do pythona:
# python -m pip install flask
# Po odpaleniu aplikacji mozna sprawdzic jak dziala. Najlepiej CURLem:
# Przykladowo:
# curl -i "http://localhost:5000/WAM/api/getHeight/?x=1&y=3"
# Wysle zapytanie getHeight do serwera, ten wyliczy wysokosc i ja zwroci w response.

# Stworzenie serwera aplikacji we flasku
app = Flask(__name__)

# Mapa bedaca funkcja matematyczna
function = 'sin(x)+sin(y)'

# GET do pobrania wysokosci przy podaniu parametrow X i Y
@app.route('/WAM/api/getHeight/', methods=['GET'])
def task():
    z = get_height(float(request.args.get('x')),float(request.args.get('y')))
    return jsonify({'height': z})

# POST do pobierania mapy
@app.route('/WAM/api/postMap/', methods=['POST'])
def post_map():
    if not request.json or not 'map' in request.json:
        abort(400)
    global function
    task = {
        'map': function,
        'shouldBe': request.json['map'],
        'done': True
    }
    function = str(request.json['map'])
    return jsonify({'task': task}), 201   

# przy zlym strzeleniu do WS response bedzie error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def get_height(x, y):
    return eval(function)

if __name__ == '__main__':
    app.run(debug=True)