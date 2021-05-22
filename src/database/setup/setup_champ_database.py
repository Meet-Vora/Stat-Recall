from src.database.classes.champion_database import ChampionDatabase

champ_db = ChampionDatabase()


# Drop table(s)
# champ_db.drop_champ_metadata_table()
# champ_db.drop_champ_base_stats_table()

# Create tables
# champ_db.create_champion_metadata_table()
# champ_db.create_champion_base_stats_table()

# Write all info to tables
champ_db.write_all_champions_metadata()
champ_db.write_all_champions_base_stats()

# Read all info in tables
# metadata = champ_db.get_some_champions_metadata(["Aatrox", "Zilean"])
# statdata = champ_db.get_some_champions_stats(["Aatrox", "Zilean"])


# Close champ_db instance
champ_db.close()
