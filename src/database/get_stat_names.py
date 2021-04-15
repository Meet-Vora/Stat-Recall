"""
Writes all the stats available in of the meraki json file. Must run this script from
the current directory for it to write to content/stat_names.json
"""

import requests
import json

data = requests.get(
    'http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions/Aatrox.json').json()

stat_names = []
for statname in data['stats']:
    for scaletype in data['stats'][statname]:
        stat_names.append((statname + scaletype).lower())

with open("../content/stat_names.json", "w+") as file:
    json.dump({"stats": stat_names}, file)
