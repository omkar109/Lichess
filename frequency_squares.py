import chess
from helpers import frequency_table

"""
Given a position in the form of a board object and a color to move, returns a move to play. 
"""
def get_next_move(board, color):
    return

piece_names = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
color_names = ["White", "Black"]

def print_frequency_tables():
    for piece_index, piece_name in enumerate(piece_names):
        for color_index, color_name in enumerate(color_names):
            print(f"\n=== {color_name} {piece_name} Frequency Table ===")

            table = frequency_table[piece_index][color_index]

            # Print ranks from 8 to 1 (top to bottom)
            for row in range(8):
                rank = 8 - row
                row_data = table[row]
                print(f"{rank} | " + " ".join(f"{val:3}" for val in row_data))

            print("   +--------------------------------")
            print("     a   b   c   d   e   f   g   h")

# Call the function (assuming your frequency_table is defined)