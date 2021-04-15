import sqlite3

class Champion:
    def __init__(self, name):
        database = Database()
        champ = database.get_champion(name)

        self.base_stats = #champ.stats

        database.close()

    
