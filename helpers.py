import chess
from collections import defaultdict
import os

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

#frequency_table[piece (0-5)][color (0-1)][row (1-7)][col (1-7)]
frequency_table = [[[[0 for _ in range(8)] for _ in range(8)] for _ in range(2)] for _ in range(6)]
 
"""
This function takes in a list of games in SAN format, and stores each position from the game in the position 
databases
"""
def create_position_database(games):

    #Iterate throught all player games
    for game in games:
        moves = game["moves"] #Get the move in string SAN format. Ex: "e4 e5 Nc6"
        white_to_play = True #Flag to know which database to store move in
        PLAYER = os.getenv("PLAYER")
        user_to_play = game['players']['white']['user']['name'] == PLAYER
        board = chess.Board()

        #Iterate over each move in the game
        for move in moves.split():
            move = board.parse_san(move)
            if user_to_play:
                white_material_value, black_material_value = _get_material_value(board)
                if white_to_play:
                    white_position_database[board.fen()] = [move, white_material_value, black_material_value]
                    white_material_database[_mpf(white_material_value, black_material_value)].append(board.fen()) 
                else:
                    black_position_database[board.fen()] = [move, white_material_value, black_material_value]
                    black_material_database[_mpf(white_material_value, black_material_value)].append(board.fen()) 

                piece = board.piece_at(move.from_square)
                if piece:
                    piece_index = piece.piece_type - 1           # Map piece type 1-6 → index 0-5 [P,N,B,R,Q,K]
                    color_index = 0 if piece.color == chess.WHITE else 1
                    row = 7 - chess.square_rank(move.to_square)  # Flip rank to match array row
                    col = chess.square_file(move.to_square)
                frequency_table[piece_index][color_index][row][col] += 1

                white_to_play = not white_to_play
            user_to_play = not user_to_play
            board.push(move)
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


#Hashing function given white and black material values (helps control number of entries filters by material_eval filter)
def _mpf(white, black):
    return (white+black)//(white + 0.000001)