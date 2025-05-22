import chess
from collections import defaultdict

"""
This evaluation function takes in a current position and finds the most similar position among all games played. Then it outputs the next move played in that position.
This move may or may not be a legal move in the input position. In this case, a backup eval function must be relied on or engine evaluation
"""

"""
The position database is a hashtable where the key is the position in FEN string format and the 
# value is a list that stores the next move made and info about the position. White indicates in white's turn 
# to move. Each string is formatted as follows: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
#Format of value: [next move, white_material_value, black_material_value]
next move is a string in san format
"""
white_position_database = {}
black_position_database = {}


#The keys will be the difference between value of white's material and value of black's material. The values will be a list of positions (could have multiple positions per key)
white_material_database = defaultdict(list)
black_material_database = defaultdict(list)

"""
This function takes in a position and side to play and outputs either the move to be made in this position or 
that no next move was found. The position is passed as a board object
"""
def get_next_move(board, color):
    positions = material_eval(board, color)
    return

"""
This function takes in a list of games in SAN format, and stores each position from the game in the position 
databases
"""
def create_position_database(games):

    #Iterate throught all player games
    for game in games:
        moves = game["moves"] #Get the move in string SAN format. Ex: "e4 e5 Nc6"
        white_to_play = True #Flag to know which database to store move in

        board = chess.Board()

        #Iterate over each move in the game
        for move in moves.split():
            white_material_value, black_material_value = _get_material_value(board)
            if white_to_play:
                white_position_database[board.fen()] = [move, white_material_value, black_material_value]
                white_material_database[_mpf(white_material_value, black_material_value)].append(board.fen()) 
            else:
                black_position_database[board.fen()] = [move, white_material_value, black_material_value]
                black_material_database[_mpf(white_material_value, black_material_value)].append(board.fen()) 
            white_to_play = not white_to_play
            board.push(board.parse_san(move))
        board.clear()
    return

"""
Given a board object, returns the total value of white's material and of black's material
"""        
def _get_material_value(board):
    piece_set = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    white_material_value = 0
    black_material_value = 0
    for piece in piece_set:
        curr_bitboard = tuple(board.pieces(piece, chess.WHITE))
        if piece == chess.PAWN:
            white_material_value += len(curr_bitboard)
        elif piece == chess.KNIGHT:
            white_material_value += len(curr_bitboard) * 3
        elif piece == chess.BISHOP:
            white_material_value += len(curr_bitboard) * 3
        elif piece == chess.ROOK:
            white_material_value += len(curr_bitboard) * 5
        elif piece == chess.QUEEN:
            white_material_value += len(curr_bitboard) * 9

    for piece in piece_set:
        curr_bitboard = tuple(board.pieces(piece, chess.BLACK))
        if piece == chess.PAWN:
            black_material_value += len(curr_bitboard)
        elif piece == chess.KNIGHT:
            black_material_value += len(curr_bitboard) * 3
        elif piece == chess.BISHOP:
            black_material_value += len(curr_bitboard) * 3
        elif piece == chess.ROOK:
            black_material_value += len(curr_bitboard) * 5
        elif piece == chess.QUEEN:
            black_material_value += len(curr_bitboard) * 9
    
    return white_material_value, black_material_value
    


"""
Given a position and a color to play, will return the positions which are most similar in terms of absolute difference between white material value and black material value.
The position is represented as a board object
"""
def material_eval(board, color):
    white_material_value, black_material_value = _get_material_value(board)
    n = 5
    similar_positions = []
    difference = 0
    while len(similar_positions) < n:
        material_value = _mpf(white_material_value, black_material_value)
        if color == chess.WHITE:
            if difference == 0:
                positions = white_material_database[material_value]
            else:
                positions = white_material_database[material_value]
                positions.extend(white_material_database[material_value])
            difference += 1
        else:
            if difference == 0:
                positions = black_material_database[material_value]
            else:
                positions = black_material_database[material_value + difference]
                positions.extend(black_material_database[material_value - difference])
            difference += 1
        similar_positions.extend(positions)

    # print(white_material_value, black_material_value)
    # testboard = chess.Board()
    # for position in similar_positions:
    #     testboard.set_fen(position)
    #     print(testboard.unicode(), "\n\n")
    return similar_positions

#Similarity heuristics (can/should combine multiple):
#Material held by each side, Distance between important pieces, Stage/move number, Squares controlled possibly
#Follow a filtered approach where material held reduces pool by a little, then distance between pieces, etc

#Parameters to tune include, number of games to parse, weighting between heuristics, 

#Hashing function given white and black material values (helps control number of entries filters by material_eval filter)
def _mpf(white, black):
    return (white+black)//white



