from metadata import Metadata
import threading


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
                self.download_flag = item.download()
                # time.sleep(1)