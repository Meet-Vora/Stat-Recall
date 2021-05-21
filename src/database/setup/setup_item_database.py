from src.database.classes.item_database import ItemDatabase

item_db = ItemDatabase()

# Drop table(s)
# item_db.drop_item_metadata_table()
# item_db.drop_item_base_stats_table()

# Create tables
item_db.create_item_metadata_table()
item_db.create_item_base_stats_table()

# Write all info to tables -- WORKS PERFECTLY!
# item_db.write_all_items_metadata()
item_db.write_all_items_base_stats()

# Read all info in tables
# metadata = item_db.get_some_champions_metadata(["Aatrox", "Zilean"])
# statdata = item_db.get_some_champions_stats(["Aatrox", "Zilean"])

# Close item_db instance
item_db.close()
