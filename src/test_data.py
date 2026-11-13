import pandas as pd
from database import engine

## csv dataframes
games_df = pd.read_csv("data/processed/games.csv") ## game level table
moves_df = pd.read_csv("data/processed/moves.csv") ## move level table

## sql dataframes (read in as pandas dataframe)
games_df_sql = pd.read_sql("SELECT * FROM games", engine)
moves_df_sql = pd.read_sql("SELECT * FROM moves", engine)

## ensuring dataframes are comparable
## fixing date type to so it compares to what postgresql database returns (as opposed to str)
games_df["date"] = pd.to_datetime(games_df["date"]).dt.date
## ordering each df by game_id
games_df = games_df.sort_values("game_id").reset_index(drop=True)
games_df_sql = games_df_sql.sort_values("game_id").reset_index(drop=True)
moves_df = moves_df.sort_values(["game_id", "move_number", "colour"]).reset_index(drop=True)
moves_df_sql = moves_df_sql.sort_values(["game_id", "move_number", "colour"]).reset_index(drop=True)
## keeping moves tables columns consistently ordered
moves_df_sql = moves_df_sql[moves_df.columns]


## TEST 1: row counts (checking if all rows got correctly uploaded)
print("TEST 1.1 - Matching Rows (Games Table):", ("PASSED" if len(games_df) == len(games_df_sql) else "FAILED"))
print("TEST 1.2 - Matching Rows (Moves Table):", ("PASSED" if len(moves_df) == len(moves_df_sql) else "FAILED"), "\n")

## TEST 2: checking for null values
print("TEST 2.1 - No missing values (CSV Games Table):", "PASSED" if games_df.isnull().values.any() == False else "FAILED")
print("TEST 2.2 - No missing values (CSV Moves Table):", "PASSED" if moves_df.isnull().values.any() == False else "FAILED")
print("TEST 2.3 - No missing values (SQL Games Table):", "PASSED" if games_df_sql.isnull().values.any() == False else "FAILED")
print("TEST 2.4 - No missing values (SQL Moves Table):", "PASSED" if moves_df_sql.isnull().values.any() == False else "FAILED", "\n")

## TEST 3: Confirming every game id in games table is unique
print("TEST 3.1 - Every row contains a unique game id (CSV Game Table)", "PASSED" if games_df["game_id"].nunique() == len(games_df) else "FAILED")
print("TEST 3.2 - Every row contains a unique game id (SQL Game Table)", "PASSED" if games_df_sql["game_id"].nunique() == len(games_df_sql) else "FAILED")
print("TEST 3.3 - Every game ID in moves df is in games df (CSV tables)", "PASSED" if moves_df["game_id"].isin(games_df["game_id"]).all() else "FAILED")
print("TEST 3.4 - Every game ID in moves df is in games df (SQL tables)", "PASSED" if moves_df_sql["game_id"].isin(games_df_sql["game_id"]).all() else "FAILED", "\n")

## TEST 4: Confirm SQL tables contain same data as CSV
print("TEST 4.1 - Each game table's data matches:", "PASSED" if games_df.equals(games_df_sql) else "FAILED")
print("TEST 4.2 - Each move table's data matches:", "PASSED" if moves_df.equals(moves_df_sql) else "FAILED")
