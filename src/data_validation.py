import pandas as pd
from data_processing import clock_move_check, clock_game_check

moves_df = pd.read_csv("data/processed/moves.csv") ## move level table
games_df = pd.read_csv("data/processed/games.csv") ## game level table

##### VALIDATING THE DATA (mainly for moves df) #####

## checking missing values per game and move
##clock_game_check(moves_df)
clock_move_check(moves_df)
## check an values for all rows
print(moves_df.isna().sum())
##checking for duplicates
##print(moves_df.duplicated().sum())

## checking move numbers per game
print(moves_df.groupby("game_id").size().describe())

##checking move numbers
print(moves_df["move_number"].describe())

## checking game ids
print(moves_df["game_id"].nunique())
print(moves_df["game_id"].min())
print(moves_df["game_id"].max())

## finding missing ids and getting their pgns
## the first df missing ids are gone due to no moves do they can be ignroed
#all_ids = set(range(moves_df["game_id"].min(), moves_df["game_id"].max() + 1))
#existing_ids = set(moves_df["game_id"].unique())
#missing_ids = all_ids - existing_ids
#print(missing_ids)
#print(moves_df[moves_df["game_id"].isin([364, 439, 829, 1075, 2918])])
#print(df.loc[[364, 439, 829, 1075, 2918], ["pgn"]])

## now checking the games_df
print(games_df.isna().sum())
print(games_df.duplicated().sum())
print(games_df["game_id"].nunique())

print(games_df.columns.tolist())
