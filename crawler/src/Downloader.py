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

    def run(self):
        while True:
            if not self.queue.empty():
                # Get metadata item from queue, and execute download logic
                item = self.queue.get()

                # Get the flag to check whether the download task is OK or not
                try:
                    self.download_flag = item.download()
                except Exception as e:
                    logging.exception("Download " + item.getResourceID() + " ERROR!!!")