from src.database.database import Database

db = Database()

# Create tables
db.create_champion_metadata_table()
db.create_champion_stats_table()
print("HELLO")

# Write all info to tables -- WORKS PERFECTLY!
# db.write_all_champions_metadata()
# print("DONE WRITING 1")
# db.write_all_champions_stats()
# print("DONE WRITING 2")

# Read all info in tables
metadata = db.get_some_champions_metadata(["Aatrox", "Zilean"])
statdata = db.get_some_champions_stats(["Aatrox", "Zilean"])
print("DONE READING")


def pretty(data, indent=0):
    for d in data:
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))
        print("-------------------------------------------")


pretty(metadata)
print("====================================")
pretty(statdata)


# Close db instance
db.close()
