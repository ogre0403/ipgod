from metadata import Metadata
import schedule
import time
import threading
import const
import json
import requests
import logging
import datetime

LOGGING_FILE = 'ipgod.log'
logging.basicConfig(  # filename=LOGGING_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')


class Fetcher(threading.Thread):
    """
    Fetcher thread get metadata of newly updated opendata.

    """

    def __init__(self, queue, sec=-1):
        """
        queue: shared queue between Fetcher and Downloader
        sec: interval to fetch updated metadata, default is -1,
            means not get new data periodically.
        """
        super(Fetcher, self).__init__()
        self.queue = queue
        self.updateInterval = sec
        if self.updateInterval > 0:
            schedule.every(self.updateInterval).seconds.do(self.dummy)

    def dummy(self):
        """
        dummy function for test
        """
        logger.info(str(threading.get_ident()) + " do repeat")

    def process_history(self):
        # TODO
        """
        process history data since last fetch
        """
        logger.info(str(threading.get_ident()) + " process hisotry")

    def run(self):
        if self.updateInterval == -1:
            self.process_history()
            return

        while True:
            schedule.run_pending()
            time.sleep(1)

    def fetchNewMetadata(self):
        dataid = self.findUpdateDataID()
        for s in dataid:
            meta = Metadata.getMetaData(s)
            logger.debug(dataid)
            for md in meta:
                logger.debug(md.getResourceID() + " put to queue")
                self.queue.put(md)

    def findUpdateDataID(self):
        """
        find all data set which have been updated since self.updateInterval

        return array contains dataset id
        """
        timeStr = self.buildQueryTimeStr()
        logger.info("Fetch new metadata since " + timeStr)
        r = requests.get(const.MODIFIED_URL_PREFIX + timeStr)
        x = json.loads(r.text)
        return x['result']

    def buildQueryTimeStr(self):
        """
        build query time string with format yyyy-mm-dd hh:mm:ss

        datetime object value is equal to self.updateInterval ago
        """
        now = datetime.datetime.now()
        return (now - datetime.timedelta(seconds=self.updateInterval)).strftime('%Y-%m-%d %H:%M:%S')
        # return "2016-10-18 20:23:12"
