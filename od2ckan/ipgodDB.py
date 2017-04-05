#!/bin/python
# -*- coding: utf-8 -*-
import logging
import psycopg2
import time
import datetime
import ConfigParser

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root') 

config = ConfigParser.ConfigParser()
config.read('config.ini')
class ipgoddb():
    def __init__(self):
        self.conn = 0
	db = config.get('db', 'database')
	user = config.get('db', 'user')
	server = config.get('db', 'host')
	password = config.get('db', 'password')

        try:
            self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (db, user, server, password))
        except:
            logger.warn("connect db error")
        self.cur = self.conn.cursor()

    def get_pkgs(self):
        pkgs = []
        rows=[]
        try:
            #self.cur.execute("SELECT package_name, status, datetime from import where  datetime > CURRENT_TIMESTAMP - INTERVAL '6000 secs' and status=200")
            self.cur.execute("SELECT package_name, resource_id from ckan_download  where status=200 and processed=FALSE and skip=FALSE and package_name != '' limit 1")
            rows = self.cur.fetchall()
        except:
            logger.warn("select error")
        for row in rows:
	    pkg = row[0].rstrip()
            pkgs.append(pkg)
        return pkgs

    def skip_package(self, package, fileid=''):
        print "skip package %s %s" % (package, fileid)
#        self.cur.execute("UPDATE ckan_download SET skip=true where package_name like '{0}'".format(package))
        try:
            if fileid == '':
                print "skip package %s" % (package)
                self.cur.execute("UPDATE ckan_download SET skip=TRUE where package_name like '{0}'".format(package))
                self.conn.commit()
            else:
                print "skip package %s, %s" % (package, fileid)
                print "UPDATE ckan_download SET skip=TRUE where package_name like '{0}' and resource_id like '{1}'".format(package, fileid)
                self.cur.execute("UPDATE ckan_download SET skip=TRUE where package_name like '{0}' and resource_id like '{0}-{1}'".format(package, fileid))
                self.conn.commit()
        except:
            logger.warn("skip packag error")

    def import_done(self, package, fileid):
        try:
            self.cur.execute("UPDATE ckan_download SET processed=TRUE where package_name like %s and resource_id like %s", (package, fileid))
            self.cur.execute("UPDATE ckan_download SET skip=FALSE where package_name like %s and resource_id like %s", (package, fileid))
            self.conn.commit()
        except:
            logger.warn("import done error")

    def exist(self, package, fileid):
        status="X"
        print "package: %s, field %s, status:%s" % (package, fileid, status)
        self.cur.execute("SELECT package_name from import where package_name like %s and file_id = %s", (package, fileid))
	count_pkg = self.cur.fetchall()
	pkg_c = len(count_pkg)
        return pkg_c

    def import_pkg(self, package, fileid, status):
        pkg_c = self.exist(package, fileid)
	if pkg_c > 0:
	    logger.warn("package %s and resource %s exist" % (package, fileid))
	else:
	    try:
		ct = datetime.datetime.now()
		self.cur.execute("INSERT INTO import (package_name, file_id, status, datetime) VALUES (%s, %s, %s, %s)", (package, fileid, status, ct))
		self.conn.commit()
	    except:
		logger.warn("import db error")

    def get_status(self, package, fileid):
        
        pkg_c = 0
        pkg_c = self.exist(package, fileid)
        if pkg_c > 0:
            self.cur.execute("SELECT status from import where package_name like %s and file_id = %s", (package, fileid))
            count_status = self.cur.fetchall()
            status = count_status[0][0]
        else:
            status = 0
        print "package: %s, field %s, status:%s" % (package, fileid, status)
        return status


    def update_pkg(self, package, fileid, status):
        
        if status <= -3:
            self.skip_package(package, fileid)
        try:
            self.cur.execute("UPDATE import SET status=%s where package_name like %s and file_id = %s", (status, package, fileid))
            self.conn.commit()
        except:
            logger.warn("update error")

    def log_package(self, package, fileid, log):
        try:
            self.cur.execute("UPDATE import SET comment='{0}' where package_name like '{1}' and file_id = '{2}'".format(log, package, fileid))
            self.conn.commit()
        except:
            logger.warn("log comment error")

    def remove_pkg(self, package, fileid):
        try:
            self.cur.execute("DELETE from import  where package_name like %s and file_id = %s", package, fileid)
            self.conn.commit()
        except:
            logger.warn("remove error")
