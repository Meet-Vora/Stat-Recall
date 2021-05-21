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
        url = self.base_url + "/" + item_number + ".json"
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
            self.write_item_metadata(item['id'])

    def write_item_metadata(self, item_number):

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
        for item in self.items:
            self.write_item_base_stats

    def write_item_base_stats(self, item_number):
        response_data = self.__item_http_request(item_number)['stats']
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
        values = [
            response_data['id'],

            response_data['abilityPower']['Flat'],
            response_data['abilityPower']['Percent'],
            response_data['abilityPower']['PerLevel'],
            response_data['abilityPower']['PercentPerLevel'],
            response_data['abilityPower']['PercentBase'],
            response_data['abilityPower']['PercentBonus'],

            response_data['armor']['Flat'],
            response_data['armor']['Percent'],
            response_data['armor']['PerLevel'],
            response_data['armor']['PercentPerLevel'],
            response_data['armor']['PercentBase'],
            response_data['armor']['PercentBonus'],

            response_data['armorPenetration']['Flat'],
            response_data['armorPenetration']['Percent'],
            response_data['armorPenetration']['PerLevel'],
            response_data['armorPenetration']['PercentPerLevel'],
            response_data['armorPenetration']['PercentBase'],
            response_data['armorPenetration']['PercentBonus'],

            response_data['attackDamage']['Flat'],
            response_data['attackDamage']['Percent'],
            response_data['attackDamage']['PerLevel'],
            response_data['attackDamage']['PercentPerLevel'],
            response_data['attackDamage']['PercentBase'],
            response_data['attackDamage']['PercentBonus'],

            response_data['attackSpeed']['Flat'],
            response_data['attackSpeed']['Percent'],
            response_data['attackSpeed']['PerLevel'],
            response_data['attackSpeed']['PercentPerLevel'],
            response_data['attackSpeed']['PercentBase'],
            response_data['attackSpeed']['PercentBonus'],

            response_data['cooldownReduction']['Flat'],
            response_data['cooldownReduction']['Percent'],
            response_data['cooldownReduction']['PerLevel'],
            response_data['cooldownReduction']['PercentPerLevel'],
            response_data['cooldownReduction']['PercentBase'],
            response_data['cooldownReduction']['PercentBonus'],

            response_data['criticalStrikeChance']['Flat'],
            response_data['criticalStrikeChance']['Percent'],
            response_data['criticalStrikeChance']['PerLevel'],
            response_data['criticalStrikeChance']['PercentPerLevel'],
            response_data['criticalStrikeChance']['PercentBase'],
            response_data['criticalStrikeChance']['PercentBonus'],

            response_data['goldPer10']['Flat'],
            response_data['goldPer10']['Percent'],
            response_data['goldPer10']['PerLevel'],
            response_data['goldPer10']['PercentPerLevel'],
            response_data['goldPer10']['PercentBase'],
            response_data['goldPer10']['PercentBonus'],

            response_data['healAndShieldPower']['Flat'],
            response_data['healAndShieldPower']['Percent'],
            response_data['healAndShieldPower']['PerLevel'],
            response_data['healAndShieldPower']['PercentPerLevel'],
            response_data['healAndShieldPower']['PercentBase'],
            response_data['healAndShieldPower']['PercentBonus'],

            response_data['health']['Flat'],
            response_data['health']['Percent'],
            response_data['health']['PerLevel'],
            response_data['health']['PercentPerLevel'],
            response_data['health']['PercentBase'],
            response_data['health']['PercentBonus'],

            response_data['healthRegen']['Flat'],
            response_data['healthRegen']['Percent'],
            response_data['healthRegen']['PerLevel'],
            response_data['healthRegen']['PercentPerLevel'],
            response_data['healthRegen']['PercentBase'],
            response_data['healthRegen']['PercentBonus'],

            response_data['lethality']['Flat'],
            response_data['lethality']['Percent'],
            response_data['lethality']['PerLevel'],
            response_data['lethality']['PercentPerLevel'],
            response_data['lethality']['PercentBase'],
            response_data['lethality']['PercentBonus'],

            response_data['lifesteal']['Flat'],
            response_data['lifesteal']['Percent'],
            response_data['lifesteal']['PerLevel'],
            response_data['lifesteal']['PercentPerLevel'],
            response_data['lifesteal']['PercentBase'],
            response_data['lifesteal']['PercentBonus'],

            response_data['magicPenetration']['Flat'],
            response_data['magicPenetration']['Percent'],
            response_data['magicPenetration']['PerLevel'],
            response_data['magicPenetration']['PercentPerLevel'],
            response_data['magicPenetration']['PercentBase'],
            response_data['magicPenetration']['PercentBonus'],

            response_data['magicResistance']['Flat'],
            response_data['magicResistance']['Percent'],
            response_data['magicResistance']['PerLevel'],
            response_data['magicResistance']['PercentPerLevel'],
            response_data['magicResistance']['PercentBase'],
            response_data['magicResistance']['PercentBonus'],

            response_data['mana']['Flat'],
            response_data['mana']['Percent'],
            response_data['mana']['PerLevel'],
            response_data['mana']['PercentPerLevel'],
            response_data['mana']['PercentBase'],
            response_data['mana']['PercentBonus'],

            response_data['manaRegen']['Flat'],
            response_data['manaRegen']['Percent'],
            response_data['manaRegen']['PerLevel'],
            response_data['manaRegen']['PercentPerLevel'],
            response_data['manaRegen']['PercentBase'],
            response_data['manaRegen']['PercentBonus'],

            response_data['movespeed']['Flat'],
            response_data['movespeed']['Percent'],
            response_data['movespeed']['PerLevel'],
            response_data['movespeed']['PercentPerLevel'],
            response_data['movespeed']['PercentBase'],
            response_data['movespeed']['PercentBonus'],

            response_data['abilityHaste']['Flat'],
            response_data['abilityHaste']['Percent'],
            response_data['abilityHaste']['PerLevel'],
            response_data['abilityHaste']['PercentPerLevel'],
            response_data['abilityHaste']['PercentBase'],
            response_data['abilityHaste']['PercentBonus'],

            response_data['omnivamp']['Flat'],
            response_data['omnivamp']['Percent'],
            response_data['omnivamp']['PerLevel'],
            response_data['omnivamp']['PercentPerLevel'],
            response_data['omnivamp']['PercentBase'],
            response_data['omnivamp']['PercentBonus'],

            response_data['tenacity']['Flat'],
            response_data['tenacity']['Percent'],
            response_data['tenacity']['PerLevel'],
            response_data['tenacity']['PercentPerLevel'],
            response_data['tenacity']['PercentBase'],
            response_data['tenacity']['PercentBonus']

        ]
        self._db_execute(insert_command, values)
