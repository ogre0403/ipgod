#!/bin/python
# -*- coding: utf-8 -*-
import csv
import logging
import os.path

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')


class organization_name():
    def __init__(self):
        self.mapfile = "agencies_name_utf8.csv"
        self.org_dict = self.create_org_dict()

    def create_org_dict(self):
        odict = {}
        with open(self.mapfile, 'r', encoding='utf-8') as govfile:
            # spamreader = unicodecsv.reader(govfile, encoding='utf-8')
            spamreader = csv.reader(govfile, delimiter=',')
            for row in spamreader:
                # org_data = row[1].encode('utf8')
                org_data = row[1]
                en = row[2].lower()
                en = en.replace(" ", "_")
                en = en.replace(".", "_")
                en = en.replace(",", "")
                en = en.replace(")", "")
                en = en.replace("(", " ")
                en = en.replace("  ", " ")
                en = en.replace(" ", "_")
                en = en.replace("__", "_")
                odict[org_data] = en
            return odict

    def mapping_chiOrg_engOrg(self, keyword):
        if os.path.isfile(self.mapfile) == False:
            logger.info("organization map(%s) fail" % keyword)
            if os.path.isdir(self.mapfile) is False:
                raise FileNotFoundError

        if keyword in self.org_dict:
            # keyword "台南市政府" , mapping "tainan_city_government"
            return (keyword ,self.org_dict[keyword])
        else :
            # inverse org_dict list to mapping keyword
            for org_key in self.org_dict.keys() :
                if org_key in  keyword :
                    return ( org_key ,self.org_dict[org_key])
            return ( keyword, None)
        # with open(self.mapfile, 'r', encoding='utf-8') as govfile:
        #     # spamreader = unicodecsv.reader(govfile, encoding='utf-8')
        #     spamreader = csv.reader(govfile, delimiter=',')
        #     for row in spamreader:
        #         # org_data = row[1].encode('utf8')
        #         org_data = row[1]
        #         if org_data == keyword:
        #             logger.info("organization map successfully")
        #             en = row[2].lower()
        #             en = en.replace(" ", "_")
        #             en = en.replace(".", "_")
        #             en = en.replace(",", "")
        #             en = en.replace(")", "")
        #             en = en.replace("(", " ")
        #             en = en.replace("  ", " ")
        #             en = en.replace(" ", "_")
        #             en = en.replace("__", "_")
        #             return en
        # return False




if __name__ == '__main__':
    org = organization_name()
    print("return: {}".format(org.search("內政部營建署")))
    print("return: {}".format(org.search("國家發展委員會")))
