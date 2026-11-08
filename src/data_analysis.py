import pandas as pd

full_df = pd.read_csv("data/processed/moves.csv") ## reading in df


## recheck clock data (if it has at least 1 value fro clock_time)
present = 0
for i in full_df["game_id"].unique():
    if full_df[full_df["game_id"] == i]["clock_time"].notna().any():
        present += 1
    else:
        print(f"no time data for game {i}", full_df[full_df["game_id"] == i])
print(f"{round(100.0 * (present / full_df['game_id'].nunique()), 2)}% of games contain clock data")

## now checking every move
present2 = 0
for i in range(len(full_df)):
    if pd.notna(full_df.iloc[i]["clock_time"]):
        present2 += 1
    else:
        print(f"no clock data for index {i}")
print(f"{round(100.0 * (present2 / full_df.index.nunique()), 2)}% of moves contain clock data")

