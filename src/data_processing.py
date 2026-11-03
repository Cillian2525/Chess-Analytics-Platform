import json
import pandas as pd
import chess.pgn ## for reading in gmae pgns
import io ## treat a pgn strign as a file

## loading the saved games
with open("data/raw/rapid_games.json", "r") as f: # open in read mode
    games = json.load(f)

## lodaing games as a pandas dataframe
## works by looping through the above loaded dictionary and extracting the
## games and usernames (**game unpacks the dictionary to go intoa new one)
## this dataframe still has dictionaries fro white nad black so that will be fixed later
df = pd.DataFrame([
    {**game, "username": username}
    for username, player_games in games.items()
    for game in player_games
])

# print(df.head(5))
# print(df.shape) -> (6258, 16)
# print(df.columns.tolist())
# print(df.isna().sum())
# print(df["white"].iloc[0])
# print(df["black"].iloc[0])

## expanding out the black and white dictionaries with json normalise
white = pd.json_normalize(df["white"]).add_prefix("white_")
black = pd.json_normalize(df["black"]).add_prefix("black_")

## merging these back into the original dataframe
## starting by removing the white and black dictionaries
df = df.drop(columns=["white", "black"])
df = pd.concat([df, white, black], axis = 1) ## axis = 1 puts rows

