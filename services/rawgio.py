import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")

RAWG_URL = "https://api.rawg.io/api/games"


def search_game(game_name: str):

    if not RAWG_API_KEY:
        raise ValueError("RAWG_API_KEY is missing")

    params = {
        "key": RAWG_API_KEY,
        "search": game_name,
        "page_size": 5
    }

    response = requests.get(RAWG_URL, params=params, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    results = data.get("results", [])

    if not results:
        return None

    return results

def get_game_details(rawg_id: int):

    if not RAWG_API_KEY:
        raise ValueError("RAWG_API_KEY is missing")

    url = f"https://api.rawg.io/api/games/{rawg_id}"

    params = {
        "key": RAWG_API_KEY
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return None

    return response.json()