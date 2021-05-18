import json
import requests
import os

response = requests.get("http://static.developer.riotgames.com/docs/lol/maps.json")
with open(os.path.join(os.path.dirname(__file__), '../../content/maps.json'), "w+") as file:
    json.dump({"maps": response.json()}, file)
