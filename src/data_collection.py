import requests

#object to store content from api link (link contains monthly games for month of my choosing)
response = requests.get("https://api.chess.com/pub/player/Cillian2525/games/2025/08",
    headers={"User-Agent": "ChessAnalyticsProject hegartycillian04@gmail.com"}) # user agent prevents 403 response

# print(response.status_code) # checking status of request

data = response.json() # storing json file

print("Number of games: ", len(data["games"]))