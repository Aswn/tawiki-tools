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

def article_by_size():
	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )
	cur = db.cursor()
	query = """SELECT  page_namespace,  page_title,  page_len  FROM page  WHERE page_namespace = 0  AND page_len > 175000  AND page_title NOT LIKE "%/%"  ORDER BY page_len DESC  LIMIT 1000;"""
	cur.execute( query )
	content = []
	content.append( ['article_by_size-namespace', 'article_by_size-title', 'article_by_size-size'] )
	for row in cur.fetchall():
		content.append( [ row[0], linkify( row[1], row[0] ), row[2] ])
	text = display_report( 'ta', content, 'article_by_size-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'article_by_size-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

def most_edited_page_last_month():
	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )
	cur = db.cursor()
	query = """SELECT rc_title, count(*) as num_edits FROM recentchanges WHERE rc_namespace = 0 GROUP BY 1 ORDER BY 2 DESC LIMIT 50;"""
	cur.execute( query )
	content = []
	content.append( ['most_edited_page_last_month-title', 'most_edited_page_last_month-editcount'] )
	for row in cur.fetchall() :
		content.append( [ linkify( row[0], '0' ), row[1] ] )
	text = display_report( 'ta', content, 'most_edited_page_last_month-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'most_edited_page_last_month-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

article_by_size()
most_edited_page_last_month()
