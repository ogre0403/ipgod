# from metadata import Metadata
import threading
import logging.config

import logging
logger = logging.getLogger(__name__)


class Downloader(threading.Thread):
    def __init__(self, queue):
        """
        queue: shared queue between Fetcher and Downloader
        """
        super(Downloader, self).__init__()
        self.queue = queue
        self.count = 0

    def run(self):
        while True:
            if not self.queue.empty():
                # Get metadata item from queue, and execute download logic
                item = self.queue.get()

                # Get the flag to check whether the download task is OK or not
                self.count = self.count + 1
                logger.info("Thread {" + str(threading.get_ident()) + "} has processed " + str(self.count) + " metadata")
                try:
                    logger.info("Thread {" + str(threading.get_ident()) + "} start download " + item.getResourceID())
                    self.download_flag = item.download()
                except Exception as e:
                    logging.exception(str(threading.get_ident()) + " download " + item.getResourceID() + " ERROR!!!")