from datetime import datetime


class Score:
    def __init__(
            self,
            losses: int = 0,
            wins: int = 0,
            numericalScore: int = 0,
            status: str = "unknown"):
        self.losses = losses
        self.wins = wins
        self.numericalScore = numericalScore
        self.status = status        
    def to_dict(self):
        return {
            'losses': self.losses,
            'wins': self.wins,
            'numericalScore': self.numericalScore,
            'status': self.status
        }

class Game:
    def __init__(
            self, 
            gameId: str,
            createdDate,
            lastUsedDate,
            playerId: str,
            turnIndex: int,
            score: Score):
        self.gameId = gameId
        self.createdDate = createdDate
        self.lastUsedDate = lastUsedDate
        self.playerId = playerId
        self.turnIndex = turnIndex
        self.score = score
    def to_dict(self):
        return {
            'gameId': self.gameId,
            'createdDate': self.createdDate,
            'lastUsedDate': self.lastUsedDate,
            'playerId': self.playerId,
            'turnIndex': self.turnIndex,
            'losses': self.score.losses,
            'wins': self.score.wins,
            'numericalScore': self.score.numericalScore,
            'status': self.score.status
        }

class Player:
    def __init__(
            self, 
            playerId: str,
            createdDate,
            lastUsedDate):
        self.playerId = playerId
        self.createdDate = createdDate
        self.lastUsedDate = lastUsedDate
    def to_dict(self):
        return {
            'playerId': self.playerId,
            'createdDate': self.createdDate,
            'lastUsedDate': self.lastUsedDate
        }

class Turn:
    def __init__(
            self, 
            turnId: str,
            gameId: str,
            createdDate,
            lastUsedDate,
            turnState: str,
            turnIndex: int):
        self.turnId = turnId
        self.gameId = gameId
        self.createdDate = createdDate
        self.lastUsedDate = lastUsedDate
        self.turnState = turnState
        self.turnIndex = turnIndex
    def to_dict(self):
        return {
            'turnId': self.turnId,
            'gameId': self.gameId,
            'createdDate': self.createdDate,
            'lastUsedDate': self.lastUsedDate,
            'turnState': self.turnState,
            'turnIndex': self.turnIndex
        }

class PlayerTurn:
    def __init__(
            self, 
            playerTurnId: str,
            createdDate,
            lastUsedDate,
            turnId: str,
            turnIndex: int,
            score: Score):
        self.playerTurnId = playerTurnId
        self.createdDate = createdDate
        self.lastUsedDate = lastUsedDate
        self.turnId = turnId
        self.turnIndex = turnIndex
        self.score = score
    def to_dict(self):
        return {
            'playerTurnId': self.playerTurnId,
            'createdDate': self.createdDate,
            'lastUsedDate': self.lastUsedDate,
            'turnId': self.turnId,
            'score': {
                'losses': self.score.losses,
                'wins': self.score.wins,
                'numericalScore': self.score.numericalScore,
                'status': self.score.status
            }
        }
