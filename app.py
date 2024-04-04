from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# Enabling CORS for all domains on all routes, adjust in production as needed
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    developer = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(80), nullable=False)
    classification = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'developer': self.developer,
            "year": self.year,
            "platform": self.platform,
            "classification": self.classification,
            "status": self.status
        }

@app.route('/')
def index():
    return 'Welcome to my GAMING API :D'

@app.route('/create_game', methods=['POST'])
def create_game():
    if not request.json or not 'name' in request.json:
        abort(400)
    try:
        game = Game(name=request.json['name'], 
                    developer=request.json['developer'], 
                    year=request.json['year'],
                    platform=request.json['platform'],
                    classification=request.json['classification'],
                    status=request.json.get('status', False))
        db.session.add(game)
        db.session.commit()
        return jsonify(game.to_dict()), 201
    except Exception as e:
        print(e)
        abort(500)

@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()
        return jsonify([game.to_dict() for game in games])
    except Exception as e:
        print(e)
        abort(500)

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    try:
        game = Game.query.get(game_id)
        if game is None:
            abort(404)
        return jsonify(game.to_dict())
    except Exception as e:
        print(e)
        abort(500)

@app.route('/games_update/<int:game_id>', methods=['PUT'])  # Changed to PUT for semantic correctness
def update_game(game_id):
    try:
        game = Game.query.get(game_id)
        if game is None:
            abort(404)
        game.status = not game.status
        db.session.commit()
        return jsonify(game.to_dict())
    except Exception as e:
        print(e)
        abort(500)

@app.route('/games_delete/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    try:
        game = Game.query.get(game_id)
        if game is None:
            abort(404)
        db.session.delete(game)
        db.session.commit()
        return jsonify({'status': 'Game deleted successfully'}), 200
    except Exception as e:
        print(e)
        abort(500)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created...")
    app.run(debug=True)
