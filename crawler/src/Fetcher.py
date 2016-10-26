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
logging.basicConfig(#filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')




class Fetcher(threading.Thread) :
    """
    Fetcher thread get metadata of newly updated opendata.

    """

    def __init__(self, sec, queue) :
        """
        sec: interval to fetch updated metadata
        queue: shared queue between Fetcher and Downloader
        """
        super(Fetcher, self).__init__()
        self.queue = queue
        self.updateInterval = sec
        schedule.every(self.updateInterval).seconds.do(self.fetchNewMetadata)

    def run(self) :
        while True:
            schedule.run_pending()
            time.sleep(1)

    def fetchNewMetadata(self):
        dataid = self.findUpdateDataID()
        for s in dataid:
            meta = Metadata.getMetaData(s)
            print(dataid)
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



class Downloader(threading.Thread) :
    def __init__(self,  queue) :
        """
        queue: shared queue between Fetcher and Downloader
        """
        super(Downloader, self).__init__()
        self.queue = queue

    def run(self) :
        while True:
            if not self.queue.empty():
                # Get metadata item from queue, and execute download logic
                item = self.queue.get()
                
                # Get the flag to check whether the download task is OK or not
                self.download_flag = item.download()
            # time.sleep(1)
