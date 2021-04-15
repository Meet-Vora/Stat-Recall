from database import Database
from itemslots import Itemslots
from item import Item

class Champion: 
    def __init__(self, champion_name):
        database_instance = Database()

        self.metadata = db.get_champion_metadata
        self.basestats = db.get_champion_stats
        self.itemslots = ItemSlots()


         