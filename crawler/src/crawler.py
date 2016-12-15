from Fetcher import Fetcher
from Downloader import Downloader
import queue
import logging
import config


def main():
    # create share queue
    SHARE_Q = queue.Queue()

    # According to configuration, start a thread for fetch
    # history data since last fetch or not.
    if (config.FetchHistory):
        historyFetcher = Fetcher(SHARE_Q)
        historyFetcher.start()

    # Start Fetcher fetch new metadata, and put into share queue
    updateFetcher = Fetcher(SHARE_Q, config.update_interval_sec)
    updateFetcher.start()

    # Start a downloader, get one metadata from queue,
    # then download open data and archive into ckan
    downloader = Downloader(SHARE_Q)
    downloader.start()


if __name__ == "__main__":
    # Filter out non-necessary logging

    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter('root'))
    main()
