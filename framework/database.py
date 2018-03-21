import logging

logger = logging.getLogger(__name__)


def create_tables(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test_suites (id text, creation_time integer)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_suite_id ON test_suites (id)")
    cursor.execute("CREATE TABLE IF NOT EXISTS stats (stat_key text, stat_value integer, test_suite_id text)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_key_test_suite_id ON stats (stat_key, test_suite_id)")
    cursor.execute("CREATE TABLE IF NOT EXISTS test_cases (hash_key text, test_suite_id text, creation_time integer, duration integer)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash_key ON test_cases (hash_key)")
    cursor.execute("CREATE TABLE IF NOT EXISTS event_info (event_hash text, test_suite_id text, frequency integer, termination integer, reward real)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_hash ON event_info (event_hash)")

    db_connection.commit()

    logger.info("Successfully created database tables.")


def add_test_suite(db_connection, test_suite_id, creation_time):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO test_suites VALUES (?, ?)", (test_suite_id, creation_time))

    db_connection.commit()

    logger.info(
        "Test generation started at {}.".format(str(creation_time)))  # TODO: change to human-readable time
    logger.info("Creating test suite with id {}".format(str(test_suite_id)))

    return test_suite_id, creation_time


def add_test_case(db_connection, test_case_hash, test_suite_id, creation_time, duration):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO test_cases VALUES (?, ?, ?, ?)", (test_case_hash, test_suite_id, creation_time, duration))

    db_connection.commit()

    return test_case_hash


def test_case_exists(db_connection, test_suite_id, test_case_hash):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM test_cases WHERE hash_key=? AND test_suite_id=?", (test_case_hash, test_suite_id))

    if len(cursor.fetchall()) == 0:
        return False

    return True


def is_termination_event(db_connection, test_suite_id, event_hash):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM event_info WHERE termination=1 AND event_hash='{}' AND test_suite_id='{}'".format(event_hash, test_suite_id))

    if len(cursor.fetchall()) == 0:
        return False

    return True


def add_termination_event(db_connection, test_suite_id, event_hash):
    cursor = db_connection.cursor()
    exists_query = "SELECT event_hash, frequency FROM event_info WHERE event_hash=? AND test_suite_id=?"
    cursor.execute(exists_query, (event_hash, test_suite_id))

    rows = cursor.fetchall()
    if len(rows) == 0:
        insert_query = "INSERT INTO event_info VALUES (?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (event_hash, test_suite_id, 1, 1, 0))
    else:
        logger.warning("Event {} already existed in database before getting marked as termination event.".format(event_hash))
        update_query = "UPDATE event_info SET termination=1"
        cursor.execute(update_query)

    db_connection.commit()

    return event_hash


def update_event_frequency(db_connection, test_suite_id, event_hash):
    cursor = db_connection.cursor()
    event_query = "SELECT frequency FROM event_info WHERE event_hash=? AND test_suite_id=?"
    cursor.execute(event_query, (event_hash, test_suite_id))

    rows = cursor.fetchall()
    if len(rows) == 0:
        insert_query = "INSERT INTO event_info VALUES (?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (event_hash, test_suite_id, 1, 0, 1.0))
    else:
        update_query = "UPDATE event_info SET frequency=frequency+1"
        cursor.execute(update_query)

    db_connection.commit()

    return event_hash



