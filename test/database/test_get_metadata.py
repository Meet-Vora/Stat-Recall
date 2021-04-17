import sqlite3
from src.database.database import Database

db = Database()
db.create_champion_metadata_table()
db.write_all_champions_metadata()
db.get_champion_metadata("Aatrox")
db.close()

# conn = sqlite3.connect('../src/database/database.py')


# select_command = "SELECT * FROM champion_metadata WHERE key=?"
# self.__db_execute(select_command, [champion_name])
# data = self.cursor.fetchall()
# print(data)
