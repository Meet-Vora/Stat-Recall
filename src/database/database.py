import sqlite3
import requests
import json
import os


class Database:

    def __init__(self, patch="latest", auto_commit=True):
        self.patch = patch
        self.auto_commit = auto_commit

        # self.database_name = "database.db"
        self.database_name = os.path.join(os.path.dirname(
            __file__), './database.db')
        self.conn = sqlite3.connect(self.database_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.base_url = "http://cdn.merakianalytics.com/riot/lol/resources/{}/en-US".format(
            self.patch)
        self.champ_names_path = os.path.join(os.path.dirname(
            __file__), '../content/champion_names.json')

        self.stat_names_path = os.path.join(os.path.dirname(
            __file__), '../content/stat_names.json')

    def __get_http_request(self, url):
        return requests.get(url)

    def __champion_http_request(self, champion_name):
        # url_name = "MonkeyKing" if champion_name == "Wukong" else champion_name
        url = self.base_url + "/champions/" + url_name + ".json"
        return self.__get_http_request(url).json()

    ### Create and write to tables in database ###
    def __db_execute(self, command, values=[]):
        """
        Private helper method for creating tables
        """
        # if not values:
        # elif len(values) == 1:
        #     self.cursor.execute(command, values)
        # else:
        #     self.cursor.executemany(command, values)

        self.cursor.execute(command, values)
        self.conn.commit()

    def __write_champion_names_json(self, write_metadata=False, write_stats=False):
        with open(self.champ_names_path, "r") as file:
            champion_names = json.load(file)['champions']
            for champion_name in champion_names:
                if write_metadata:
                    self.write_champion_metadata(champion_name)
                if write_stats:
                    self.write_champion_stats(champion_name)

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
        self.__write_champion_names_json(write_metadata=True)

    def write_champion_metadata(self, champion_name):
        request_data = self.__champion_http_request(champion_name)
        insert_command = "INSERT OR REPLACE INTO champion_metadata VALUES (?,?,?,?,?,?,?,?,?)"
        values = [request_data['id'], request_data['key'].lower(), champion_name, request_data['title'],
                  request_data['fullName'], request_data['icon'], request_data['resource'],
                  request_data['attackType'], request_data['adaptiveType']
                  ]

        self.__db_execute(insert_command, values)

    def write_all_champions_stats(self):
        self.__write_champion_names_json(write_stats=True)

    def write_champion_stats(self, champion_name):
        key = self.__champion_http_request(champion_name)['key']
        request_data = self.__champion_http_request(champion_name)['stats']
        insert_command = """INSERT OR REPLACE INTO champion_base_stats VALUES
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
            ?,?,?,?
        )
        """
        values = [

            key,

            request_data['health']['flat'],
            request_data['health']['percent'],
            request_data['health']['perLevel'],
            request_data['health']['percentPerLevel'],

            request_data['healthRegen']['flat'],
            request_data['healthRegen']['percent'],
            request_data['healthRegen']['perLevel'],
            request_data['healthRegen']['percentPerLevel'],

            request_data['mana']['flat'],
            request_data['mana']['percent'],
            request_data['mana']['perLevel'],
            request_data['mana']['percentPerLevel'],

            request_data['manaRegen']['flat'],
            request_data['manaRegen']['percent'],
            request_data['manaRegen']['perLevel'],
            request_data['manaRegen']['percentPerLevel'],

            request_data['armor']['flat'],
            request_data['armor']['percent'],
            request_data['armor']['perLevel'],
            request_data['armor']['percentPerLevel'],

            request_data['magicResistance']['flat'],
            request_data['magicResistance']['percent'],
            request_data['magicResistance']['perLevel'],
            request_data['magicResistance']['percentPerLevel'],

            request_data['attackDamage']['flat'],
            request_data['attackDamage']['percent'],
            request_data['attackDamage']['perLevel'],
            request_data['attackDamage']['percentPerLevel'],

            request_data['movespeed']['flat'],
            request_data['movespeed']['percent'],
            request_data['movespeed']['perLevel'],
            request_data['movespeed']['percentPerLevel'],

            request_data['acquisitionRadius']['flat'],
            request_data['acquisitionRadius']['percent'],
            request_data['acquisitionRadius']['perLevel'],
            request_data['acquisitionRadius']['percentPerLevel'],

            request_data['selectionRadius']['flat'],
            request_data['selectionRadius']['percent'],
            request_data['selectionRadius']['perLevel'],
            request_data['selectionRadius']['percentPerLevel'],

            request_data['pathingRadius']['flat'],
            request_data['pathingRadius']['percent'],
            request_data['pathingRadius']['perLevel'],
            request_data['pathingRadius']['percentPerLevel'],

            request_data['gameplayRadius']['flat'],
            request_data['gameplayRadius']['percent'],
            request_data['gameplayRadius']['perLevel'],
            request_data['gameplayRadius']['percentPerLevel'],

            request_data['criticalStrikeDamage']['flat'],
            request_data['criticalStrikeDamage']['percent'],
            request_data['criticalStrikeDamage']['perLevel'],
            request_data['criticalStrikeDamage']['percentPerLevel'],

            request_data['criticalStrikeDamageModifier']['flat'],
            request_data['criticalStrikeDamageModifier']['percent'],
            request_data['criticalStrikeDamageModifier']['perLevel'],
            request_data['criticalStrikeDamageModifier']['percentPerLevel'],

            request_data['attackSpeed']['flat'],
            request_data['attackSpeed']['percent'],
            request_data['attackSpeed']['perLevel'],
            request_data['attackSpeed']['percentPerLevel'],

            request_data['attackSpeedRatio']['flat'],
            request_data['attackSpeedRatio']['percent'],
            request_data['attackSpeedRatio']['perLevel'],
            request_data['attackSpeedRatio']['percentPerLevel'],

            request_data['attackCastTime']['flat'],
            request_data['attackCastTime']['percent'],
            request_data['attackCastTime']['perLevel'],
            request_data['attackCastTime']['percentPerLevel'],

            request_data['attackTotalTime']['flat'],
            request_data['attackTotalTime']['percent'],
            request_data['attackTotalTime']['perLevel'],
            request_data['attackTotalTime']['percentPerLevel'],

            request_data['attackDelayOffset']['flat'],
            request_data['attackDelayOffset']['percent'],
            request_data['attackDelayOffset']['perLevel'],
            request_data['attackDelayOffset']['percentPerLevel'],

            request_data['attackRange']['flat'],
            request_data['attackRange']['percent'],
            request_data['attackRange']['perLevel'],
            request_data['attackRange']['percentPerLevel'],

        ]
        self.__db_execute(insert_command, values)

    ### Read from tables in database ###

    def get_some_champion_metadata(self, champions=[]):
        """
        Return:
        all champion metadata in a python dictionary
        """
        pass

    def get_some_champion_stats(self, champions=[]):
        """
        Return:
        all champion stat data in a python dictionary
        """
        data = {}
        if not champions:
            champions =
        # return self.__open_champion_names_json(read_stats=True)

    def get_champion_metadata(self, champion_name):
        """
        Return:
        champion metadata in a python dictionary
        """
        select_command = "SELECT * FROM champion_metadata WHERE key = ?"
        self.__db_execute(select_command, values=[champion_name.lower()])
        data = self.cursor.fetchall()
        return data[0]

    def get_champion_stats(self, champion_name):
        """
        Return:
        champion base stats data in a python dictionary
        """

    def close(self):
        self.conn.close()


# if __name__ == '__main__':
#     database = Database()
#     # database.drop_champ_metadata_table()
#     # database.drop_champ_basestat_table()
#     # database.create_champion_metadata_table()
#     # database.create_champion_stats_table()
#     # database.write_all_champion_metadata()
#     database.write_all_champion_stats()
#     database.close()
