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

## creating game_id, result, datetime columns and filtering to fit thje postgresql table
df["game_id"] = range(len(df)) ## id column for game table

df["result"] = df["white_result"].map({
    "win": "white_win",
    "resigned": "white_loss",
    "checkmated": "white_loss",
    "abandoned": "white_loss",
    "timeout": "white_loss",
    "stalemate": "draw",
    "repetition": "draw",
    "insufficient": "draw",
    "agreed": "draw",
    "timevsinsufficient": "draw",
    "50move": "draw"
})

df["date"] = pd.to_datetime(df["end_time"], unit="s").dt.date

df = df[[
    "game_id",
    "username",
    "white_username",
    "black_username",
    "white_rating",
    "black_rating",
    "result",
    "date",
    "time_control",
    "time_class",
    "rated",
    "url",
    "pgn"
]]

df.to_csv("data/processed/games.csv", index=False)

## headers to use wiht newly parsed game
# print(game.headers["White"])
# print(game.headers["Black"])
# print(game.headers["WhiteElo"])

## going through each mvoe of the game (e4e5 format, not standard chess notation)
#for move in game.mainline():
    #print(move)

full_df = []

## creating a function to parse games
def game_parser(game):
    ## making a board object to display moves in standard chess notation
    ## only contains the starting position, still have to loop thorugh game and apply the moves to board
    ## (SAN = standard algebraic notation)
    ## each node in the or loop contaisn move anc clock position
    board = game.board()
    game_data = []
    strings = ["White", "Black"]
    num_moves = game.end().ply()
    i = 0

    ## for loop fills each row of the dictionary, which will become a dataframe
    for node in game.mainline():
        san_move = board.san(node.move)
        move_number = node.parent.board().fullmove_number
        move = {
            "move_number": move_number,
            "colour": strings[i % 2],
            "move": san_move,
            "clock_time": node.clock()
        }
        game_data.append(move)

        if node.move not in board.legal_moves:
            print("Illegal move found")
            break

        board.push(node.move)
        i += 1

    game_df = pd.DataFrame(game_data)
    return game_df

for game_id, pgn in enumerate(df["pgn"]):
    ## converting to format to be used by game_parser
    game_pgn = io.StringIO(pgn) # makes the string a file to be used below
    game = chess.pgn.read_game(game_pgn)

    ## skip games with no moves
    if game.end().ply() == 0:
        continue

    game_df = game_parser(game)
    game_df["game_id"] = game_id

    full_df.append(game_df)

##combingin all dtaframes into one
full_df = pd.concat(full_df, ignore_index = True)
full_df["move_number"] = full_df["move_number"].astype(int) ## removing decimal places
full_df.to_csv("data/processed/moves.csv", index = False)

## function to check game level clock availability
def clock_game_check(df):
    present = 0
    for i in df["game_id"].unique():
        if df[df["game_id"] == i]["clock_time"].notna().any():
            present += 1
        else:
            print(f"no time data for game {i}", df[df["game_id"] == i])
    print(f"{round(100.0 * (present / df['game_id'].nunique()), 2)}% of games contain clock data")

## functoin to check move level clock availability
def clock_move_check(df):
    present = 0
    for i in range(len(df)):
        if pd.notna(df.iloc[i]["clock_time"]):
            present += 1
        else:
            print(f"no clock data for index {i}")
    print(f"{round(100.0 * (present / len(df)), 2)}% of moves contain clock data")


