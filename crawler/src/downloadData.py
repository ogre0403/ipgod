import logging
import config
import requests

logging.getLogger("download").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class downloadData:
    def __init__(self, URL, format, dataSetID, resourceID):
        self.URL = URL
        self.format = format
        self.dataSetID = dataSetID
        self.resourceID = resourceID

    def download(self):
        URL = self.URL
        logger.info("download from " + URL)

        name = self.resourceID.replace("/", "")
        dir_name = self.dataSetID + "/"

        abspath = config.DOWNLOAD_PATH + "/" + dir_name

        # to avoid the bad connection and invalid URL
        try:
            response = requests.get(URL, stream=True, verify=False, headers={'Connection': 'close'})
        except:
            logger.debug("Request error at " + URL)
            return -1

        file_name = abspath + name + "." + self.format.strip(";\"").lower()

        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info("Download completed. File path: " + file_name)

        return response.status_code

    def getResourceID(self):
        return self.resourceID
    def getDataSetID(self):
        return self.dataSetID
    def getURL(self):
        return self.URL
    def getFormat(self):
        return self.format