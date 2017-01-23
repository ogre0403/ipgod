#!/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import ConfigParser
import sys

from ckanapi import RemoteCKAN, NotAuthorized, NotFound, ValidationError, CKANAPIError, ServerIncompatibleError

LOGGING_FILE = 'ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root') 

config = ConfigParser.ConfigParser()
config.read('config.ini')

class downloadPackage():
    def __init__(self):
        global config
        url = config.get('ckan', 'ckanurl')
        ckan_key = config.get('ckan', 'ckan_key')
        ua = 'ckanapiexample/1.0 (+http://example.com/my/website)'
        self.ckan = RemoteCKAN(url, apikey=ckan_key, user_agent=ua)

    def package(self, packageid):
        package = self.ckan.action.package_show(id=packageid)
        return package

    def resource(self, resourceid):
        resource = self.ckan.action.resource_show(id=resourceid)
        return resource

    def extract_list(self):
	#test = self.ckan.action.user_show(id='thomas')
	#test = self.ckan.action.get_news()
	list_data = self.ckan.action.get_selection()
	return list_data['list']


if __name__ == '__main__': 

    ckandata = downloadPackage()
    pkglist = ckandata.extract_list()
    print pkglist
    for pkg in pkglist:
	pkgid = pkg['package']
	rid = pkg['resource']
	pkg_data = ckandata.package(pkgid)
        res_data = ckandata.resource(rid)
	res_url = res_data['url']
	print "wget %s" % res_url

