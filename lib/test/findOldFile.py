#!/bin/python
# -*- coding: utf-8 -*-

import requests
import re

def getRIDfromURL(res, url):
    url = re.sub('.*:', '', url, 1)
    resdatas = res
    for resdata in resdatas:
            print(resdata.get('extras').get('downloadURL'))
            extras = resdata['extras']
            testurl = re.sub('.*:', '', extras['downloadURL'], 1)
            #print resdata['resourceid']
            if testurl == url:
                return resdata['resourceid']

    return ''


# https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def downloadFile(url, fn):
    #local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(fn, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return True

if __name__ == '__main__':
    #pid = "A62000000G-000076"
    testurl = "http://www.ftc.gov.tw/upload/公平交易委員會補(捐)助經費一覽表(105年第4季).csv"
    testurl = "http://www4.yunlin.gov.tw/uploaddowndoc?file=/pubyunlin/pubbulletin/雲林縣公車路線清單.docx&flag=doc"
    downloadFile(testurl, "a.doc")
    #rid = getRIDfromURL(pid, testurl)
    #print(rid)
