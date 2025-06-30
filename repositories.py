from game_objects import *
import pyodbc



def get_game(gameId: str) -> Game:
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.createdDate, g.lastUsedDate, g.turnIndex,
                   s.losses, s.wins, s.score, s.status
            FROM games g
            JOIN scores s ON g.gameId = s.gameID
            WHERE g.gameId = ?
        """, gameId)
        row = cursor.fetchone()
        if row:
            score = Score(row.losses, row.wins, row.score, row.status)
            return Game(gameId, row.createdDate, row.lastUsedDate, None, row.turnIndex, score)
        return None

def create_game(gameId: str, playerId: str, turnIndex: int, losses: int, wins: int, numericalScore: int, status: str) -> Game:
    createdDate = lastUsedDate = datetime.now()
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO games (gameId, createdDate, lastUsedDate, turnIndex) VALUES (?, ?, ?, ?)",
                       gameId, createdDate, lastUsedDate, turnIndex)
        cursor.execute("INSERT INTO scores (scoreID, losses, wins, score, status, gameID) VALUES (?, ?, ?, ?, ?, ?)",
                       gameId + "_score", losses, wins, numericalScore, status, gameId)
        conn.commit()
    score = Score(losses, wins, numericalScore, status)
    return Game(gameId, createdDate, lastUsedDate, playerId, turnIndex, score)


def get_turn(turnId: str) -> Turn:
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT gameID, createDate, lastUsedDate, turnsState, turnIndex
            FROM Turns WHERE turnID = ?
        """, turnId)
        row = cursor.fetchone()
        if row:
            return Turn(turnId, row.gameID, row.createDate, row.lastUsedDate, row.turnsState, row.turnIndex)
        return None

def get_random_turn(turn_index: int):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 1 turnID, gameID, createDate, lastUsedDate, turnsState, turnIndex
            FROM Turns
            WHERE turnIndex = ?
            ORDER BY NEWID()
        """, turn_index)
        row = cursor.fetchone()
        if row:
            return Turn(row.turnID, row.gameID, row.createDate, row.lastUsedDate, row.turnsState, row.turnIndex)
        return None

def create_turn(turnId: str, gameId: str, turnState: str, turnIndex: int) -> Turn:
    createdDate = lastUsedDate = datetime.now()
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Turns (turnID, gameID, createDate, lastUsedDate, turnsState, turnIndex)
            VALUES (?, ?, ?, ?, ?, ?)
        """, turnId, gameId, createdDate, lastUsedDate, turnState, turnIndex)
        conn.commit()
    return Turn(turnId, gameId, createdDate, lastUsedDate, turnState, turnIndex)

def get_player(playerId: str) -> Player:
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT createdDate, lastUsedDate FROM Players WHERE playerID = ?", playerId)
        row = cursor.fetchone()
        if row:
            return Player(playerId, row.createdDate, row.lastUsedDate)
        return None

def create_player(playerId: str) -> Player:
    createdDate = lastUsedDate = datetime.now()
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Players (playerID, createdDate, lastUsedDate) VALUES (?, ?, ?)",
                       playerId, createdDate, lastUsedDate)
        conn.commit()
    return Player(playerId, createdDate, lastUsedDate)

def get_player_turn(playerTurnId: str) -> PlayerTurn:
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.turnID, pt.turnIndex, pt.createDate, pt.lastUsedDate,
                   s.losses, s.wins, s.score, s.status
            FROM PlayerTurns pt
            JOIN scores s ON pt.scoreID = s.scoreID
            WHERE playerTurnID = ?
        """, playerTurnId)
        row = cursor.fetchone()
        if row:
            score = Score(row.losses, row.wins, row.score, row.status)
            return PlayerTurn(playerTurnId, row.createDate, row.lastUsedDate, row.turnID, row.turnIndex, score)
        return None

def create_player_turn(playerTurnId: str, turnId: str, turnIndex: int, score: Score) -> PlayerTurn:
    createdDate = lastUsedDate = datetime.now()
    score_id = playerTurnId + "_score"
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (scoreID, losses, wins, score, status, gameID) VALUES (?, ?, ?, ?, ?, ?)",
                       score_id, score.losses, score.wins, score.numericalScore, score.status, None)
        cursor.execute("""
            INSERT INTO PlayerTurns (playerTurnID, turnID, turnIndex, scoreID, createDate, lastUsedDate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, playerTurnId, turnId, turnIndex, score_id, createdDate, lastUsedDate)
        conn.commit()
    return PlayerTurn(playerTurnId, createdDate, lastUsedDate, turnId, turnIndex, score)