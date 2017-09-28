import database
import unittest
import sqlite3
import os
import uuid


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect("../../db/autodroid.db")
        database.create_tables(self.connection)

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND (name='test_suites' OR name='stats' OR name='test_cases')")
        self.assertEqual(len(cursor.fetchall()), 3)

    def can_add_test_suite(self):
        test_suite_id = uuid.uuid4().hex
        test_suite_id, creation_time, duration = database.add_test_suite(self.connection, test_suite_id)

        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM test_suites WHERE id=? AND creation_time=? AND duration=?", (test_suite_id, creation_time,
                                                                                     duration))
        self.assertEqual(len(cursor.fetchall()), 1)

    def tearDown(self):
        self.connection.close()
        db_path = "../../db/autodroid.db"
        if os.path.isfile(db_path):
            os.remove(db_path)