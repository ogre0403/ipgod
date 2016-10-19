from Fetcher import Fetcher, Downloader
import Queue
import logging

def main():

    # create share queue
    SHARE_Q = Queue.Queue()

    # Start Fetcher fetch new metadata, and put into share queue
    fetcher = Fetcher(60, SHARE_Q)
    fetcher.start()

    # Start a downloader, get one metadata from queue,
    # then download open data and archive into ckan
    downloader = Downloader(SHARE_Q)
    downloader.start()



if __name__ == "__main__":
    # Filter out non-necessary logging
    print("123456")
    """
    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter('root'))
    main()
    """