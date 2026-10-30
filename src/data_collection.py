import requests
import pandas as pd

##### VARIABLES #####

usernames = ["SOK1954", "HASHEM_NAjd", "GaLaXy14112191014", "sync7122", "Cillian2525"]
months = [1,2,3,4,5,6,7,8,9,10,11,12]
years = [2026]

##### FUNCTIONS #####

## function to retrieve content from api link (link contains monthly games for month of my choosing)
def fetch_games(username, year, month):
    response = requests.get(f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}",
        headers={"User-Agent": "ChessAnalyticsProject hegartycillian04@gmail.com"}) ## user agent prevents 403 response
    return response.json() # storing json file

# function to filter fetched games to only include rapid time classes (returns games, not original fetched data)
def rapid_games(data):
    rapid_games = []

    for game in data["games"]:
        if game["time_class"] == "rapid":
            rapid_games.append(game)
    
    return rapid_games

## loops thrugh each player and gets data for that months games
#for username in usernames:
#    print(fetch_games(username))

# print(response.status_code) ## checking status of request

## getting colnames these tables contain
# df = pd.json_normalize(data["games"])
# print(df.columns)

## check what percent of games contain clock data
def clock_check(data):

    if len(data["games"]) == 0:
        print("No games found for this month.")
        return
    
    clock_games = sum(
        "[%clk" in game["pgn"]
        for game in data["games"]
    )

    print("Games with clock data:", clock_games)
    print("Total games:", len(data["games"]))
    print("Percentage:", round(clock_games / len(data["games"]) * 100, 2), "%")

# print total games per username as well as clock data presence rate (for chosen period)
#for username in usernames:
    print(username)
    clock_check(fetch_games(username, 2026, 5))
    print("\t")

# function to find average rating of each user for that time period (rapid games only)
def get_rapid_rating(username, year, month):
    data = fetch_games(username, year, month)
    rapid_data = rapid_games(data)

    ratings = []

    for game in rapid_data:
        if game["white"]["username"].lower() == username.lower():
            ratings.append(game["white"]["rating"])
        elif game["black"]["username"].lower() == username.lower():
            ratings.append(game["black"]["rating"])
    
    if len(ratings) == 0:
        print(username, "No rapid games found")
        return
    
    print(username, round(sum(ratings) / len(ratings)))

## prints average rapid ratings for chosen every month from the start of 2024 (not labelled)
#for username in usernames:
    for year in years:
        for month in months:
            get_rapid_rating(username, year, month)
    

## funciton to save all rapid games from chosen months, years and user and store in all_games
## takes in lists
def fetch_all_rapid_games(usernames, years, months):
    all_games = {}

    for username in usernames:
        all_games[username] = []

    for username in usernames:
        for year in years:
            for month in months:
                data = fetch_games(username, year, month)
                all_games[username].extend(rapid_games(data))
    
    return all_games

##### STORING COLLECTED RAPID GAMES #####
import json

games = fetch_all_rapid_games(usernames, years, months)

with open("data/raw/rapid_games.json", "w") as f: # w for writing a file (creates or overwrites)
    json.dump(games, f)