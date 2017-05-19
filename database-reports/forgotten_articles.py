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

def forgotten_articles():

	db = MySQLdb.connect( host = 'tawiki.labsdb', user = credentials['user'], passwd = credentials['pass'], db = 'tawiki_p' )
	site = mwclient.Site( 'ta.wikipedia.org' )
	site.login( cttbot['user'], cttbot['pass'] )

	# Make the query
	cur = db.cursor()
	query = """SELECT SQL_SMALL_RESULT MAX(rev_timestamp) AS lastedit, COUNT(rev_id) AS editcount, page_title FROM revision,  	( SELECT rev_timestamp as lastedit,page_id,page_title  FROM page, revision WHERE page_id IN ( SELECT page_id FROM page WHERE page_namespace = 0 AND page_is_redirect = 0 AND NOT EXISTS ( SELECT 1 FROM page_props WHERE pp_page=page_id AND pp_propname = 'disambiguation' ) AND page_id < 51000) AND rev_id=page_latest  ORDER BY lastedit ASC LIMIT 500 ) as InnerQuery  WHERE rev_page=page_id  GROUP BY page_id  ORDER BY lastedit ASC;"""
	cur.execute( query )
	content = [ ['forgotten-articles-title', 'forgotten-articles-last-edited', 'forgotten-articles-editcount'] ]
	for row in cur.fetchall():
		content.append( [ linkify( row[2], 0 ), datetime.datetime.strptime( row[0],'%Y%m%d%H%M%S'), row[1] ] )

	# Format the data as wikitext
	text = display_report( 'ta', content, 'forgotten-articles-desc' )
	dict_obj = i18n.lang_dicts[ str( 'tadict') ]
	reports_base_url = dict_obj[ str( 'reports_base_url' ) ]
	report_title = dict_obj[ str( 'forgotten-articles-page-title' ) ]
	posturl = str(reports_base_url) + str(report_title)
	page = site.Pages[ posturl.decode('utf-8') ]
	page.save( text, summary = dict_obj[ 'summary' ] , minor=True)

forgotten_articles()
