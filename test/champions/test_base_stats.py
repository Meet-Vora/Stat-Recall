from src.champions.champion import Champion
import requests
from bs4 import BeautifulSoup
# champ = Champion("Aatrox")
response = requests.get("http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items/")
soup = BeautifulSoup(response.text, "html.parser")
links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href != "../" and href.find("msgpack") == -1:
        links.append(href)
    
print(len(links))