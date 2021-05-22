import sqlite3
import requests
import json
import os
from src.database.classes.database import Database


class ItemDatabase(Database):
    def __init__(self, patch="latest", auto_commit=True):
        super().__init__(patch=patch, auto_commit=auto_commit)

        self.items_file_path = os.path.join(os.path.dirname(
            __file__), '../../content/ddragon_item_list.json')

        self.base_url += "/items"
        self.items = self.__read_all_items()

    def __read_all_items(self):
        with open(self.items_file_path, "r") as file:
            return json.load(file)['items']

    def __item_http_request(self, item_number):
        # url_name = "MonkeyKing" if champion_name == "Wukong" else champion_name
        url = self.base_url + "/" + str(item_number) + ".json"
        return self._get_http_request(url).json()

    def drop_item_metadata_table(self):
        schema = "DROP TABLE IF EXISTS item_metadata"
        self._db_execute(schema)

    def drop_item_base_stats_table(self):
        schema = "DROP TABLE IF EXISTS item_base_stats"
        self._db_execute(schema)

    def create_item_metadata_table(self):
        schema = """
        CREATE TABLE IF NOT EXISTS item_metadata
        (
            id INTEGER NOT NULL PRIMARY KEY,

            name TEXT NOT NULL,
            requiredChampion TEXT NOT NULL,
            requiredAlly TEXT NOT NULL,

            goldTotal INTEGER NOT NULL,
            goldSell INTEGER NOT NULL,
            purchasable INTEGER NOT NULL CHECK (purchasable IN (0, 1))
        )
        """
        self._db_execute(schema)

    def create_item_base_stats_table(self):
        schema = """
        CREATE TABLE IF NOT EXISTS item_base_stats
        (
            id INTEGER NOT NULL PRIMARY KEY,

            abilityPowerFlat INTEGER NOT NULL,
            abilityPowerPercent INTEGER NOT NULL,
            abilityPowerPerLevel INTEGER NOT NULL,
            abilityPowerPercentPerLevel INTEGER NOT NULL,
            abilityPowerPercentBase INTEGER NOT NULL,
            abilityPowerPercentBonus INTEGER NOT NULL,

            armorFlat INTEGER NOT NULL,
            armorPercent INTEGER NOT NULL,
            armorPerLevel INTEGER NOT NULL,
            armorPercentPerLevel INTEGER NOT NULL,
            armorPercentBase INTEGER NOT NULL,
            armorPercentBonus INTEGER NOT NULL,

            armorPenetrationFlat INTEGER NOT NULL,
            armorPenetrationPercent INTEGER NOT NULL,
            armorPenetrationPerLevel INTEGER NOT NULL,
            armorPenetrationPercentPerLevel INTEGER NOT NULL,
            armorPenetrationPercentBase INTEGER NOT NULL,
            armorPenetrationPercentBonus INTEGER NOT NULL,

            attackDamageFlat INTEGER NOT NULL,
            attackDamagePercent INTEGER NOT NULL,
            attackDamagePerLevel INTEGER NOT NULL,
            attackDamagePercentPerLevel INTEGER NOT NULL,
            attackDamagePercentBase INTEGER NOT NULL,
            attackDamagePercentBonus INTEGER NOT NULL,

            attackSpeedFlat INTEGER NOT NULL,
            attackSpeedPercent INTEGER NOT NULL,
            attackSpeedPerLevel INTEGER NOT NULL,
            attackSpeedPercentPerLevel INTEGER NOT NULL,
            attackSpeedPercentBase INTEGER NOT NULL,
            attackSpeedPercentBonus INTEGER NOT NULL,

            cooldownReductionFlat INTEGER NOT NULL,
            cooldownReductionPercent INTEGER NOT NULL,
            cooldownReductionPerLevel INTEGER NOT NULL,
            cooldownReductionPercentPerLevel INTEGER NOT NULL,
            cooldownReductionPercentBase INTEGER NOT NULL,
            cooldownReductionPercentBonus INTEGER NOT NULL,

            criticalStrikeChanceFlat INTEGER NOT NULL,
            criticalStrikeChancePercent INTEGER NOT NULL,
            criticalStrikeChancePerLevel INTEGER NOT NULL,
            criticalStrikeChancePercentPerLevel INTEGER NOT NULL,
            criticalStrikeChancePercentBase INTEGER NOT NULL,
            criticalStrikeChancePercentBonus INTEGER NOT NULL,

            goldPer10Flat INTEGER NOT NULL,
            goldPer10Percent INTEGER NOT NULL,
            goldPer10PerLevel INTEGER NOT NULL,
            goldPer10PercentPerLevel INTEGER NOT NULL,
            goldPer10PercentBase INTEGER NOT NULL,
            goldPer10PercentBonus INTEGER NOT NULL,

            healAndShieldPowerFlat INTEGER NOT NULL,
            healAndShieldPowerPercent INTEGER NOT NULL,
            healAndShieldPowerPerLevel INTEGER NOT NULL,
            healAndShieldPowerPercentPerLevel INTEGER NOT NULL,
            healAndShieldPowerPercentBase INTEGER NOT NULL,
            healAndShieldPowerPercentBonus INTEGER NOT NULL,

            healthFlat INTEGER NOT NULL,
            healthPercent INTEGER NOT NULL,
            healthPerLevel INTEGER NOT NULL,
            healthPercentPerLevel INTEGER NOT NULL,
            healthPercentBase INTEGER NOT NULL,
            healthPercentBonus INTEGER NOT NULL,

            healthRegenFlat INTEGER NOT NULL,
            healthRegenPercent INTEGER NOT NULL,
            healthRegenPerLevel INTEGER NOT NULL,
            healthRegenPercentPerLevel INTEGER NOT NULL,
            healthRegenPercentBase INTEGER NOT NULL,
            healthRegenPercentBonus INTEGER NOT NULL,

            lethalityFlat INTEGER NOT NULL,
            lethalityPercent INTEGER NOT NULL,
            lethalityPerLevel INTEGER NOT NULL,
            lethalityPercentPerLevel INTEGER NOT NULL,
            lethalityPercentBase INTEGER NOT NULL,
            lethalityPercentBonus INTEGER NOT NULL,

            lifestealFlat INTEGER NOT NULL,
            lifestealPercent INTEGER NOT NULL,
            lifestealPerLevel INTEGER NOT NULL,
            lifestealPercentPerLevel INTEGER NOT NULL,
            lifestealPercentBase INTEGER NOT NULL,
            lifestealPercentBonus INTEGER NOT NULL,

            magicPenetrationFlat INTEGER NOT NULL,
            magicPenetrationPercent INTEGER NOT NULL,
            magicPenetrationPerLevel INTEGER NOT NULL,
            magicPenetrationPercentPerLevel INTEGER NOT NULL,
            magicPenetrationPercentBase INTEGER NOT NULL,
            magicPenetrationPercentBonus INTEGER NOT NULL,

            magicResistanceFlat INTEGER NOT NULL,
            magicResistancePercent INTEGER NOT NULL,
            magicResistancePerLevel INTEGER NOT NULL,
            magicResistancePercentPerLevel INTEGER NOT NULL,
            magicResistancePercentBase INTEGER NOT NULL,
            magicResistancePercentBonus INTEGER NOT NULL,

            manaFlat INTEGER NOT NULL,
            manaPercent INTEGER NOT NULL,
            manaPerLevel INTEGER NOT NULL,
            manaPercentPerLevel INTEGER NOT NULL,
            manaPercentBase INTEGER NOT NULL,
            manaPercentBonus INTEGER NOT NULL,

            manaRegenFlat INTEGER NOT NULL,
            manaRegenPercent INTEGER NOT NULL,
            manaRegenPerLevel INTEGER NOT NULL,
            manaRegenPercentPerLevel INTEGER NOT NULL,
            manaRegenPercentBase INTEGER NOT NULL,
            manaRegenPercentBonus INTEGER NOT NULL,

            movespeedFlat INTEGER NOT NULL,
            movespeedPercent INTEGER NOT NULL,
            movespeedPerLevel INTEGER NOT NULL,
            movespeedPercentPerLevel INTEGER NOT NULL,
            movespeedPercentBase INTEGER NOT NULL,
            movespeedPercentBonus INTEGER NOT NULL,

            abilityHasteFlat INTEGER NOT NULL,
            abilityHastePercent INTEGER NOT NULL,
            abilityHastePerLevel INTEGER NOT NULL,
            abilityHastePercentPerLevel INTEGER NOT NULL,
            abilityHastePercentBase INTEGER NOT NULL,
            abilityHastePercentBonus INTEGER NOT NULL,

            omnivampFlat INTEGER NOT NULL,
            omnivampPercent INTEGER NOT NULL,
            omnivampPerLevel INTEGER NOT NULL,
            omnivampPercentPerLevel INTEGER NOT NULL,
            omnivampPercentBase INTEGER NOT NULL,
            omnivampPercentBonus INTEGER NOT NULL,

            tenacityFlat INTEGER NOT NULL,
            tenacityPercent INTEGER NOT NULL,
            tenacityPerLevel INTEGER NOT NULL,
            tenacityPercentPerLevel INTEGER NOT NULL,
            tenacityPercentBase INTEGER NOT NULL,
            tenacityPercentBonus INTEGER NOT NULL
        )
        """
        self._db_execute(schema)

    def write_all_items_metadata(self):
        for item in self.items:
            self.write_item_metadata(int(item['id']))

    def __write_item_metadata(self, item_number):

        response_data = self.__item_http_request(item_number)
        insert_command = "INSERT OR REPLACE INTO item_metadata VALUES (?, ?, ?, ?, ?, ?, ?)"

        requiredChampion, requiredAlly = "requiredChampion", "requiredAlly"
        if requiredChampion not in response_data:
            requiredChampion = "required_champion"
        if requiredAlly not in response_data:
            requiredAlly = "required_ally"

        values = [
            response_data['id'], response_data['name'], response_data[requiredChampion],
            response_data[requiredAlly],  response_data['shop']['prices']['total'],
            response_data['shop']['prices']['sell'],
            1 if response_data['shop']['purchasable'] else 0
        ]
        self._db_execute(insert_command, values)

    def write_all_items_base_stats(self):
        counter = 0
        for item in self.items:
            print(counter, "|", item['id'])
            self.write_item_base_stats(int(item['id']))
            counter += 1

    def __write_item_base_stats(self, item_number):
        response_data = self.__item_http_request(item_number)
        item_id = response_data['id']
        stats = response_data['stats']

        insert_command = """
        INSERT OR REPLACE INTO item_base_stats VALUES
        (
            ?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?
        )
        """
        values = [item_id]
        stat_types = [
            "abilityPower",
            "armor",
            "armorPenetration",
            "attackDamage",
            "attackSpeed",
            "cooldownReduction",
            "criticalStrikeChance",
            "goldPer_10",
            "healAndShieldPower",
            "health",
            "healthRegen",
            "lethality",
            "lifesteal",
            "magicPenetration",
            "magicResistance",
            "mana",
            "manaRegen",
            "movespeed",
            "abilityHaste",
            "omnivamp",
            "tenacity",
        ]

        for stat in stat_types:
            # setting value of stats that are not included to be -1
            if stat not in stats:
                for _ in range(6):
                    values += [-1]
            else:
                for scale_type in stats[stat]:
                    values += [stats[stat][scale_type]]

        self._db_execute(insert_command, values)

    def get_some_items_metadata(self, item_numbers=[]):
        data = []
        if item_numbers:
            for item_number in self.items:
                data += [self.get_item_metadata(int(item_number))]
        else:
            for item in self.items:
                data += [self.get_item_metadata(int(item['id']))]
        return data

    def __get_item_metadata(self, item_number):
        select_command = "SELECT * FROM item_metadata WHERE id = ?"
        self._db_execute(select_command, values=[item_number])
        entry = self.cursor.fetchall()
        return dict(entry[0])

    def get_some_items_base_stats(self, item_numbers=[]):
        data = []
        if item_numbers:
            for item_number in self.items:
                data += [self.get_item_base_stats(int(item_number))]
        else:
            for item in self.items:
                data += [self.get_item_base_stats(int(item['id']))]
        return data

    def __get_item_base_stats(self, item_number):
        select_command = "SELECT * FROM item_base_stats WHERE id = ?"
        self._db_execute(select_command, values=[item_number])
        entry = self.cursor.fetchall()
        return dict(entry[0])
