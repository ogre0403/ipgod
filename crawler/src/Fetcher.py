from metadata import Metadata
import schedule
import time
import threading
import const
import json
import requests
import datetime
import DBUtil
import logging

logging.getLogger("schedule").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


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
            schedule.every(self.updateInterval).seconds.do(self.fetchNewMetadata)

    def dummy(self):
        """
        dummy function for test
        """
        logger.info(str(threading.get_ident()) + " do repeat")

    def process_history(self):
        """
        process history data since last fetch
        """
        logger.info(str(threading.get_ident()) + " process hisotry")
        conn = DBUtil.createConnection()
        latestTime = DBUtil.getLastUpdateEpoch(conn)
        DBUtil.closeConnection(conn)

        dataid = self.findUpdateDataID(latestTime)
        for s in dataid:
            meta = Metadata.getMetaData(s, self.timeStr)
            for md in meta:
                logger.debug(md.getResourceID() + " put to queue")
                self.queue.put(md)


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
            meta = Metadata.getMetaData(s, self.timeStr)
            logger.debug(dataid)
            for md in meta:
                logger.debug(md.getResourceID() + " put to queue")
                self.queue.put(md)

    def findUpdateDataID(self, historyTime= None):
        """
        find all data set which have been updated since self.updateInterval
        return array contains dataset id
        """

        if historyTime is None:
            # fetcher thread get new data periodically
            self.timeStr = self.buildQueryTimeStr()
            logger.info("Fetch new metadata since " + self.timeStr)
            r = requests.get(const.MODIFIED_URL_PREFIX + self.timeStr)
        else:
            # fetcher thread handle history data
            # Case 1: First run
            # Case 2: recovery from failure
            self.timeStr = self.buildQueryTimeStr()
            if historyTime is "NA":
                # Case 1: The first run scenario, handle all past data
                logger.info("Fetch new history metadata from scratch")
                r = requests.get(const.METADATA_URL_PREFIX)
            else:
                # Case 2: Recovery from failure, handle data between failure time and current
                logger.info("Fetch new history metadata since "+historyTime)
                r = requests.get(const.MODIFIED_URL_PREFIX + historyTime)

        x = json.loads(r.text)
        return x['result']


    def buildQueryTimeStr(self):
        """
        build query time string with format yyyy-mm-dd hh:mm:ss
        datetime object value is equal to self.updateInterval ago
        """
        now = datetime.datetime.now()
        return (now - datetime.timedelta(seconds=self.updateInterval)).strftime('%Y-%m-%d %H:%M:%S')

        # Use a fixed time String for testing
        # return "2016-12-01 11:30:00"
