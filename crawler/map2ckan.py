#!/bin/python
# -*- coding: utf-8 -*-
import hashlib
import re
import organization_map


class mapod2ckan():
    def __init__(self):
        self.package = {'groups': [], 'extras': [], 'tag': [], 'resources': [], 'org': {'extras': []}}
        self.license_id = '1'
        self.license_url = 'http'

    def map_package_params(self, key, value):
        self.package[key] = value

    def map_tag_params(self, key, value):
        for keyword in value:
            # mark for create vocabulary tags
            #    testkeyword = keyword.encode('utf-8')
            #    if testkeyword.isalpha() == True:
            #	testkeyword = testkeyword.lower()
            #	testkeyword = testkeyword.replace(" ", "_")
            #	tagdata={'name':testkeyword.lower()}
            #	self.package['tag'].append(tagdata)
            #    else:
            #	tagdata={'name':testkeyword}
            #	self.package['tag'].append(tagdata)
            # and thsi is free tags
            values = re.split(",", keyword)
            if len(values) > 1:
                self.map_tag_params("keyword", values)
            else:
                skipkw = re.compile('http://')
                if skipkw.search(keyword) != '':
                    return
                keyword = keyword.replace(u"「", "")
                keyword = keyword.replace(u"」", "")
                keyword = keyword.replace(u"／", "")
                keyword = keyword.replace(u"/", "")
                keyword = keyword.replace(u"。", "")
                keyword = keyword.replace(u"、", "")
                keyword = keyword.replace(u"'", "")
                keyword = keyword.replace(u"?", "")
                if len(keyword) == 0:
                    return
                elif len(keyword) < 2:
                    keyword = "%s_" % keyword
                # print "keyword: n%sn" % keyword
                tagdata = {'name': keyword}
                self.package['tag'].append(tagdata)

    def map_group_param(self, key, value):
        # this is static rule 'categoryCode:group_name'
        # makesure your ckan create the group first
        group_info = {
            'E00': 'lifesafety',  # 生活安全及品質
            'I00': 'publicinformation',  # 公共資訊
            '900': 'travel',  # 休閒旅遊
            '800': 'investment',  # 投資理財
            'A00': 'traffic',  # 交通及通訊
            '600': 'business',  # 開創事業
            '500': 'job',  # 求職及就業
            'B00': 'medical',  # 就醫
            '300': 'study',  # 求學及進修
            'D00': 'election',  # 選舉及投票
            '200': 'birth',  # 出生及收養
            'G00': 'elderlycare',  # 老年安養
            '100': 'fertility',  # 生育保健
            'H00': 'lifeetiquette',  # 生命禮儀
            'C00': 'housepurchase',  # 購屋及遷徙
            '400': 'army',  # 服兵役
            '700': 'marriage',  # 婚姻
            'F00': 'retirement'  # 退休
        }

        groupdata = {'name': group_info[value]}
        self.package['groups'].append(groupdata)

    def map_organization_params(self, key, value):
        if key == 'publisher':
            org = organization_map.organization_name()
            # owner_org = org.search(value.encode('utf8'))
            owner_org = org.search(value)
            if owner_org == None:
                m = hashlib.md5()
                # m.update(value.encode('utf-8'))
                m.update(value)
                owner_org = m.hexdigest()[:10]

            self.package['owner_org'] = owner_org
            self.package['org']['name'] = owner_org
            # self.package['org']['title'] = value.encode('utf-8')
            self.package['org']['title'] = value
        else:
            org_extra = {}
            # org_extra['key'] = key.encode('utf-8')
            org_extra['key'] = key
            # org_extra['value'] = value.encode('utf-8')
            org_extra['value'] = value
            self.package['org']['extras'].append(org_extra)
            # print "org"+key

    def map_package_extras(self, key, value):
        if key == 'notes':
            key = "extra note"

        if key == 'type':
            key = "data type"

        # print "key %s value b%sb" % (key, value)
        if type(value) is int:
            data = value
        elif type(value) is bool:
            data = str(value)
        elif type(value) is list or type(value) is tuple:
            data = ''.join(str(e) for e in value)
        else:
            # data = value.encode('utf-8')
            data = value

        extra = {}
        # extra['key'] = key.encode('utf-8')
        extra['key'] = key
        extra['value'] = data
        self.package['extras'].append(extra)

    def map_resources_params(self, key, value):
        for data in value:
            resource = {'resourceid': '', 'resourcedescription': '', 'format': '', 'resourcemodified': '', 'extras': {}}
            for rk, rv in data.items():
                if rk == 'resourceID':
                    resource['resourceid'] = rv
                elif rk == 'resourceDescription':
                    resource['resourcedescription'] = rv
                elif rk == 'format':
                    resource['format'] = rv
                elif rk == 'resourceModified':
                    resource['resourcemodified'] = rv
                else:
                    resource['extras'][rk] = rv
            self.package['resources'].append(resource)

    def map(self, data):
        rs = data
        for k, v in rs.items():
            if k == 'title':
                self.map_package_params('title', v)
            elif k == 'identifier':
                self.map_package_params('name', v)
            elif k == 'description':
                self.map_package_params('notes', v)
            # elif k == 'type':
            #		self.map_package_params('type', v)
            elif k == 'modified':
                self.map_package_params('last_modified', v)
            elif k == 'license':
                self.map_package_params('license_id', self.license_id)
            elif k == 'license_URL':
                self.map_package_params('license_url', self.license_url)
            elif k == 'publisherOID':
                self.map_organization_params(k, v)
            elif k == 'publisherOrgCode':
                self.map_organization_params(k, v)
            elif k == 'publisherContactEmail':
                self.map_organization_params(k, v)
                self.map_package_params('author_email', v)
            elif k == 'publisherContactName':
                self.map_package_params('author', v)
                self.map_organization_params(k, v)
            elif k == 'publisher':
                self.map_organization_params(k, v)
            elif k == 'publisherContactPhone':
                self.map_organization_params(k, v)
            elif k == 'contactName':
                self.map_package_params('author', v)
            elif k == 'contactEmail':
                self.map_package_params('author_email', v)
            elif k == 'landingPage':
                self.map_organization_params(k, v)
            elif k == 'keyword':
                self.map_tag_params(k, v)
            elif k == 'distribution':
                self.map_resources_params(k, v)
            elif k == 'categoryCode':
                self.map_group_param('group', v)
            elif k == 'Comments':
                continue
            else:
                self.map_package_extras(k, v)
        return self.package
