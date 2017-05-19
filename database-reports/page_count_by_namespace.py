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

def page_count_by_namespace():

	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )

	# Make the query
	cur = db.cursor()
	query = """SELECT page_namespace, COUNT(*) AS total, SUM(page_is_redirect) AS redirect FROM page GROUP BY page_namespace;"""
	cur.execute( query )
	content = [ ['pagecount-namespace', 'pagecount-namespace-name', 'pagecount-total', 'pagecount-redirect', 'pagecount-non-redirect'] ]
	for row in cur.fetchall():
		content.append( [ row[0], '{{subst:ns:' + str( row[0] ) + '}}', row[1], row[2], row[1]-row[2] ])

	# Format the data as wikitext
	text = display_report( 'ta', content, 'pagecount-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'pagecount-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

page_count_by_namespace()
