import berserk
import time
from dotenv import load_dotenv
import os
import chess
import similar_positions_eval
import frequency_squares
import helpers

load_dotenv()  
TOKEN = os.getenv("LICHESS_TOKEN")
PLAYER = os.getenv("PLAYER")

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

num_games = 500 #Number of games to import 
perf_types = "ultraBullet,bullet,blitz,rapid,classical,correspondence"
games = client.games.export_by_player(PLAYER, max=num_games, perf_type=perf_types)

helpers.create_position_database(games)
test_pos = chess.Board()
test_pos.set_fen("rn1q2k1/p1Bp1rpp/5n2/7P/3pb3/8/PP3PP1/2RQ1RK1 b KQkq - 0 1")
similar_positions_eval.material_eval(test_pos, chess.WHITE)
frequency_squares.print_frequency_tables()