from copy import deepcopy
from src.database.database import Database
# from itemslots import Itemslots
# from item import Item

class Champion: 
    def __init__(self, champion_name):
        db = Database()
        self.metadata = db.get_some_champions_metadata([champion_name])
        self.base_stats = db.get_some_champions_stats([champion_name])
        self.current_stats = deepcopy(self.base_stats)
