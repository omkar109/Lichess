import berserk
import time
from dotenv import load_dotenv
import os

load_dotenv()  
TOKEN = os.getenv("LICHESS_TOKEN")

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

perf_types = "ultraBullet,bullet,blitz,rapid,classical,correspondence"
games = client.games.export_by_player("omkar109", max=1, perf_type=perf_types)
time.sleep(3)

for game in games:
    print(f"{game['players']['white']['user']['name']} vs {game['players']['black']['user']['name']}")
    print(f"Result: {game['status']}")
