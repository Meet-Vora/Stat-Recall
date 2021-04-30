from src.database.database import Database

db = Database()

# Create tables
db.create_champion_metadata_table()
db.create_champion_stats_table()
print("HELLO")

# Write all info to tables -- WORKS PERFECTLY!
# db.write_all_champions_metadata()
# print("DONE WRITING 1")
db.write_all_champions_stats()
print("DONE WRITING 2")

# Read all info in tables
metadata = db.get_champion_metadata("Aatrox")
statdata = db.get_champion_stats("Aatrox")
print("DONE READING")


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


pretty(metadata)
print("====================================")
pretty(statdata)


# Close db instance
db.close()
