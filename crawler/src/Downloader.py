from metadata import Metadata
import threading
import logging

LOGGING_FILE = 'ipgod.log'
logging.basicConfig(  # filename=LOGGING_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')


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