"""
Writes all the names of the champions in league of legends to a json file. Must run this script from
the current directory for it to write to content/champion_names.json 
"""

import requests
import json
import os

data = requests.get(
    'http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json').json()

champion_names = []
for champ in data:
    # if champ == "MonkeyKing":
    #     champ = "Wukong"
    champion_names += [champ]
    # champion_names += [data[champ]['name']]

with open(os.path.join(os.path.dirname(
        __file__), '../../content/champion_names.json'), "w+") as file:
    json.dump({"champions": champion_names}, file)
