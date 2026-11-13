import pandas as pd
from database import engine

games_df = pd.read_csv("data/processed/games.csv") ## game level table
moves_df = pd.read_csv("data/processed/moves.csv") ## move level table


## exporting tables ot postgresql db

games_df.to_sql(
    name = "games",
    con = engine,
    if_exists = 'append',
    index = False
)
moves_df.to_sql(
    name = "moves",
    con = engine,
    if_exists = 'append',
    index = False
)



print("succesfully exported data")