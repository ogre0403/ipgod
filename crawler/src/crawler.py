from Fetcher import Fetcher, Downloader
import queue
import logging

def main():

    # create share queue
    SHARE_Q = queue.Queue()

    # Start Fetcher fetch new metadata, and put into share queue
    fetcher = Fetcher(600, SHARE_Q)
    fetcher.start()

    # Start a downloader, get one metadata from queue,
    # then download open data and archive into ckan
    downloader = Downloader(SHARE_Q)
    downloader.start()



if __name__ == "__main__":
    # Filter out non-necessary logging
    
    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter('root'))
    main()
    