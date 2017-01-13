from Fetcher import Fetcher
from Downloader import Downloader
import queue
import config
import logging
import const
import requests
import json
import DBUtil

logger = logging.getLogger(__name__)


def main():


    SHARE_Q = queue.Queue()


    # r = requests.get(const.METADATA_URL_PREFIX)
    # x = json.loads(r.text)

    # dataid = x['result']
    # count = 1
    conn = DBUtil.createConnection()
    # for s in dataid:
    #     DBUtil.insertDataSetID(conn, s)
    #     logger.debug(str(count) + " _ " + s)
    #     count = count +1

    count = 1
    dataid2 = DBUtil.getNotProcessedDataSet(conn)
    # for s in dataid2:
    # logger.debug(str(count) + " _ " + s.package_name)
    # logger.debug(str(count) + " _ " + s)
    # count = count +1

    DBUtil.closeConnection(conn)

    fetchers = []
    if (config.fetcher_num > 0):
        for i in range(config.fetcher_num):
            fetchers.append(Fetcher(SHARE_Q, i, dataid2))
            fetchers[i].start()


if __name__ == "__main__":
    # using python logging in multiple modules
    # Ref: http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
    import logging.config
    logging.config.fileConfig(config.logging_configure_file,
                              defaults=None,
                              disable_existing_loggers=False)
    main()