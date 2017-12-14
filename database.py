
def create_tables(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test_suites (id text, creation_time integer, duration integer)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_suite_id ON test_suites (id)")
    cursor.execute("CREATE TABLE IF NOT EXISTS stats (stat_key text, stat_value integer, test_suite_id text)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_key_test_suite_id ON stats (stat_key, test_suite_id)")
    cursor.execute("CREATE TABLE IF NOT EXISTS test_cases (hash_key text, test_suite_id text, creation_time, duration integer)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash_key ON test_cases (hash_key)")

    db_connection.commit()


def add_test_suite(db_connection, test_suite_id, test_suite_start_time):
    duration = 0
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO test_suites VALUES (?, ?, ?)", (test_suite_id, test_suite_start_time, duration))

    db_connection.commit()

    return test_suite_id, test_suite_start_time, duration
