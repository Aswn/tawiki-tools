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
	elif namespace is 0:
		return '[[' + title_clean + ']]'
	elif namespace is 6:
		return '[[:{{subst:ns:%s}}:%s]]' % ( namespace, title_clean )
	elif namespace is 14:
		return '[[:{{subst:ns:%s}}:%s]]' % ( namespace, title_clean )
	else:
		return '[[:{{subst:ns:%s}}:%s]]' % ( namespace, title_clean )

def pages_with_most_revisions():

	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )

	# Make the query
	cur = db.cursor()
	query = """SELECT COUNT(*) AS revisions, rev_page, p.page_namespace, p.page_title FROM revision r LEFT JOIN ( SELECT page_id, page_title, page_namespace FROM page ) p ON r.rev_page = p.page_id GROUP BY rev_page ORDER BY revisions DESC  LIMIT 1000;"""
	cur.execute( query )
	content = [ ['pagerevisions-namespace', 'pagerevisions-title', 'pagerevisions-revisions'] ]
	for row in cur.fetchall():
		content.append( [ row[2], linkify( row[3], str(row[2]) ), row[0] ])

	# Format the data as wikitext
	text = display_report( 'ta', content, 'pagerevisions-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'pagerevisions-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

pages_with_most_revisions()
