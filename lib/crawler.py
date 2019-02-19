import json
import logging
import logging.config
import queue

import config
import Downloader2
import FetcherList

logger = logging.getLogger(__name__)
logging.config.fileConfig(config.crawler_logging_configure_file,
                          defaults=None,
                          disable_existing_loggers=False)

def fatchList():
    SHARE_Q = queue.Queue()
    historyFetcher = FetcherList.FetcherList()
    historyFetcher.processHistory()

def startDownload():
    SHARE_Q = queue.Queue()
    try:
        with open(config.LIST_PATH) as f :
            dataid = json.load(f)
    except(FileNotFoundError):
        logger.info("[startDownload] dataid_list file_not_found")
        return False
    except:
        logger.info("[startDownload] dataid_list Exception")
        return False


    ## build queue
    for s in dataid:
        SHARE_Q.put(s)

    ## start download threads
    downloader_list = []
    for i in range(config.downloader_num):
        downloader_list.append(Downloader2.Downloader(SHARE_Q))
        downloader_list[i].start()



if __name__ == "__main__":
    # using python logging in multiple modules
    # Ref: http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules

    if config.FetchHistory :
        fatchList()
    startDownload()
