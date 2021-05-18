import requests
from bs4 import BeautifulSoup
import os
import json

base_url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items/"
base_response = requests.get(base_url)
soup = BeautifulSoup(base_response.text, "html.parser")
links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href != "../" and href.find("msgpack") == -1:
        links.append(href)
        
data_lst = []
for json_name in links:
    url = base_url + json_name
    item = requests.get(url).json()
    data = {}
    data['id'] = item["id"]
    data['name'] = item["name"]
    data_lst += [data]

with open(os.path.join(os.path.dirname(__file__), '../../content/item_list.json'), "w+") as file:
    json.dump({"items": data_lst}, file)
    