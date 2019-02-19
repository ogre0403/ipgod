import logging.config
import threading

import DsMeta2

logger = logging.getLogger(__name__)


class Downloader(threading.Thread):
    def __init__(self, queue=None):
        """
        queue: shared queue between Fetcher and Downloader
        """
        super(Downloader, self).__init__()
        self.queue = queue
        self.count = 0

    def run(self):
        # Download info from shared queue

        # if not self.queue.empty():
        success = 0
        failed = 0
        failed_list = []
        while not self.queue.empty():
            # Get metadata item from queue, and execute download logic
            dataset_id = self.queue.get()

            # dataset = metadata2.Metadata2.getMetaData(s)
            dsmeta_ojb = DsMeta2.DatasetMeta()
            resource_list = dsmeta_ojb.getResList(dataset_id)

            # Get the flag to check whether the download task is OK or not
            self.count = self.count + 1

            for res_item in resource_list:
                try:

                    if res_item.download(success):
                        success += 1
                        logger.info("download success:" + str(res_item.resourceID))
                    else:
                        failed += 1
                        failed_list.append(res_item.resourceID)
                        logger.info("download failed:" + str(res_item.resourceID))
                except Exception as e:
                    failed += 1
                    failed_list.append(res_item.resourceID)
                    logger.error("download failed:" + str(res_item.resourceID))
        ## finalize the report of the downloaad thread
        logger.info(
            "[Report] Thread {} : total {}, success {}, failed {}"
                .format(threading.get_ident(), self.count, success,failed))

        if failed_list:
            logger.info("[Err] FailedList: {}".format(",".join(failed_list)))
