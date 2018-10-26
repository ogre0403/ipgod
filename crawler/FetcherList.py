import json
import logging
import requests
import config


logger = logging.getLogger(__name__)


class FetcherList():
    dataid = None
    def processHistory(self):
        latestTime = config.History_Time
        r = requests.get(config.MODIFIED_URL_PREFIX + latestTime)
        x = json.loads(r.text)
        dataid = x['result']

        ## load json file only as dataid
        try:
            with open(config.LIST_PATH, 'w') as outfile:
                json.dump(dataid, outfile)
        except:
            return False



if __name__ == "__main__":
    # using python logging in multiple modules
    # Ref: http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules

    fl = FetcherList()
    if fl.processHistory() :
        print("Ok")
    else:
        print("Failed")