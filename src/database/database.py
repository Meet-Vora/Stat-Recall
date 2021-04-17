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
        return requests.get(url)

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

            healthFlat INTEGER NOT NULL,
            healthPercent INTEGER NOT NULL,
            healthPerLevel INTEGER NOT NULL,
            healthPercentPerLevel INTEGER NOT NULL,

            healthRegenFlat INTEGER NOT NULL,
            healthRegenPercent INTEGER NOT NULL,
            healthRegenPerLevel INTEGER NOT NULL,
            healthRegenPercentPerLevel INTEGER NOT NULL,

            manaFlat INTEGER NOT NULL,
            manaPercent INTEGER NOT NULL,
            manaPerLevel INTEGER NOT NULL,
            manaPercentPerLevel INTEGER NOT NULL,
            
            manaRegenFlat INTEGER NOT NULL,
            manaRegenPercent INTEGER NOT NULL,
            manaRegenPerLevel INTEGER NOT NULL,
            manaRegenPercentPerLevel INTEGER NOT NULL,

            armorFlat INTEGER NOT NULL,
            armorPercent INTEGER NOT NULL,
            armorPerLevel INTEGER NOT NULL,
            armorPercentPerLevel INTEGER NOT NULL,

            magicResistanceFlat INTEGER NOT NULL,
            magicResistancePercent INTEGER NOT NULL,
            magicResistancePerLevel INTEGER NOT NULL,
            magicResistancePercentPerLevel INTEGER NOT NULL,

            attackDamageFlat INTEGER NOT NULL,
            attackDamagePercent INTEGER NOT NULL,
            attackDamagePerLevel INTEGER NOT NULL,
            attackDamagePercentPerLevel INTEGER NOT NULL,

            movespeedFlat INTEGER NOT NULL,
            movespeedPercent INTEGER NOT NULL,
            movespeedPerLevel INTEGER NOT NULL,
            movespeedPercentPerLevel INTEGER NOT NULL,

            acquisitionRadiusFlat INTEGER NOT NULL,
            acquisitionRadiusPercent INTEGER NOT NULL,
            acquisitionRadiusPerLevel INTEGER NOT NULL,
            acquisitionRadiusPercentPerLevel INTEGER NOT NULL,

            selectionRadiusFlat INTEGER NOT NULL,
            selectionRadiusPercent INTEGER NOT NULL,
            selectionRadiusPerLevel INTEGER NOT NULL,
            selectionRadiusPercentPerLevel INTEGER NOT NULL,

            pathingRadiusFlat INTEGER NOT NULL,
            pathingRadiusPercent INTEGER NOT NULL,
            pathingRadiusPerLevel INTEGER NOT NULL,
            pathingRadiusPercentPerLevel INTEGER NOT NULL,

            gameplayRadiusFlat INTEGER NOT NULL,
            gameplayRadiusPercent INTEGER NOT NULL,
            gameplayRadiusPerLevel INTEGER NOT NULL,
            gameplayRadiusPercentPerLevel INTEGER NOT NULL,

            criticalStrikeDamageFlat INTEGER NOT NULL,
            criticalStrikeDamagePercent INTEGER NOT NULL,
            criticalStrikeDamagePerLevel INTEGER NOT NULL,
            criticalStrikeDamagePercentPerLevel INTEGER NOT NULL,

            criticalStrikeDamageModifierFlat INTEGER NOT NULL,
            criticalStrikeDamageModifierPercent INTEGER NOT NULL,
            criticalStrikeDamageModifierPerLevel INTEGER NOT NULL,
            criticalStrikeDamageModifierPercentPerLevel INTEGER NOT NULL,

            attackSpeedFlat INTEGER NOT NULL,
            attackSpeedPercent INTEGER NOT NULL,
            attackSpeedPerLevel INTEGER NOT NULL,
            attackSpeedPercentPerLevel INTEGER NOT NULL,

            attackSpeedRatioFlat INTEGER NOT NULL,
            attackSpeedRatioPercent INTEGER NOT NULL,
            attackSpeedRatioPerLevel INTEGER NOT NULL,
            attackSpeedRatioPercentPerLevel INTEGER NOT NULL,

            attackCastTimeFlat INTEGER NOT NULL,
            attackCastTimePercent INTEGER NOT NULL,
            attackCastTimePerLevel INTEGER NOT NULL,
            attackCastTimePercentPerLevel INTEGER NOT NULL,

            attackTotalTimeFlat INTEGER NOT NULL,
            attackTotalTimePercent INTEGER NOT NULL,
            attackTotalTimePerLevel INTEGER NOT NULL,
            attackTotalTimePercentPerLevel INTEGER NOT NULL,

            attackDelayOffsetFlat INTEGER NOT NULL,
            attackDelayOffsetPercent INTEGER NOT NULL,
            attackDelayOffsetPerLevel INTEGER NOT NULL,
            attackDelayOffsetPercentPerLevel INTEGER NOT NULL,

            attackRangeFlat INTEGER NOT NULL,
            attackRangePercent INTEGER NOT NULL,
            attackRangePerLevel INTEGER NOT NULL,
            attackRangePercentPerLevel INTEGER NOT NULL,

            FOREIGN KEY(key) REFERENCES champion_metadata(key)
        )
        """
        self.__db_execute(schema)

    def write_all_champions_metadata(self):
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

    def write_all_champions_stats(self):
        with open(self.champ_names_path, "r") as file:
            champion_names = json.load(file)['champions']
            for champion_name in champion_names:
                self.write_champion_stats(champion_name)

    def write_champion_stats(self, champion_name):
        url = self.base_url + "/champions/" + champion_name + ".json"
        request_data = self.__get_http_request(url).json()['stats']
        insert_command = """INSERT INTO champion_metadata VALUES 
        (
            ?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
        ) 
        ON DUPLICATE KEY UPDATE
        """
        values = [

            request_data['healthFlat'],
            request_data['healthPercent'],
            request_data['healthPerLevel'],
            request_data['healthPercentPerLevel'],

            request_data['healthRegenFlat'],
            request_data['healthRegenPercent'],
            request_data['healthRegenPerLevel'],
            request_data['healthRegenPercentPerLevel'],

            request_data['manaFlat'],
            request_data['manaPercent'],
            request_data['manaPerLevel'],
            request_data['manaPercentPerLevel'],

            request_data['manaRegenFlat'],
            request_data['manaRegenPercent'],
            request_data['manaRegenPerLevel'],
            request_data['manaRegenPercentPerLevel'],

            request_data['armorFlat'],
            request_data['armorPercent'],
            request_data['armorPerLevel'],
            request_data['armorPercentPerLevel'],

            request_data['magicResistanceFlat'],
            request_data['magicResistancePercent'],
            request_data['magicResistancePerLevel'],
            request_data['magicResistancePercentPerLevel'],

            request_data['attackDamageFlat'],
            request_data['attackDamagePercent'],
            request_data['attackDamagePerLevel'],
            request_data['attackDamagePercentPerLevel'],

            request_data['movespeedFlat'],
            request_data['movespeedPercent'],
            request_data['movespeedPerLevel'],
            request_data['movespeedPercentPerLevel'],

            request_data['acquisitionRadiusFlat'],
            request_data['acquisitionRadiusPercent'],
            request_data['acquisitionRadiusPerLevel'],
            request_data['acquisitionRadiusPercentPerLevel'],

            request_data['selectionRadiusFlat'],
            request_data['selectionRadiusPercent'],
            request_data['selectionRadiusPerLevel'],
            request_data['selectionRadiusPercentPerLevel'],

            request_data['pathingRadiusFlat'],
            request_data['pathingRadiusPercent'],
            request_data['pathingRadiusPerLevel'],
            request_data['pathingRadiusPercentPerLevel'],

            request_data['gameplayRadiusFlat'],
            request_data['gameplayRadiusPercent'],
            request_data['gameplayRadiusPerLevel'],
            request_data['gameplayRadiusPercentPerLevel'],

            request_data['criticalStrikeDamageFlat'],
            request_data['criticalStrikeDamagePercent'],
            request_data['criticalStrikeDamagePerLevel'],
            request_data['criticalStrikeDamagePercentPerLevel'],

            request_data['criticalStrikeDamageModifierFlat'],
            request_data['criticalStrikeDamageModifierPercent'],
            request_data['criticalStrikeDamageModifierPerLevel'],
            request_data['criticalStrikeDamageModifierPercentPerLevel'],

            request_data['attackSpeedFlat'],
            request_data['attackSpeedPercent'],
            request_data['attackSpeedPerLevel'],
            request_data['attackSpeedPercentPerLevel'],

            request_data['attackSpeedRatioFlat'],
            request_data['attackSpeedRatioPercent'],
            request_data['attackSpeedRatioPerLevel'],
            request_data['attackSpeedRatioPercentPerLevel'],

            request_data['attackCastTimeFlat'],
            request_data['attackCastTimePercent'],
            request_data['attackCastTimePerLevel'],
            request_data['attackCastTimePercentPerLevel'],

            request_data['attackTotalTimeFlat'],
            request_data['attackTotalTimePercent'],
            request_data['attackTotalTimePerLevel'],
            request_data['attackTotalTimePercentPerLevel'],

            request_data['attackDelayOffsetFlat'],
            request_data['attackDelayOffsetPercent'],
            request_data['attackDelayOffsetPerLevel'],
            request_data['attackDelayOffsetPercentPerLevel'],

            request_data['attackRangeFlat'],
            request_data['attackRangePercent'],
            request_data['attackRangePerLevel'],
            request_data['attackRangePercentPerLevel'],

        ]
        self.__db_execute(insert_command, values)

    ### Read from tables in database ###

    def get_all_champion_metadata(self):
        """
        Return:
        all champion metadata in a python dictionary
        """
        pass

    def get_all_champion_stats(self):
        """
        Return:
        all champion stat data in a python dictionary
        """
        pass

    def get_champion_metadata(self, champion_name):
        """
        Return:
        champion data in a python dictionary
        """
        pass

    def get_champion_stats(self, champion_name):
        """
        Return:
        champion data in a python dictionary
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
