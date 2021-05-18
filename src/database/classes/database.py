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
            __file__), '../database.db')

        self.conn = sqlite3.connect(self.database_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.base_url = "http://cdn.merakianalytics.com/riot/lol/resources/{}/en-US".format(
            self.patch)

    def _get_http_request(self, url):
        return requests.get(url)

    def _db_execute(self, command, values=[]):
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

    def close(self):
        self.cursor.close()
        self.conn.close()
