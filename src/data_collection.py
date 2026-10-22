import requests
import pandas as pd

usernames = ["SOK1954", "HASHEM_NAjd", "GaLaXy14112191014", "sync7122", "Cillian2525"]

## function to retrieve content from api link (link contains monthly games for month of my choosing)
def fetch_games(username):
    response = requests.get(f"https://api.chess.com/pub/player/{username}/games/2026/09",
        headers={"User-Agent": "ChessAnalyticsProject hegartycillian04@gmail.com"}) ## user agent prevents 403 response
    return response.json() # storing json file

## loops thrugh each player and gets data for that months games
#for username in usernames:
#    print(fetch_games(username))

# print(response.status_code) ## checking status of request

## getting colnames these tables contain
# df = pd.json_normalize(data["games"])
# print(df.columns)

## check what percent of games contain clock data
def clock_check(data):
    clock_games = sum(
        "[%clk" in game["pgn"]
        for game in data["games"]
    )

    print("Games with clock data:", clock_games)
    print("Total games:", len(data["games"]))
    print("Percentage:", round(clock_games / len(data["games"]) * 100, 2), "%")

for username in usernames:
    print(username)
    clock_check(fetch_games(username))
    print("\t")