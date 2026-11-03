import json
import pandas as pd

## loading the saved games
with open("data/raw/rapid_games.json", "r") as f: # open in read mode
    games = json.load(f)

## lodaing games as a pandas dataframe
## works by looping through the above loaded dictionary and extracting the
## games and usernames (**game unpacks the dictionary to go intoa new one)
df = pd.DataFrame([
    {**game, "username": username}
    for username, player_games in games.items()
    for game in player_games
])

print(df.head(5))