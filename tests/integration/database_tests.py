import os
import sqlite3
import unittest
import uuid
import time

from framework import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect("../../db/autodroid.db")
        database.create_tables(self.connection)

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND (name='test_suites' OR name='stats' OR name='test_cases')")
        self.assertEqual(len(cursor.fetchall()), 3)

    def test_can_add_test_suite(self):
        test_suite_id = uuid.uuid4().hex
        creation_time = time.time()
        test_suite_id, creation_time = database.add_test_suite(self.connection, test_suite_id, creation_time)

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM test_suites WHERE id=?", (test_suite_id, ))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], test_suite_id)
        self.assertEqual(rows[0][1], creation_time)

    def test_can_add_test_case(self):
        test_case_hash = "test_case_hash"
        test_suite_id = "b927bd995c5d4204a3c1e1420dde735c"
        creation_time = 1516959397
        duration = 10

        database.add_test_case(self.connection, test_case_hash, test_suite_id, creation_time, duration)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE hash_key=?", (test_case_hash, ))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], test_case_hash)
        self.assertEqual(rows[0][1], test_suite_id)
        self.assertEqual(rows[0][2], creation_time)
        self.assertEqual(rows[0][3], duration)

    def tearDown(self):
        self.connection.close()
        dbo_path = os.path.join("..", "..", "db", "autodroid.db")
        db_path = "../../db/autodroid.db"
        if os.path.isfile(db_path):
            os.remove(db_path)