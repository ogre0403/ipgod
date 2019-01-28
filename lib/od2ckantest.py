#!/bin/python

import logging
import os
import sys
import time

from ckanapi import RemoteCKAN, NotFound, ValidationError, CKANAPIError

import config
import map2ckan
import odtw


class import2ckan():
    def __init__(self):
        # global config
        # url = config.get('od2ckan', 'ckanurl')
        url = config.ckanurl
        # ckan_key = config.get('od2ckan', 'ckan_key')
        ckan_key = config.ckan_key

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
            if testresid in res['url']:
                return True

        return False

    def check_organization(self):
        # if self.package['owner_org'] == None:
        #     self.package['owner_org']=self.package['identifier']
        org = self.ckan.action.organization_list(organizations=[self.package['owner_org']])
        if len(org) == 0:
            return False
        else:
            return True

    def check_tag(self):
        return


    def add_organization(self):

        self.ckan.action.organization_create(
            name=self.package['owner_org'],
            title=self.package['org']['title'],
            extras=self.package['org']['extras'],
            users=[{"name": "admin"}]
        )


    def update_organization(self):
        self.ckan.action.organization_update(
        # self.ckan.action.update.organization_update(
            id=self.package['owner_org'],
            name=self.package['owner_org'],
            title=self.package['org']['title'],
            extras=self.package['org']['extras'],
            users=[{"name": "admin"}]
        )
        return

    def commit(self, data):
        self.package = data
        ckan_res = {}
        # print data
        if self.check_organization() == False:
            self.add_organization()
        else:
            self.update_organization()

        return ckan_res

if __name__ == '__main__':
    jsonfile = './data/301210000T-000312/301210000T-000312.json'
    odtw = odtw.od()
    data = odtw.read(jsonfile)

    ckmap = map2ckan.mapod2ckan()
    package = ckmap.map(data)
    od_data_path = os.path.dirname(os.path.realpath(jsonfile))
    package['basepath'] = od_data_path
    put2ckan = import2ckan()
    res = put2ckan.commit(package)

