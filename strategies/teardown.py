
def standard(driver, test_case=None, db_connection=None, output_file=None, get_logs_fn=None, get_coverage_fn=None):
    assert test_case is not None and db_connection is not None and output_file is not None and get_logs_fn is not None

   # clear SD card

    # close AUT
    driver.quit()