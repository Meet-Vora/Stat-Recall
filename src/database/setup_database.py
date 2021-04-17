from src.database.database import Database

db = Database()

# Create tables
db.create_champion_metadata_table()
db.create_champion_stats_table()

# Write all info to tables
db.write_all_champions_stats()

# Close db instance
db.close()
