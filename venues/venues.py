import requests
import json
import re
import logging
from typing import List, Dict, TypeVar, Any

T = TypeVar("T", str, List[str])
DEFAULT_USERS_URL = "https://gist.githubusercontent.com/benjambles/ea36b76bc5d8ff09a51def54f6ebd0cb/raw/ee1d0c16eaf373cccadd3d5604a1e0ea307b2ca0/users.json"
DEFAULT_VENUES_URL = "https://gist.githubusercontent.com/benjambles/ea36b76bc5d8ff09a51def54f6ebd0cb/raw/ee1d0c16eaf373cccadd3d5604a1e0ea307b2ca0/venues.json"


def get_compatible_venues(
        user_list: T,
        users_url: str = DEFAULT_USERS_URL,
        venues_url: str = DEFAULT_VENUES_URL) -> Dict[str, Any]:

    user_list = check_user_list(user_list)
    users = parse_json_users(_get_json_from_url(users_url))
    venues = parse_json_venues(_get_json_from_url(venues_url))

    users = filter_users(user_list, users)

    venues_check = check_venues(users, venues)
    logging.debug(f"Output: {venues_check}")
    return venues_check


def setup_logging(log_level: str = "ERROR"):
    root = logging.getLogger()
    if root.handlers:
        for h in root.handlers:
            root.removeHandler(h)
    logging.basicConfig(
        format=
        "[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s]   %(message)s",
        level=log_level)


def _get_json_from_url(url: str) -> List[Dict[str, T]]:
    try:
        logging.info(f"Fetching data from {url}")
        response = json.loads(requests.get(url).text)
    except Exception as e:
        logging.error("Unable to get url: {url}")
        raise e
    return response


def _normalize_string(x: str) -> str:
    # Removes unwanted spaces
    # Converts strings to Title Case
    return re.sub(r"\s+", " ", x.strip()).title()


# Converts user name to dict key and normalizes user preferences
def parse_json_users(
        users_response: List[Dict[str, T]]) -> Dict[str, Dict[str, T]]:
    users = {}
    for user in users_response:
        users[_normalize_string(user["name"])] = {
            "wont_eat": [_normalize_string(food) for food in user["wont_eat"]],
            "drinks": [_normalize_string(drink) for drink in user["drinks"]]
        }
    return users


# Converts venues name to dict key and normalizes venues menu
def parse_json_venues(
        venues_response: List[Dict[str, T]]) -> Dict[str, Dict[str, T]]:
    venues = {}
    for venue in venues_response:
        venues[_normalize_string(venue["name"])] = {
            "food": [_normalize_string(food) for food in venue["food"]],
            "drinks": [_normalize_string(drink) for drink in venue["drinks"]]
        }
    return venues


# Selects only preferences of the selected users
def filter_users(user_list: List[str],
                 users: Dict[str, Dict[str, T]]) -> Dict[str, Dict[str, T]]:
    filtered_users = {}
    for user in user_list:
        user = _normalize_string(user)
        try:
            filtered_users[user] = users[user]
        except KeyError as e:
            logging.error((f"Preferences of user {user} were not found."))
            raise e

    return filtered_users


def check_user_list(user_list: T) -> List[str]:
    if isinstance(user_list, list) and all(
            isinstance(user, str) for user in user_list):
        return user_list
    elif isinstance(user_list, str):
        return list(user_list)
    else:
        logging.error(
            "A list containing user names or a single name was expected as input."
        )
        raise TypeError("Input must be a list of strings or a string.")


def _is_valid_food_menu(food_menu: List[str],
                        food_restrictions: List[str]) -> bool:
    if set(food_menu).difference(set(food_restrictions)):
        return True
    return False


def _is_valid_drink_menu(drink_menu: List[str],
                         drinks_approved: List[str]) -> bool:
    if set(drink_menu).intersection(set(drinks_approved)):
        return True
    return False


def check_venues(users: Dict[str, Dict[str, T]],
                 venues: Dict[str, Dict[str, T]]) -> Dict[str, Any]:
    places_to_visit = []
    places_to_avoid = []

    for venue_name, venue_menu in venues.items():
        venue_approved = True
        reasons_to_avoid = []

        for user_name, user_preferences in users.items():
            if not _is_valid_food_menu(
                    food_menu=venue_menu["food"],
                    food_restrictions=user_preferences["wont_eat"]):
                venue_approved = False
                reasons_to_avoid.append(
                    f"There is nothing for {user_name} to eat.")
            if not _is_valid_drink_menu(
                    drink_menu=venue_menu["drinks"],
                    drinks_approved=user_preferences["drinks"]):
                venue_approved = False
                reasons_to_avoid.append(
                    f"There is nothing for {user_name} to drink.")

        if venue_approved:
            places_to_visit.append(venue_name)
        else:
            places_to_avoid.append({
                "name": venue_name,
                "reason": reasons_to_avoid
            })

    return {
        "places_to_visit": places_to_visit,
        "places_to_avoid": places_to_avoid
    }


if __name__ == "__main__":
    get_compatible_venues(user_list=["Karol Drewno", "Wen Li"])
