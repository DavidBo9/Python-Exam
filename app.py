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
    game = Game(name=request.json['name'], 
                developer=request.json['developer'], 
                year=request.json['year'],
                platform=request.json['platform'],
                classification=request.json['classification'],
                status=request.json.get('status', False))
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

if __name__ == '__main__':  # Corrected from '_main_'
    with app.app_context():
        db.create_all()
        print("Tables created...")

    app.run(debug=True)
