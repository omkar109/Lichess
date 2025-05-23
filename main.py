import berserk
import time
from dotenv import load_dotenv
import os
import chess
import similar_positions_eval

load_dotenv()  
TOKEN = os.getenv("LICHESS_TOKEN")

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

num_games = 10 #Number of games to import 
perf_types = "ultraBullet,bullet,blitz,rapid,classical,correspondence"
games = client.games.export_by_player("omkar109", max=num_games, perf_type=perf_types)

similar_positions_eval.create_position_database(games)
test_pos = chess.Board()
test_pos.set_fen("rn1q2k1/p1Bp1rpp/5n2/7P/3pb3/8/PP3PP1/2RQ1RK1 b KQkq - 0 1")
similar_positions_eval.material_eval(test_pos, chess.WHITE)
