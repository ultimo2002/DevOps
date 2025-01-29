import json
import os
import time

from config import STEAMAPI_BASE_URL, STEAMSTORE_BASE_URL, fetch_from_api, APPS_LIST_CACHE_FILE, CACHE_EXPIRATION_TIME

def get_app_details(appid):
    """Fetch details for a specific app (game) from the Steam store API."""
    try:
        data = fetch_from_api(f"{STEAMSTORE_BASE_URL}appdetails?appids={appid}")
        if data and data[str(appid)]["success"]:
            return data[str(appid)]["data"]

    except Exception as e:
        print(f"Error fetching details for appid {appid}: {e}")

    return False

def is_cache_valid(cache_file, expiration_time):
    """Check if the cache file is valid based on its timestamp."""
    if os.path.exists(cache_file):
        cache_timestamp = os.path.getmtime(cache_file)
        current_time = time.time()
        return current_time - cache_timestamp < expiration_time
    return False

def load_cache(cache_file):
    """Load data from the cache file."""
    with open(cache_file, 'r') as cache_file_obj:
        print("Loading app list from cache file...")
        return json.load(cache_file_obj)

def save_cache(cache_file, data):
    """Save data to the cache file."""
    with open(cache_file, 'w') as cache_file_obj:
        print("Saving app list to cache...")
        json.dump(data, cache_file_obj)


def fetch_app_list():
    """Fetch the list of all the apps (games) from the Steam API."""

    # Ensure cache directory exists
    os.makedirs(os.path.dirname(APPS_LIST_CACHE_FILE), exist_ok=True)

    # Check if cache is valid and return from cache if possible
    if is_cache_valid(APPS_LIST_CACHE_FILE, CACHE_EXPIRATION_TIME):
        return load_cache(APPS_LIST_CACHE_FILE)


    print("Fetching app list...")

    # Fetch the app list from the Steam API
    data = fetch_from_api(f"{STEAMAPI_BASE_URL}ISteamApps/GetAppList/v2/")

    if data:
        save_cache(APPS_LIST_CACHE_FILE, data["applist"]["apps"])
        return data["applist"]["apps"]

    return False

def get_app_categories(details):
    """Extract the categories from the app details."""
    if details and details.get("categories"):
        return details["categories"]

    return []

def get_current_player_count(appid):
    """Fetch the current player count for a app (game) from the Steam API."""
    data = fetch_from_api(f"{STEAMAPI_BASE_URL}ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}")

    try:
        if data and data["response"]:
            return int(data["response"]["player_count"])
    except (KeyError, ValueError):
        pass

    return False

if __name__ == "__main__":
    # Fetch and process each app
    app_list = fetch_app_list()

    if not app_list or len(app_list) == 0:
        exit("No games found. Exiting the application.")

    for app in app_list:
        appid = app["appid"]
        name = app["name"]

        # when name is empty, skip to the next app
        if not name:
            continue

        print(f"Processing appid {appid}: {name}")
        details = get_app_details(appid)

        if details:
            categories = get_app_categories(details)
            category_names = ", ".join([cat["description"] for cat in categories])

            # Print data instead of saving to database
            print(f"AppID: {appid}, Name: {name}, Categories: {category_names}")

        # player_count = get_current_player_count(appid)
        # if player_count:
        #     print(f"Player count for {name}: {player_count}")

        # Sleep to prevent rate limits
        time.sleep(0.5)

    print("Done fetching app data.")

