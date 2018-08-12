from framework.utils.adb import clear_logs


def standard(driver, adb_path, device_id):
    # clear logs
    clear_logs(adb_path, device_id)

    # close AUT
    driver.quit()
