"""
Writes all the stats available in of the meraki json file. Must run this script from
the current directory for it to write to content/stat_names.json
"""

import requests
import json

data = requests.get(
    'http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions/Aatrox.json').json()

stat_names = []
counter = 0
for statname in data['stats']:
    counter += 1
# for scaletype in data['stats'][statname]:
#     print((statname + scaletype).lower())
#     stat_names.append((statname + scaletype).lower())

print(counter)
# with open("../content/stat_names.json", "w+") as file:
#     json.dump({"stats": stat_names}, file)
