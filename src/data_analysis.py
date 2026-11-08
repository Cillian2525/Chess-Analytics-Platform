import pandas as pd
from data_processing import clock_move_check, clock_game_check

full_df = pd.read_csv("data/processed/moves.csv")

## checking missing values per game and move
clock_game_check(full_df)
clock_move_check(full_df)
## check an values for all rows
print(full_df.isna().sum())
##checking for duplicates
print(full_df.duplicated().sum())