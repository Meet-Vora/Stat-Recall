import sqlite3
import requests
import json
import os
from src.database.classes.database import Database


class ChampionDatabase(Database):

    def __init__(self, patch="latest", auto_commit=True):
        super().__init__(patch=patch, auto_commit=auto_commit)

        self.champ_names_path = os.path.join(os.path.dirname(
            __file__), '../../content/champion_names.json')

        self.champion_names = self.__read_all_champions()
        self.base_url += "/champions"

    def __champion_http_request(self, champion_name):
        # url_name = "MonkeyKing" if champion_name == "Wukong" else champion_name
        url = self.base_url + "/" + champion_name + ".json"
        return self._get_http_request(url).json()

    ### Create and write to tables in database ###

    def __read_all_champions(self):
        with open(self.champ_names_path, "r") as file:
            return json.load(file)['champions']

    def drop_champ_metadata_table(self):
        schema = """
        DROP TABLE IF EXISTS champion_metadata

        """
        self._db_execute(schema)

    def drop_champ_base_stats_table(self):
        schema = """
        DROP TABLE IF EXISTS champion_base_stats

        """
        self._db_execute(schema)

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
        self._db_execute(schema)

    def create_champion_base_stats_table(self):
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
        self._db_execute(schema)

    def write_all_champions_metadata(self):
        for champion_name in self.champion_names:
            self.write_champion_metadata(champion_name)

    def write_champion_metadata(self, champion_name):
        response_data = self.__champion_http_request(champion_name)
        insert_command = "INSERT OR REPLACE INTO champion_metadata VALUES (?,?,?,?,?,?,?,?,?)"
        values = [response_data['id'], response_data['key'].lower(), champion_name, response_data['title'],
                  response_data['fullName'], response_data['icon'], response_data['resource'],
                  response_data['attackType'], response_data['adaptiveType']
                  ]

        self._db_execute(insert_command, values)

    def write_all_champions_stats(self):
        for champion_name in self.champion_names:
            self.write_champion_stats(champion_name)

    def write_champion_stats(self, champion_name):
        key = self.__champion_http_request(champion_name)['key'].lower()
        response_data = self.__champion_http_request(champion_name)['stats']
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

            response_data['health']['flat'],
            response_data['health']['percent'],
            response_data['health']['perLevel'],
            response_data['health']['percentPerLevel'],

            response_data['healthRegen']['flat'],
            response_data['healthRegen']['percent'],
            response_data['healthRegen']['perLevel'],
            response_data['healthRegen']['percentPerLevel'],

            response_data['mana']['flat'],
            response_data['mana']['percent'],
            response_data['mana']['perLevel'],
            response_data['mana']['percentPerLevel'],

            response_data['manaRegen']['flat'],
            response_data['manaRegen']['percent'],
            response_data['manaRegen']['perLevel'],
            response_data['manaRegen']['percentPerLevel'],

            response_data['armor']['flat'],
            response_data['armor']['percent'],
            response_data['armor']['perLevel'],
            response_data['armor']['percentPerLevel'],

            response_data['magicResistance']['flat'],
            response_data['magicResistance']['percent'],
            response_data['magicResistance']['perLevel'],
            response_data['magicResistance']['percentPerLevel'],

            response_data['attackDamage']['flat'],
            response_data['attackDamage']['percent'],
            response_data['attackDamage']['perLevel'],
            response_data['attackDamage']['percentPerLevel'],

            response_data['movespeed']['flat'],
            response_data['movespeed']['percent'],
            response_data['movespeed']['perLevel'],
            response_data['movespeed']['percentPerLevel'],

            response_data['acquisitionRadius']['flat'],
            response_data['acquisitionRadius']['percent'],
            response_data['acquisitionRadius']['perLevel'],
            response_data['acquisitionRadius']['percentPerLevel'],

            response_data['selectionRadius']['flat'],
            response_data['selectionRadius']['percent'],
            response_data['selectionRadius']['perLevel'],
            response_data['selectionRadius']['percentPerLevel'],

            response_data['pathingRadius']['flat'],
            response_data['pathingRadius']['percent'],
            response_data['pathingRadius']['perLevel'],
            response_data['pathingRadius']['percentPerLevel'],

            response_data['gameplayRadius']['flat'],
            response_data['gameplayRadius']['percent'],
            response_data['gameplayRadius']['perLevel'],
            response_data['gameplayRadius']['percentPerLevel'],

            response_data['criticalStrikeDamage']['flat'],
            response_data['criticalStrikeDamage']['percent'],
            response_data['criticalStrikeDamage']['perLevel'],
            response_data['criticalStrikeDamage']['percentPerLevel'],

            response_data['criticalStrikeDamageModifier']['flat'],
            response_data['criticalStrikeDamageModifier']['percent'],
            response_data['criticalStrikeDamageModifier']['perLevel'],
            response_data['criticalStrikeDamageModifier']['percentPerLevel'],

            response_data['attackSpeed']['flat'],
            response_data['attackSpeed']['percent'],
            response_data['attackSpeed']['perLevel'],
            response_data['attackSpeed']['percentPerLevel'],

            response_data['attackSpeedRatio']['flat'],
            response_data['attackSpeedRatio']['percent'],
            response_data['attackSpeedRatio']['perLevel'],
            response_data['attackSpeedRatio']['percentPerLevel'],

            response_data['attackCastTime']['flat'],
            response_data['attackCastTime']['percent'],
            response_data['attackCastTime']['perLevel'],
            response_data['attackCastTime']['percentPerLevel'],

            response_data['attackTotalTime']['flat'],
            response_data['attackTotalTime']['percent'],
            response_data['attackTotalTime']['perLevel'],
            response_data['attackTotalTime']['percentPerLevel'],

            response_data['attackDelayOffset']['flat'],
            response_data['attackDelayOffset']['percent'],
            response_data['attackDelayOffset']['perLevel'],
            response_data['attackDelayOffset']['percentPerLevel'],

            response_data['attackRange']['flat'],
            response_data['attackRange']['percent'],
            response_data['attackRange']['perLevel'],
            response_data['attackRange']['percentPerLevel'],

        ]
        self._db_execute(insert_command, values)

    ### Read from tables in database ###

    def get_some_champions_metadata(self, champion_names=[]):
        """
        Return:
        all champion metadata in a python dictionary
        """
        data = []
        if not champion_names:
            champion_names = self.champion_names

        for champion_name in champion_names:
            data += [self.__get_champion_metadata(champion_name)]

        return data

    def __get_champion_metadata(self, champion_name):
        """
        Return:
        champion metadata in a python dictionary
        """
        select_command = "SELECT * FROM champion_metadata WHERE key = ?"
        self._db_execute(select_command, values=[champion_name.lower()])
        entry = self.cursor.fetchall()
        return dict(entry[0])

    def get_some_champions_stats(self, champion_names=[]):
        """
        Return:
        all champion stat data in a python dictionary
        """
        data = []
        if not champion_names:
            champion_names = self.champion_names

        for champion_name in champion_names:
            data += [self.__get_champion_stats(champion_name)]

        return data
        # return self.__open_champion_names_json(read_stats=True)

    def __get_champion_stats(self, champion_name):
        """
        Return:
        champion base stats data in a python dictionary
        """
        select_command = "SELECT * FROM champion_base_stats WHERE key = ?"
        self._db_execute(select_command, values=[champion_name.lower()])
        entry = self.cursor.fetchall()
        return dict(entry[0])

        # self._db_execute(select_command, values=[champion_name.lower()])
        # data = self.cursor.fetchall()
        # print("HERE!!!", data[0])
        # return data[0]
