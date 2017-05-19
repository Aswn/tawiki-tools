#!/usr/bin/python
# -*- coding: utf-8 -*-

import mwclient
import MySQLdb
import datetime
from reports import *
from config import *
import sys
from displayTable import *

def linkify( title, namespace ):
	title = str( title )
	title_clean = title.replace( '_', ' ' )
	if namespace is None:
		return '[[' + title_clean + ']]'
	elif namespace is 6:
		return '[[:{{subst:ns:%s}}:%s]]' % ( namespace, title_clean )
	else:
		return '[[{{subst:ns:%s}}:%s]]' % ( namespace, title_clean )

def long_stubs():

	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )

	# Make the query
	cur = db.cursor()
	query = """SELECT page_title, page_len FROM page JOIN categorylinks ON cl_from = page_id WHERE cl_to LIKE '%குறுங்கட்டுரைகள்' AND page_namespace = 0 AND page_len > 2000 GROUP BY page_title ORDER BY page_len DESC LIMIT 2000;"""
	cur.execute( query )
	content = [ ['longstubs-title', 'longstubs-length'] ]
	for row in cur.fetchall():
		content.append([ linkify( row[0], 0 ) , row[1] ])

	# Format the data as wikitext
	text = display_report( 'ta', content, 'longstubs-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'longstubs-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

long_stubs()
