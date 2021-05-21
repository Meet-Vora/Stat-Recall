from src.database.classes.champion_database import ChampionDatabase

champ_db = ChampionDatabase()

# Create tables
champ_db.create_champion_metadata_table()
champ_db.create_champion_base_stats_table()

# Write all info to tables -- WORKS PERFECTLY!
# champ_db.write_all_champions_metadata()
# print("DONE WRITING 1")
# champ_db.write_all_champions_stats()
# print("DONE WRITING 2")

# Read all info in tables
metadata = champ_db.get_some_champions_metadata(["Aatrox", "Zilean"])
statdata = champ_db.get_some_champions_stats(["Aatrox", "Zilean"])

print(metadata[0])
print("====================================")
print(statdata[0])

# print("DONE READING")


# def pretty(data, indent=0):
#     for d in data:
#         for key, value in d.items():
#             print('\t' * indent + str(key))
#             if isinstance(value, dict):
#                 pretty(value, indent+1)
#             else:
#                 print('\t' * (indent+1) + str(value))
#         print("-------------------------------------------")


# pretty(metadata)
# pretty(statdata)


# Close champ_db instance
champ_db.close()
