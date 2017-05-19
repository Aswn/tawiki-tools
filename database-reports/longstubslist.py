#!/usr/bin/python
# -*- coding: utf-8 -*-
import mwclient
import MySQLdb
import datetime
from reports import *
from config import *
import sys
from displayTable import *
def long_stubs():

	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )

	# Make the query
	cur = db.cursor()
	query = """SELECT page_title, page_len FROM page JOIN categorylinks ON cl_from = page_id WHERE cl_to LIKE '%குறுங்கட்டுரைகள்' AND page_namespace = 0 AND page_len > 3000 GROUP BY page_title ORDER BY page_len DESC LIMIT 2000;"""
	cur.execute( query )
	content = []
	f2name = "/data/project/aswnbot/database-reports/longstubslist"
	f2 = open(f2name, 'w')
	for row in cur.fetchall():
		f2.write ("[[" + row[0].replace( '_', ' ' ) + "]]\n")
	f2.close()
long_stubs()
