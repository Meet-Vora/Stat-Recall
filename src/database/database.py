import sqlite3
import requests
import json
import os


class Database:

    def __init__(self, patch="latest", auto_commit=True):
        self.patch = patch
        self.auto_commit = auto_commit

        self.database_name = "database.db"
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()

        self.base_url = "http://cdn.merakianalytics.com/riot/lol/resources/{}/en-US".format(
            self.patch)
        self.champ_names_path = os.path.join(os.path.dirname(
            __file__), '../content/champion_names.json')

        self.stat_names_path = os.path.join(os.path.dirname(
            __file__), '../content/stat_names.json')

    def __get_http_request(self, url):
        response = requests.get(url)
        print(url)
        return response

    ### Create and write to tables in database ###
    def __db_execute(self, command, values=[]):
        """
        Private helper method for creating tables
        """
        if not values:
            self.cursor.execute(command)

        self.cursor.executemany(command, values)
        self.conn.commit()

    def drop_champ_metadata_table(self):
        schema = """
        DROP TABLE IF EXISTS champion_metadata

        """
        self.__db_execute(schema)

    def drop_champ_basestat_table(self):
        schema = """
        DROP TABLE IF EXISTS champion_base_stats

        """
        self.__db_execute(schema)

    def create_champion_metadata_table(self):
        schema = """
        CREATE TABLE IF NOT EXISTS champion_metadata
        (
            id INTEGER NOT NULL, 
            key TEXT NOT NULL PRIMARY KEY, 
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            fullName TEXT NOT NULL,
            icon TEXT NOT NULL,
            resource TEXT NOT NULL,
            attackType TEXT NOT NULL,
            adaptiveType TEXT NOT NULL
        )
        """
        self.__db_execute(schema)

    def create_champion_stats_table(self):
        schema = """
        CREATE TABLE IF NOT EXISTS champion_base_stats
        (
            key TEXT NOT NULL,

            health TEXT NOT NULL,
            healthFlat INTEGER NOT NULL,
            healthPercent INTEGER NOT NULL,
            healthPerLevel INTEGER NOT NULL,
            healthPercentPerLevel INTEGER NOT NULL,

            healthRegen TEXT NOT NULL,
            healthRegenFlat INTEGER NOT NULL,
            healthRegenPercent INTEGER NOT NULL,
            healthRegenPerLevel INTEGER NOT NULL,
            healthRegenPercentPerLevel INTEGER NOT NULL,

            mana TEXT NOT NULL,
            manaFlat INTEGER NOT NULL,
            manaPercent INTEGER NOT NULL,
            manaPerLevel INTEGER NOT NULL,
            manaPercentPerLevel INTEGER NOT NULL,
            
            manaRegen TEXT NOT NULL,
            manaRegenFlat INTEGER NOT NULL,
            manaRegenPercent INTEGER NOT NULL,
            manaRegenPerLevel INTEGER NOT NULL,
            manaRegenPercentPerLevel INTEGER NOT NULL,

            armor TEXT NOT NULL,
            armorFlat INTEGER NOT NULL,
            armorPercent INTEGER NOT NULL,
            armorPerLevel INTEGER NOT NULL,
            armorPercentPerLevel INTEGER NOT NULL,

            magicResistance TEXT NOT NULL,
            magicResistanceFlat INTEGER NOT NULL,
            magicResistancePercent INTEGER NOT NULL,
            magicResistancePerLevel INTEGER NOT NULL,
            magicResistancePercentPerLevel INTEGER NOT NULL,

            attackDamage TEXT NOT NULL,
            attackDamageFlat INTEGER NOT NULL,
            attackDamagePercent INTEGER NOT NULL,
            attackDamagePerLevel INTEGER NOT NULL,
            attackDamagePercentPerLevel INTEGER NOT NULL,

            movespeed TEXT NOT NULL,
            movespeedFlat INTEGER NOT NULL,
            movespeedPercent INTEGER NOT NULL,
            movespeedPerLevel INTEGER NOT NULL,
            movespeedPercentPerLevel INTEGER NOT NULL,

            acquisitionRadius TEXT NOT NULL,
            acquisitionRadiusFlat INTEGER NOT NULL,
            acquisitionRadiusPercent INTEGER NOT NULL,
            acquisitionRadiusPerLevel INTEGER NOT NULL,
            acquisitionRadiusPercentPerLevel INTEGER NOT NULL,

            selectionRadius TEXT NOT NULL,
            selectionRadiusFlat INTEGER NOT NULL,
            selectionRadiusPercent INTEGER NOT NULL,
            selectionRadiusPerLevel INTEGER NOT NULL,
            selectionRadiusPercentPerLevel INTEGER NOT NULL,

            pathingRadius TEXT NOT NULL,
            pathingRadiusFlat INTEGER NOT NULL,
            pathingRadiusPercent INTEGER NOT NULL,
            pathingRadiusPerLevel INTEGER NOT NULL,
            pathingRadiusPercentPerLevel INTEGER NOT NULL,

            gameplayRadius TEXT NOT NULL,
            gameplayRadiusFlat INTEGER NOT NULL,
            gameplayRadiusPercent INTEGER NOT NULL,
            gameplayRadiusPerLevel INTEGER NOT NULL,
            gameplayRadiusPercentPerLevel INTEGER NOT NULL,

            criticalStrikeDamage TEXT NOT NULL,
            criticalStrikeDamageFlat INTEGER NOT NULL,
            criticalStrikeDamagePercent INTEGER NOT NULL,
            criticalStrikeDamagePerLevel INTEGER NOT NULL,
            criticalStrikeDamagePercentPerLevel INTEGER NOT NULL,

            criticalStrikeDamageModifier TEXT NOT NULL,
            criticalStrikeDamageModifierFlat INTEGER NOT NULL,
            criticalStrikeDamageModifierPercent INTEGER NOT NULL,
            criticalStrikeDamageModifierPerLevel INTEGER NOT NULL,
            criticalStrikeDamageModifierPercentPerLevel INTEGER NOT NULL,

            attackSpeed TEXT NOT NULL,
            attackSpeedFlat INTEGER NOT NULL,
            attackSpeedPercent INTEGER NOT NULL,
            attackSpeedPerLevel INTEGER NOT NULL,
            attackSpeedPercentPerLevel INTEGER NOT NULL,

            attackSpeedRatio TEXT NOT NULL,
            attackSpeedRatioFlat INTEGER NOT NULL,
            attackSpeedRatioPercent INTEGER NOT NULL,
            attackSpeedRatioPerLevel INTEGER NOT NULL,
            attackSpeedRatioPercentPerLevel INTEGER NOT NULL,

            attackCastTime TEXT NOT NULL,
            attackCastTimeFlat INTEGER NOT NULL,
            attackCastTimePercent INTEGER NOT NULL,
            attackCastTimePerLevel INTEGER NOT NULL,
            attackCastTimePercentPerLevel INTEGER NOT NULL,

            attackTotalTime TEXT NOT NULL,
            attackTotalTimeFlat INTEGER NOT NULL,
            attackTotalTimePercent INTEGER NOT NULL,
            attackTotalTimePerLevel INTEGER NOT NULL,
            attackTotalTimePercentPerLevel INTEGER NOT NULL,

            attackDelayOffset TEXT NOT NULL,
            attackDelayOffsetFlat INTEGER NOT NULL,
            attackDelayOffsetPercent INTEGER NOT NULL,
            attackDelayOffsetPerLevel INTEGER NOT NULL,
            attackDelayOffsetPercentPerLevel INTEGER NOT NULL,

            attackRange TEXT NOT NULL,
            attackRangeFlat INTEGER NOT NULL,
            attackRangePercent INTEGER NOT NULL,
            attackRangePerLevel INTEGER NOT NULL,
            attackRangePercentPerLevel INTEGER NOT NULL,

            FOREIGN KEY(key) REFERENCES champion_metadata(key)
        )
        """
        self.__db_execute(schema)

    def write_all_champion_metadata(self):
        with open(self.champ_names_path, "r") as file:
            champion_names = json.load(file)['champions']
            for champion_name in champion_names:
                self.write_champion_metadata(champion_name)

    def write_champion_metadata(self, champion_name):
        url_name = "MonkeyKing" if champion_name == "Wukong" else champion_name

        url = self.base_url + "/champions/" + url_name + ".json"
        request_data = self.__get_http_request(url).json()
        insert_command = "INSERT INTO champion_metadata VALUES (?,?,?,?,?,?,?,?,?)"
        values = [(request_data['id'], request_data['key'], champion_name, request_data['title'],
                   request_data['fullName'], request_data['icon'], request_data['resource'],
                   request_data['attackType'], request_data['adaptiveType'])]
        self.__db_execute(insert_command, values)

    def write_all_champion_stats(self):
        with open(self.champ_names_path, "r") as file:
            champion_names = json.load(file)['champions']
            for champion_name in champion_names:
                self.write_champion_stats(champion_name)

    def write_champion_stats(self, champion_name):
        url_name = "MonkeyKing" if champion_name == "wukong" else champion_name
        return
        # values = [(request_data['id'], request_data['key'], champion_name, request_data['title'],
        #           request_data['fullName'], request_data['icon'], request_data['resource'],
        #           request_data['attackType'], request_data['adaptiveType'])]
        # self.__db_execute(insert_command, values)

    ### Read from tables in database ###

    def get_all_champion_metadata(self):
        """
        Return:
        all champion metadata in JSON python object
        """
        pass

    def get_all_champion_stats(self):
        """
        Return:
        all champion stat data in JSON python object
        """
        pass

    def get_champion_metadata(self, champion_name):
        """
        Return:
        champion data in JSON python object
        """
        pass

    def get_champion_stats(self, champion_name):
        """
        Return:
        champion data in JSON python object
        """
        pass

    # create_table() method with passed-in schema
    # read_table() method

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    database = Database()
    # database.drop_champ_metadata_table()
    # database.drop_champ_basestat_table()
    # database.create_champion_metadata_table()
    # database.create_champion_stats_table()
    # database.write_all_champion_metadata()
    database.write_all_champion_stats()
    database.close()


data["health"]
data["healthFlat"]
data["healthPercent"]
data["healthPerLevel"]
data["healthPercentPerLevel"]
