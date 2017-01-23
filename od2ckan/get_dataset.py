#!/bin/python 
# -*- coding: utf-8 -*- 
import os 
import logging 
import ConfigParser 
import sys 
 
from ckanapi import RemoteCKAN, NotAuthorized, NotFound, ValidationError, CKANAPIError, ServerIncompatibleError 
 
LOGGING_FILE = 'ipgod-od2ckan.log' 
logging.basicConfig(filename=LOGGING_FILE, 
                    level=logging.INFO, 
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s') 
logger = logging.getLogger('root')  
 
config = ConfigParser.ConfigParser() 
config.read('config.ini') 
 
class downloadPackage(): 
    def __init__(self): 
        global config 
        url = config.get('od2ckan', 'ckanurl') 
        ckan_key = config.get('od2ckan', 'ckan_key') 
        ua = 'ckanapiexample/1.0 (+http://example.com/my/website)' 
        self.ckan = RemoteCKAN(url, apikey=ckan_key, user_agent=ua) 
 
    def package(self, packageid): 
        package = self.ckan.action.package_show(id=packageid) 
        print package 
 
    def resource(self, resourceid): 
        resource = self.ckan.action.resource_show(id=resourceid) 
        print resource 
 
if __name__ == '__main__':  
    pkgid = 'lass_data' 
    rid = '8dc0f68b-5175-482b-8aa7-25c202d9f48b'
    if len(sys.argv) > 0: 
        pkgid = sys.argv[1] 
 
    ckandata = downloadPackage() 
    ckandata.package(pkgid) 
    ckandata.resource(rid) 

