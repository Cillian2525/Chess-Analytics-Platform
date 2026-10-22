import requests
import pandas as pd

## object to store content from api link (link contains monthly games for month of my choosing)
response = requests.get("https://api.chess.com/pub/player/Cillian2525/games/2025/08",
    headers={"User-Agent": "ChessAnalyticsProject hegartycillian04@gmail.com"}) ## user agent prevents 403 response

# print(response.status_code) ## checking status of request

data = response.json() # storing json file

# print("Number of games: ", len(data["games"]))

## getting colnames these tables contain
# df = pd.json_normalize(data["games"])
# print(df.columns)

## checking if each game contains clock data
# pgn = data["games"][0]["pgn"]
# print(pgn) ## inspecting first game pgn

# clock_games = sum(
#     "[%clk" in game["pgn"]
#     for game in data["games"]
# )

# print("Games with clock data:", clock_games)
# print("Total games:", len(data["games"]))
# print("Percentage:", round(clock_games / len(data["games"]) * 100, 2), "%") ## all games have clokc date