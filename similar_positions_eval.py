import chess
from helpers import _get_material_value, _mpf, white_material_database, black_material_database

"""
This evaluation function takes in a current position and finds the most similar position among all games played. Then it outputs the next move played in that position.
This move may or may not be a legal move in the input position. In this case, a backup eval function must be relied on or engine evaluation
"""


"""
This function takes in a position and side to play and outputs either the move to be made in this position or 
that no next move was found. The position is passed as a board object
"""
def get_next_move(board, color):
    positions = material_eval(board, color)
    return



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





