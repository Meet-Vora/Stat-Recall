from src.database.database import Database

db = Database()

# Create tables
db.create_champion_metadata_table()
db.create_champion_stats_table()

# Write all info to tables
# db.write_all_champions_metadata()
# db.write_all_champions_stats()

# Read all info in tables
# data = db.get_all_champion_metadata()
data = db.get_champion_metadata("Aatrox")
# print(data)


# Close db instance
db.close()
