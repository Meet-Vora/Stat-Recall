import requests
from bs4 import BeautifulSoup
import os
import json


############### Requesting data from ddragon API ###############

ddragon_url = "https://ddragon.leagueoflegends.com/cdn/11.10.1/data/en_US/item.json"
response = requests.get(ddragon_url)
item_json = response.json()['data']
data_lst = []
for item_number in item_json:
    item = item_json[item_number]
    if 'maps' in item and '11' in item['maps'] and item['maps']['11']:
        data = {}
        data['id'] = item_number
        data['name'] = item['name']
        data_lst += [data]

with open(os.path.join(os.path.dirname(__file__), '../../content/ddragon_item_list.json'), "w+") as file:
    json.dump({"items": data_lst}, file)


############### Requesting data from merakianalytics API ###############

# api_base_url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items/"
# base_response = requests.get(api_base_url)
# soup = BeautifulSoup(base_response.text, "html.parser")
# links = []

# # gets all the names of the json files so that you can use them in the request url
# for link in soup.find_all('a'):
#     href = link.get('href')
#     if href != "../" and href.find("msgpack") == -1:
#         links.append(href)

# data_lst = []
# for json_name in links:
#     url = api_base_url + json_name
#     item = requests.get(url).json()
#     if not item['removed']:
#         data = {}
#         data['id'] = item["id"]
#         data['name'] = item["name"]
#         data_lst += [data]

# with open(os.path.join(os.path.dirname(__file__), '../../content/item_list.json'), "w+") as file:
#     json.dump({"items": data_lst}, file)

############### Parsing wiki web page ###############

# wiki_base_url = "https://leagueoflegends.fandom.com/wiki/List_of_items"
# grid_xpath = "/html/body/div[3]/div[7]/div/div[1]/article/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div[3]/div/div"
# wiki_base_response = requests.get(wiki_base_url)
# wiki_soup = BeautifulSoup(wiki_base_response.text, "html.parser")

# all_items_div = wiki_soup.findAll("div", id="item-grid")[1]
# item_types = []
# for dl in all_items_div.findAll("dl"):
#     item_types += [dl.dt.string]

# counter = 0
# data = {}
# for div in all_items_div.findAll("div"):
#     item_names = []
#     if div.ul is not None:
#         for li in div.ul.findAll('li'):
#             if li is not None:
#                 item_names += [li.div.div.a['title']]
#         data[item_types[counter]] = item_names
#         counter += 1

# with open(os.path.join(os.path.dirname(__file__), '../../content/item_list.json'), "w+") as file:
#     json.dump(data, file)
