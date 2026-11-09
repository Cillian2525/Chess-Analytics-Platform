import pandas as pd
from data_processing import clock_move_check, clock_game_check

full_df = pd.read_csv("data/processed/moves.csv")

##### VALIDATING THE DATA #####

## checking missing values per game and move
##clock_game_check(full_df)
clock_move_check(full_df)
## check an values for all rows
print(full_df.isna().sum())
##checking for duplicates
##print(full_df.duplicated().sum())

## checking move numbers per game
print(full_df.groupby("game_id").size().describe())

##checking move numbers
print(full_df["move_number"].describe())

## checking game ids
print(full_df["game_id"].nunique())
print(full_df["game_id"].min())
print(full_df["game_id"].max())

## finding missing ids and getting their pgns
## the first df missing ids are gone due to no moves do they can be ignroed
#all_ids = set(range(full_df["game_id"].min(), full_df["game_id"].max() + 1))
#existing_ids = set(full_df["game_id"].unique())
#missing_ids = all_ids - existing_ids
#print(missing_ids)
#print(full_df[full_df["game_id"].isin([364, 439, 829, 1075, 2918])])
#print(df.loc[[364, 439, 829, 1075, 2918], ["pgn"]])
