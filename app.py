from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    developer = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    plataform = db.Column(db.String(80), nullable=False)
    classification = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desarrollador': self.developer,
            "anio_lanzamiento": self.year,
            "plataforma": self.plataform,
            "clasificacion": self.classification
        }

@app.route('/')
def index():
    return 'Welcome to my GAMING API :D'

@app.route('/create_game', methods=['POST'])
def create_game():
    if not request.json or not 'name' in request.json:
        abort(400)
    game = Game(name=request.json['name'], status=request.json.get('status', False))
    db.session.add(game)
    db.session.commit()
    return jsonify(game.to_dict()), 201

@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([game.to_dict() for game in games])

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get(game_id)
    if game is None:
        abort(404)
    return jsonify(game.to_dict())

@app.route('/games_update/<int:game_id>', methods=['GET'])
def update_game(game_id):
    game = Game.query.get(game_id)
    if game is None:
        abort(404)
    game.status = not game.status
    return jsonify(game.to_dict())

@app.route('/games_delete/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game is None:
        abort(404)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'status':True}), 201

@app.route('/games_update/<int:game_id>', methods=['PUT'])  # Cambia el método a PUT, que es más adecuado para actualizaciones.
def update_game_info(game_id):
    game = Game.query.get(game_id)
    if game is None:
        abort(404)  # Si la tarea no existe, retorna un error 404.
    if not request.json:
        abort(400)  # Si no hay cuerpo JSON, retorna un error 400.
    name = request.json.get('name')  # Obtiene el nombre de la solicitud JSON, si existe.
    if name is not None:
        game.name = name  # Actualiza el nombre de la tarea si se proporcionó uno nuevo.
    db.session.commit()  # Guarda los cambios en la base de datos.
    return jsonify(game.to_dict())  # Devuelve la tarea actualizada.

if __name__ == '_main_':
    with app.app_context():
        db.create_all()
        print("Tables created...")

if __name__ == '_main_':
    with app.app_context():
        db.create_all()
        print("Tables created...")

    app.run(debug=True)

