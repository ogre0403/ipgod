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
    conn = DBUtil.createConnection()

    r = requests.get(const.METADATA_URL_PREFIX)
    x = json.loads(r.text)

    dataset = x['result']
    count = 1

    for id in dataset:
        DBUtil.insertDataSetID(conn, id)
        # logger.debug(str(count) + " _ " + id)
        count = count +1

    count = 1
    dataid = DBUtil.getNotProcessedDataSet(conn)
    for s in dataid:
        # logger.debug(str(count) + " _ " + s.package_name)
        # logger.debug(str(count) + " _ " + s)
        count = count +1

    DBUtil.closeConnection(conn)

    fetchers = []
    if config.fetcher_num > 0 :
        for i in range(config.fetcher_num):
            fetchers.append(Fetcher(SHARE_Q, i, dataid))
            fetchers[i].start()

    downloaders = []
    if config.downloader_num > 0:
        for i in range(config.downloader_num):
            downloaders.append(Downloader())
            downloaders[i].start()

if __name__ == "__main__":
    # using python logging in multiple modules
    # Ref: http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
    import logging.config
    logging.config.fileConfig(config.logging_configure_file,
                              defaults=None,
                              disable_existing_loggers=False)
    main()