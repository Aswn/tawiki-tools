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

def most_used_templates():

	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )

	# Make the query
	cur = db.cursor()
	query = """SELECT tl_title, COUNT(*) FROM templatelinks WHERE tl_namespace = 10 GROUP BY tl_title ORDER BY COUNT(*) DESC LIMIT 500;"""
	cur.execute( query )
	content = [ ['mostusedtemplate-title', 'mostusedtemplate-count'] ]
	for row in cur.fetchall():
		content.append([ linkify( row[0], 10 ) , row[1] ])

	# Format the data as wikitext
	text = display_report( 'ta', content, 'mostusedtemplate-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'mostusedtemplate-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

most_used_templates()
