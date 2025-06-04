from flask import Flask, jsonify, request
from game_objects import *
from repositories import *

app = Flask(__name__)

@app.route('/api/players', methods=['GET'])
def get_players():
    player_id = request.args.get('playerId')
    player = get_player(player_id)
    if not player:
        player = create_player(player_id)
    return jsonify(player.to_dict())

@app.route('/api/turns', methods=['GET'])
def get_turns():
    turn_id = request.args.get('turnId')
    turn = get_turn(turn_id)
    if not turn:
        turn = create_turn(turn_id)
    return jsonify(turn.to_dict())

@app.route('/api/turns', methods=['POST'])
def create_new_turn():
    data = request.json
    turn_id = data.get('turnId')
    game_id = data.get('gameId')
    turn_state = data.get('turnState')
    turn_index = data.get('turnIndex')
    
    if not all([turn_id, game_id, turn_state, turn_index is not None]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    turn = create_turn(turn_id, game_id, turn_state, turn_index)
    return jsonify(turn.to_dict()), 201

@app.route('/api/playerturns', methods=['GET'])
def get_player_turns():
    player_turn_id = request.args.get('playerTurnId')
    player_turn = get_player_turn(player_turn_id)
    if not player_turn:
        player_turn = create_player_turn(player_turn_id)
    return jsonify(player_turn.to_dict())

@app.route('/api/playerturns', methods=['POST'])
def create_new_player_turn():
    data = request.json
    player_turn_id = data.get('playerTurnId')
    turn_id = data.get('turnId')
    score = data.get('score')
    if not all([player_turn_id, turn_id, score]):
        return jsonify({'error': 'Missing required fields'}), 400
    player_turn = create_player_turn(player_turn_id, turn_id, score)
    return jsonify(player_turn.to_dict()), 201

@app.route('/api/games', methods=['GET'])
def get_games():
    game_id = request.args.get('gameId')
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(game.to_dict())

@app.route('/api/games', methods=['POST'])
def create_new_game():
    data = request.json
    game_id = data.get('gameId')
    player_id = data.get('playerId')
    turn_index = data.get('turnIndex')
    score_id = data.get('scoreId')
    losses = data.get('losses')
    wins = data.get('wins')
    numerical_score = data.get('numericalScore')
    status = data.get('status')
    game = create_game(game_id, player_id, turn_index, score_id, losses, wins, numerical_score, status)
    return jsonify(game.to_dict()), 201
    

if __name__ == '__main__':
    app.run(debug=True)