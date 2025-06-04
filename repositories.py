import random
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from game_objects import *

dynamodb = boto3.resource('dynamodb')

tableGames = dynamodb.Table('BogglingsGames')
tablePlayers = dynamodb.Table('BogglingsPlayers')
tablePlayerTurns = dynamodb.Table('BogglingsPlayerTurns')
tableTurns = dynamodb.Table('BogglingsTurns')

def get_game(gameId: str) -> Game:
    response = tableGames.get_item(
        Key={
            'gameId': gameId
        }
    )
    if 'Item' in response:
        item = response['Item']
        score = Score(
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
    
def create_game(gameId: str, playerId: str, turnIndex: int, losses: int, wins: int, numericalScore: int, status: str) -> Game:
    createdDate = lastUsedDate = datetime.now().isoformat()
    item = {
        'gameId': gameId,
        'createdDate': createdDate,
        'lastUsedDate': lastUsedDate,
        'playerId': playerId,
        'turnIndex': turnIndex,
        'losses': losses,
        'wins': wins,
        'numericalScore': numericalScore,
        'status': status
    }
    tableGames.put_item(Item=item)
    return Game(
        gameId=gameId,
        createdDate=createdDate,
        lastUsedDate=lastUsedDate,
        playerId=playerId,
        turnIndex=turnIndex,
        score=Score(
            losses=losses,
            wins=wins,
            numericalScore=numericalScore,
            status=status
        )
    )

def get_turn(turnId: str) -> Turn:
    response = tableTurns.get_item(
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
        tableTurns.update_item(
            Key={'turnId': turnId},
            UpdateExpression='SET lastUsedDate = :lastUsedDate',
            ExpressionAttributeValues={':lastUsedDate': last_used_date}
        )
        return turn
    else:
        return None

def get_random_turn(turn_index: int):
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        
        # Verify table exists
        tableTurns.load()
        
        # Verify GSI exists by checking table's index configuration
        table_info = dynamodb.meta.client.describe_table(TableName=tableTurns.name)
        indexes = table_info['Table'].get('GlobalSecondaryIndexes', [])
        gsi_name = 'turnIndex-index'  # Replace with your GSI name
        if not any(index['IndexName'] == gsi_name for index in indexes):
            print(f"GSI '{gsi_name}' not found on table 'Turns'")
            return None

        # Query using the GSI
        response = tableTurns.query(
            IndexName=gsi_name,
            KeyConditionExpression=Key('turnIndex').eq(turn_index),
            ProjectionExpression='turnId, turnIndex, gameId, createdDate, lastUsedDate, turnState',  
        )
        
        items = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = tableTurns.query(
                IndexName=gsi_name,
                KeyConditionExpression=Key('turnIndex').eq(turn_index),
                ProjectionExpression='turnId, turnIndex',
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))
        
        if not items:
            print(f"No records found for turnIndex={turn_index}")
            return None
                            

        item = random.choice(items)  

        if item:
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
            tableTurns.update_item(
                Key={'turnId': turn.turnId},
                UpdateExpression='SET lastUsedDate = :lastUsedDate',
                ExpressionAttributeValues={':lastUsedDate': last_used_date}
            )
            return turn

        return None
       
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        if error_code == 'ResourceNotFoundException':
            print(f"Resource not found: {error_msg}. Check table 'Turns' and GSI '{gsi_name}' in your AWS region.")
        else:
            print(f"DynamoDB error: {error_code} - {error_msg}")
        return None
    except Exception as e:
        print(f"Error querying DynamoDB: {str(e)}")
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
    tableTurns.put_item(Item=item)
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
        score = Score(
            losses=item['losses'],
            wins=item['wins'],
            numericalScore=item['numericalScore'],
            status=item['status']
        )
        playerTurn = PlayerTurn(
            playerTurnId=item['playerTurnId'],
            createdDate=item['createdDate'],
            lastUsedDate=item['lastUsedDate'],
            turnId=item['turnId'],
            turnIndex=item['turnIndex'],
            score=score
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
    
def create_player_turn(playerTurnId: str, turnId: str, turnIndex: int, score: Score) -> PlayerTurn:
    createdDate = lastUsedDate = datetime.now().isoformat()
    item = {
        'playerTurnId': playerTurnId,
        'turnId': turnId,
        'createdDate': createdDate,
        'lastUsedDate': lastUsedDate,
        'losses': score.losses,
        'wins': score.wins,
        'numericalScore': score.numericalScore,
        'status': score.status,
        'turnIndex': turnIndex

    }
    tablePlayerTurns.put_item(Item=item)
    return PlayerTurn(
        playerTurnId=playerTurnId,
        turnId=turnId,
        createdDate=createdDate,
        lastUsedDate=lastUsedDate,
        score=score
    )