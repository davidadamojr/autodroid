import logging
import factory
from appiumatic.exceptions import InvalidParameter
from framework.utils import adb
import config
from allpairspy import AllPairs


logger = logging.getLogger(__name__)


def main():
    database = factory.create_database()
    suite_info = database.create_suite()
    try:
        output_paths = factory.create_directories(suite_info.creation_time)
        text_values = factory.retrieve_text_values()
        allpairs_input = [["CHANGE_LANDSCAPE","CHANGE_PORTRAIT"],["POWER_ON","POWER_OFF"],["INTERNET_CONNECTED","INTERNET_DISCONNECTED"],["BATTERY_LOW","BATTERY_OK","BATTERY_HIGH"]]
        context_covering_array = []
        for val in AllPairs(allpairs_input):
            context_covering_array.append(val)

        explorer = factory.create_explorer(database, text_values, context_covering_array)
        explorer.explore(suite_info, output_paths)
    except InvalidParameter as ip:
        logger.critical(ip)
    except IOError as io_error:
        logger.fatal(io_error)
    except ConnectionRefusedError as conn_refused:
        logger.fatal("Could not connect to appium server: {}.".format(conn_refused))

        # clean up - remove directories, remove database entries
    except Exception as e:
        logger.fatal("A fatal error occurred: {}".format(e))

        # clean up - remove directories, remove database entries

    database.close()


main()
