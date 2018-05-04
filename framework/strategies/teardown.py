from framework.utils.scripts import clear_logs


def standard(driver, adb_path):
    # clear logs
    clear_logs(adb_path)

    # close AUT
    driver.quit()
