#!/bin/python
# -*- coding: utf-8 -*-
import odtw
import map2ckan
import os
import logging
from ckanapi import RemoteCKAN, NotAuthorized

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root') 


class import2ckan():
    def __init__(self):
	url = "http://140.110.240.59"
	ckan_key = "a6d44b37-7407-4ad1-b457-aa4b6c611d29"
	ua = 'ckanapiexample/1.0 (+http://example.com/my/website)'
	self.ckan = RemoteCKAN(url, apikey=ckan_key, user_agent=ua)
	self.package = {}
	self.package_exist = 0
	self.resources = []

    def check_package(self):
	pkgs = self.ckan.action.package_autocomplete(q=self.package['name'].lower())
	for pkg in pkgs: 
	    if self.package['name'].lower() == pkg['name']:
		package_resources = self.ckan.action.package_show(id=pkg['name'])
		self.resources = package_resources['resources']
		return True
	return False

    def check_resource(self, testresid):
	for res in self.resources:
	    if res['name'] == testresid:
		return True
	return False

    def check_organization(self):
	org = self.ckan.action.organization_list(organizations=[self.package['owner_org']])
	if len(org) == 0:
	    return False
	else:
	    return True

    def check_tag(self):
	return

    def add_package(self):
	try:
            self.ckan.action.package_create(
		name = self.package['name'].lower(),
		title = self.package['title'],
		owner_org = self.package['owner_org'],
		notes = self.package['notes'],
		type = self.package['type'],
		last_modified = self.package['last_modified'],
		#license_id = self.package['license_id'],
		author = self.package['author'],
		author_email = self.package['author_email'],
		tags = self.package['tag'],
		extras = self.package['extras']
            )
	    res = {self.package['name']:True}
	except:
	    res = {self.package['name']:False}
	return res

    def add_resource(self):

	rres = {}
	for res in self.package['resources']:
	    rfile = self.package['basepath']+'/'+res['resourceid']+'.'+res['format'].lower()
	    rid = res['resourceid']
	    try:
		if self.check_resource(res['resourceid'].lower()) == True:
		    logger.info("resource %s exist" % res['resourceid'])
		else:
		    self.ckan.action.resource_create(
			package_id=self.package['name'].lower(),
			url=res['resourceid'].lower(),
			description=res['resourcedescription'],
			format=res['format'].lower(),
			name=res['resourceid'].lower(),
			last_modified=res['resourcemodified'],
			upload=open(rfile, 'rb'),
		    )
		    logger.info("resource added %s" % res['resourceid'])
		rres[rid] = True
	    except:
		rres[rid] = False
	return rres

    def add_organization(self):
	self.ckan.action.organization_create(
		name=self.package['owner_org'],
		title=self.package['org']['title'],
		extras=self.package['org']['extras']
		)
	return

    def add_tag(self):
	return

    def update_organization(self):
	self.ckan.action.organization_update(
		id=self.package['owner_org'],
		name=self.package['owner_org'],
		title=self.package['org']['title'],
		extras=self.package['org']['extras']
		)
	return

    def update_package(self):
	try:
	    self.ckan.action.package_patch(
		id = self.package['name'].lower(),
		name = self.package['name'].lower(),
		title = self.package['title'],
		owner_org = self.package['owner_org'],
		notes = self.package['notes'],
		type = self.package['type'],
		last_modified = self.package['last_modified'],
		#license_id = self.package['license_id'],
		author = self.package['author'],
		author_email = self.package['author_email'],
		tags = self.package['tag'],
		extras = self.package['extras']
	    )
	    res = {self.package['name']:True}
	except:
	    res = {self.package['name']:False}
	return res

    def commit(self, data):
	self.package = data
	ckan_res = {}
	if self.check_organization() == False:
	    logger.info("add organization " + self.package['org']['name'])
	    self.add_organization()
	else:
	    logger.info("update organization " + self.package['org']['name'])
	    self.update_organization()
	
	if self.check_package() == True:
	    logger.info("update package and add resources " + self.package['name'])
	    pres = self.update_package()
	    rres = self.add_resource()
	else:
	    logger.info("add package and resources " + self.package['name'])
	    pres = self.add_package()
	    rres = self.add_resource()
	ckan_res = {'package':pres, 'resources':rres}
	return ckan_res

if __name__ == '__main__': 
    jsonfile = 'testdata/A41000000G-000001/A41000000G-000001.json'
    odtw = odtw.od()
    data = odtw.read(jsonfile)

    ckmap = map2ckan.mapod2ckan()
    package = ckmap.map(data)
    od_data_path = os.path.dirname(os.path.realpath(jsonfile))
    package['basepath'] = od_data_path
    put2ckan = import2ckan()
    res = put2ckan.commit(package)
    print res

