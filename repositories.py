from datetime import datetime
import boto3
from game_objects import *

dynamodb = boto3.resource('dynamodb')

tableGames = dynamodb.Table('BogglingsGames')
tablePlayers = dynamodb.Table('BogglingsPlayers')
tablePlayerTurns = dynamodb.Table('BogglingsPlayerTurns')
tableTurns = dynamodb.Table('BogglingsTurns')

def get_game(gameId: str) -> Game:
    response = tablePlayers.get_item(
        Key={
            'gameId': gameId
        }
    )
    if 'Item' in response:
        item = response['Item']
        score = Score(
            scoreId=item['scoreId'],
            createdDate=item['createdDate'],
            lastUsedDate=item['lastUsedDate'],
            losses=item['losses'],
            wins=item['wins'],
            numericalScore=item['numericalScore'],
            status=item['status']
        )
        game = Game(
            gameId=item['gameId'],
            createdDate=item['createdDate'],
            lastUsedDate=item['lastUsedDate'],
            playerId=item['playerId'],
            turnIndex=item['turnIndex'],
            score=score
        )
        last_used_date = datetime.utcnow().isoformat()
        game.lastUsedDate = last_used_date
        tableGames.update_item(
            Key={'gameId': gameId},
            UpdateExpression='SET lastUsedDate = :lastUsedDate',
            ExpressionAttributeValues={':lastUsedDate': last_used_date}
        )
        return game
    else:
        return None
    
def create_game(gameId: str, playerId: str, turnIndex: int, scoreId: str, losses: int, wins: int, numericalScore: int, status: str) -> Game:
    createdDate = lastUsedDate = datetime.now().isoformat()
    item = {
        'gameId': gameId,
        'createdDate': createdDate,
        'lastUsedDate': lastUsedDate,
        'playerId': playerId,
        'turnIndex': turnIndex,
        'scoreId': scoreId,
        'losses': losses,
        'wins': wins,
        'numericalScore': numericalScore,
        'status': status
    }
    tablePlayers.put_item(Item=item)
    return Game(
        gameId=gameId,
        createdDate=createdDate,
        lastUsedDate=lastUsedDate,
        playerId=playerId,
        turnIndex=turnIndex,
        score=Score(
            scoreId=scoreId,
            createdDate=createdDate,
            lastUsedDate=lastUsedDate,
            losses=losses,
            wins=wins,
            numericalScore=numericalScore,
            status=status
        )
    )

def get_turn(turnId: str) -> Turn:
    response = tablePlayerTurns.get_item(
        Key={
            'turnId': turnId
        }
    )
    if 'Item' in response:
        item = response['Item']
        turn = Turn(
            turnId=item['turnId'],
            gameId=item['gameId'],
            createdDate=item['createdDate'],
            lastUsedDate=item['lastUsedDate'],
            turnState=item['turnState'],
            turnIndex=item['turnIndex']
        )
        last_used_date = datetime.utcnow().isoformat()
        turn.lastUsedDate = last_used_date
        tablePlayers.update_item(
            Key={'turnId': turnId},
            UpdateExpression='SET lastUsedDate = :lastUsedDate',
            ExpressionAttributeValues={':lastUsedDate': last_used_date}
        )
        return turn
    else:
        return None

def create_turn(turnId: str, gameId: str, turnState: str, turnIndex: int) -> Turn:
    createdDate = lastUsedDate = datetime.now().isoformat()
    item = {
        'turnId': turnId,
        'gameId': gameId,
        'createdDate': createdDate,
        'lastUsedDate': lastUsedDate,
        'turnState': turnState,
        'turnIndex': turnIndex
    }
    tablePlayerTurns.put_item(Item=item)
    return Turn(
        turnId=turnId,
        gameId=gameId,
        createdDate=createdDate,
        lastUsedDate=lastUsedDate,
        turnState=turnState,
        turnIndex=turnIndex
    )

def get_player(playerId: str) -> Player:
    response = tablePlayers.get_item(
        Key={
            'playerId': playerId
        }
    )
    if 'Item' in response:
        item = response['Item']
        player = Player(
            playerId=item['playerId'],
            createdDate=item['createdDate'],
            lastUsedDate=item['lastUsedDate'],
        )
        last_used_date = datetime.utcnow().isoformat()
        player.lastUsedDate = last_used_date
        tablePlayers.update_item(
            Key={'playerId': playerId},
            UpdateExpression='SET lastUsedDate = :lastUsedDate',
            ExpressionAttributeValues={':lastUsedDate': last_used_date}
        )
        return player
    else:
        return None

def create_player(playerId: str) -> Player:
    createdDate = lastUsedDate = datetime.now().isoformat()
    item = {
        'playerId': playerId,
        'createdDate': createdDate,
        'lastUsedDate': lastUsedDate,
    }
    tablePlayers.put_item(Item=item)
    return Player(
        playerId=playerId,
        createdDate=createdDate,
        lastUsedDate=lastUsedDate
    )

def get_player_turn(playerTurnId: str) -> PlayerTurn:
    response = tablePlayerTurns.get_item(
        Key={
            'playerTurnId': playerTurnId
        }
    )
    if 'Item' in response:
        item = response['Item']
        playerTurn = PlayerTurn(
            playerTurnId=item['playerTurnId'],
            gameId=item['gameId'],
            createdDate=item['createdDate'],
            lastUsedDate=item['lastUsedDate'],
            turnState=item['turnState'],
            turnIndex=item['turnIndex']
        )
        last_used_date = datetime.utcnow().isoformat()
        playerTurn.lastUsedDate = last_used_date
        tablePlayerTurns.update_item(
            Key={'playerTurnId': playerTurnId},
            UpdateExpression='SET lastUsedDate = :lastUsedDate',
            ExpressionAttributeValues={':lastUsedDate': last_used_date}
        )
        return playerTurn
    else:
        return None
    
def create_player_turn(playerTurnId: str, turnId: str, score: Score) -> PlayerTurn:
    createdDate = lastUsedDate = datetime.now().isoformat()
    item = {
        'playerTurnId': playerTurnId,
        'turnId': turnId,
        'createdDate': createdDate,
        'lastUsedDate': lastUsedDate,
        'scoreId': score.scoreId,
        'losses': score.losses,
        'wins': score.wins,
        'numericalScore': score.numericalScore,
        'status': score.status
    }
    tablePlayerTurns.put_item(Item=item)
    return PlayerTurn(
        playerTurnId=playerTurnId,
        turnId=turnId,
        createdDate=createdDate,
        lastUsedDate=lastUsedDate,
        score=score
    )