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
            "SELECT name FROM sqlite_master WHERE type='table' AND (name='test_suites' OR name='stats' OR name='test_cases'" +
            " OR name='event_info')")
        self.assertEqual(len(cursor.fetchall()), 4)

    def test_can_add_test_suite(self):
        # Arrange
        test_suite_id = uuid.uuid4().hex
        creation_time = time.time()

        # Act
        test_suite_id, creation_time = database.add_test_suite(self.connection, test_suite_id, creation_time)

        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM test_suites WHERE id=?", (test_suite_id, ))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], test_suite_id)
        self.assertEqual(rows[0][1], creation_time)

    def test_can_add_test_case(self):
        # Arrange
        test_case_hash = "test_case_hash"
        test_suite_id = "b927bd995c5d4204a3c1e1420dde735c"
        creation_time = 1516959397
        duration = 10

        # Act
        database.add_test_case(self.connection, test_case_hash, test_suite_id, creation_time, duration)

        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE hash_key=?", (test_case_hash, ))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], test_case_hash)
        self.assertEqual(rows[0][1], test_suite_id)
        self.assertEqual(rows[0][2], creation_time)
        self.assertEqual(rows[0][3], duration)

    def test_test_case_exists(self):
        # Arrange
        test_case_hash = "test_case_hash"
        test_suite_id = "test_suite_id"
        creation_time = 1234567890
        duration = 10
        database.add_test_case(self.connection, test_case_hash, test_suite_id, creation_time, duration)

        # Act
        test_case_exists = database.test_case_exists(self.connection, test_suite_id, test_case_hash)

        # Assert
        self.assertTrue(test_case_exists)

    def test_test_case_does_not_exist(self):
        # Arrange
        test_case_hash = "test_case_hash"
        test_suite_id = "test_suite_id"
        creation_time = 1234567890
        duration = 10
        database.add_test_case(self.connection, test_case_hash, test_suite_id, creation_time, duration)

        # Act
        test_case_exists = database.test_case_exists(self.connection, "fake_test_suite_id", "fake_test_case_hash")

        # Assert
        self.assertFalse(test_case_exists)

    def test_add_termination_event_when_not_existing(self):
        #Arrange
        event_hash = "event_hash"
        test_suite_id = "test_suite_id"
        reward = 1.0

        # Act
        database.add_termination_event(self.connection, test_suite_id, event_hash)

        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM event_info WHERE event_hash=? AND test_suite_id=?", (event_hash, test_suite_id))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][3], 1)

    def test_add_termination_event_when_existing(self):
        # Arrange
        event_hash = "event_hash"
        test_suite_id = "test_suite_id"
        database.add_termination_event(self.connection, test_suite_id, event_hash)

        # Act
        database.add_termination_event(self.connection, test_suite_id, event_hash)

        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM event_info WHERE event_hash=? AND test_suite_id=?", (event_hash, test_suite_id))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][3], 1)

    def test_is_termination_event(self):
        # Arrange
        event_hash = "event_hash"
        test_suite_id = "test_suite_id"
        database.add_termination_event(self.connection, test_suite_id, event_hash)

        # Act
        is_termination_event = database.is_termination_event(self.connection, test_suite_id, event_hash)

        # Assert
        self.assertTrue(is_termination_event)

    def test_is_not_termination_event(self):
        # Arrange
        event_hash = "event_hash"
        test_suite_id = "test_suite_id"

        # Act
        is_termination_event = database.is_termination_event(self.connection, test_suite_id, event_hash)

        # Assert
        self.assertFalse(is_termination_event)

    def test_update_event_frequency_when_not_existing(self):
        # Arrange
        event_hash = "event_hash"
        test_suite_id = "test_suite_id"

        # Act
        database.update_event_frequency(self.connection, test_suite_id, event_hash)

        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT frequency FROM event_info WHERE test_suite_id=? AND event_hash=?", (test_suite_id, event_hash))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 1)

    def test_update_event_frequency_when_existing(self):
        # Arrange
        event_hash = "event_hash"
        test_suite_id = "test_suite_id"
        database.update_event_frequency(self.connection, test_suite_id, event_hash)

        # Act
        database.update_event_frequency(self.connection, test_suite_id, event_hash)

        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT frequency FROM event_info WHERE test_suite_id=? AND event_hash=?", (test_suite_id, event_hash))
        rows = cursor.fetchall()
        print(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 2)

    def tearDown(self):
        self.connection.close()
        dbo_path = os.path.join("..", "..", "db", "autodroid.db")
        db_path = "../../db/autodroid.db"
        if os.path.isfile(db_path):
            os.remove(db_path)