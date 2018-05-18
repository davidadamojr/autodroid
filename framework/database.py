import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def cursor(self):
        return self.db_connection.cursor()

    def close(self):
        self.db_connection.close()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test_suites (id text, creation_time integer)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_suite_id ON test_suites (id)")
        cursor.execute("CREATE TABLE IF NOT EXISTS stats (stat_key text, stat_value integer, test_suite_id text)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_key_test_suite_id ON stats (stat_key, test_suite_id)")
        cursor.execute("CREATE TABLE IF NOT EXISTS test_cases (hash_key text, test_suite_id text, creation_time integer, duration integer)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash_key ON test_cases (hash_key)")
        cursor.execute("CREATE TABLE IF NOT EXISTS event_info (event_hash text, test_suite_id text, frequency integer, termination integer, reward real)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_hash ON event_info (event_hash)")
        self.db_connection.commit()

        logger.info("Successfully created database tables.")

    def add_test_suite(self, test_suite_id, creation_time):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO test_suites VALUES (?, ?)", (test_suite_id, creation_time))
        self.db_connection.commit()

        logger.info(
            "Test generation started at {}.".format(str(creation_time)))  # TODO: change to human-readable time
        logger.info("Creating test suite with id {}".format(str(test_suite_id)))

        return test_suite_id, creation_time

    def add_test_case(self, test_case_hash, test_suite_id, creation_time, duration):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO test_cases VALUES (?, ?, ?, ?)", (test_case_hash, test_suite_id, creation_time, duration))
        self.db_connection.commit()

        return test_case_hash

    def test_case_exists(self, test_suite_id, test_case_hash):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE hash_key=? AND test_suite_id=?", (test_case_hash, test_suite_id))

        if len(cursor.fetchall()) == 0:
            return False

        return True

    def is_termination_event(self, test_suite_id, event_hash):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM event_info WHERE termination=1 AND event_hash='{}' AND test_suite_id='{}'".format(event_hash, test_suite_id))

        if len(cursor.fetchall()) == 0:
            return False

        return True

    def add_termination_event(self, event_hash, test_suite_id):
        cursor = self.db_connection.cursor()
        exists_query = "SELECT event_hash, frequency FROM event_info WHERE event_hash=? AND test_suite_id=?"
        cursor.execute(exists_query, (event_hash, test_suite_id))

        rows = cursor.fetchall()
        if rows:
            logger.warning(
                "Event {} already existed in database before getting marked as termination event.".format(event_hash))
            update_query = "UPDATE event_info SET termination=1, reward=0 WHERE event_hash=? AND test_suite_id=?"
            cursor.execute(update_query, (event_hash, test_suite_id))
        else:
            logger.debug("Marking event {} as termination event.".format(event_hash))
            insert_query = "INSERT INTO event_info VALUES (?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (event_hash, test_suite_id, 1, 1, 0))

        self.db_connection.commit()

        return event_hash

    def update_event_frequency(self, test_suite_id, event_hash):
        logger.debug("Updating event frequency for {}.".format(event_hash))
        cursor = self.db_connection.cursor()
        event_query = "SELECT frequency FROM event_info WHERE event_hash=? AND test_suite_id=?"
        cursor.execute(event_query, (event_hash, test_suite_id))

        rows = cursor.fetchall()
        if rows:
            update_query = "UPDATE event_info SET frequency=frequency+1 WHERE event_hash=? AND test_suite_id=?"
            cursor.execute(update_query, (event_hash, test_suite_id))
        else:
            insert_query = "INSERT INTO event_info VALUES (?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (event_hash, test_suite_id, 1, 0, 1.0))

        self.db_connection.commit()

        return event_hash

    def get_event_frequencies(self, event_hashes, test_suite_id):
        cursor = self.db_connection.cursor()
        placeholders = ','.join('?' for _ in event_hashes)
        query = "SELECT event_hash, frequency FROM event_info " \
                "WHERE event_hash IN ({}) AND test_suite_id=?".format(placeholders)
        cursor.execute(query, list(event_hashes) + [test_suite_id])

        event_frequencies = OrderedDict()
        rows = cursor.fetchall()
        for row in rows:
            event_hash = row[0]
            event_frequency = row[1]
            event_frequencies[event_hash] = event_frequency

        for event_hash in event_hashes:
            if event_hash not in event_frequencies:
                event_frequencies[event_hash] = 0

        return event_frequencies



