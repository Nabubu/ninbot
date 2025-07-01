import json

def load_games(region):
    with open("data/games.json", "r", encoding="utf-8") as f:
        all_games = json.load(f)
    return [g for g in all_games if g["region"].upper() == region.upper()]

def find_combination(balance, games):
    games_sorted = sorted(games, key=lambda g: g["price"], reverse=True)
    result = []
    total = 0.0

    for game in games_sorted:
        if total + game["price"] <= balance:
            result.append(game)
            total += game["price"]

    leftover = round(balance - total, 2)
    return result, leftover

def suggest_topup(balance, games, topup_options=[10, 20, 35, 45, 50, 70, 100]):
    for amount in topup_options:
        new_balance = balance + amount
        result, leftover = find_combination(new_balance, games)
        if leftover == 0:
            return amount, result
    return None, []