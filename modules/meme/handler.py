from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from datetime import datetime
import time
import urllib2
import unicodedata
import re

class MemeHandler:
	def __init__(self):
		pass
	def privmsg(self, user, channel, msg):
		msg = msg.strip()
		if msg.startswith('!meme '):
			query = msg[6:]
			print
			print 'query:',query
			meme = query_meme(query)
			if meme:
				line = meme.encode('utf-8', 'ignore')
				print 'found:',line[:line.find(':')]
			else:
				print 'found: nothing :('
				line = 'sorry, fant ikke mem.. :( '
			return [line]

def fetch(url):
	opener = urllib2.build_opener()
	opener.addheaders = [("User-agent", "meme-bot")]
	response = opener.open(url)
	return response.read()

def mangle(string):
	""" Hacky fix for Twisted unicode issues and general charset conversion problems.
	"""
	return reduce(lambda x,y: x+y, map(unicode,string)).decode("utf-8").encode("utf-8")

def search_meme(query):
	"""Search knowyourmeme.com and retrieve name of first hit"""
	query = '+'.join(query.split(' '))
	doc = fetch('http://knowyourmeme.com/search/memes?q='+query)
	soup = BeautifulSoup(doc)
	hits = soup.findAll('td',{'class':re.compile('^entry_')})
	if not hits:
		# No search results :(
		return None
	return hits[0].h2.a['href'].replace('/memes/','')

def fetch_meme(query):
	"""Fetch information about a given meme"""
	doc = fetch('http://knowyourmeme.com/memes/'+query)
	soup = BeautifulSoup(doc)
	content = soup.find('div',{'id':'maru'})
	meme_title = content.header.h1.a.string
	ps = content.find('div',id='entry_body').findAllNext('p')
	meme_content = ''
	for p in ps:
		text = ''.join(p(text=True))
		meme_content += text
		if len(meme_content) > 100:
			break
	meme_content = BeautifulStoneSoup(meme_content,convertEntities=
					BeautifulStoneSoup.HTML_ENTITIES).contents[0] # htmlentities -> unicode
	return meme_title, meme_content

def query_meme(query):
	"""Return information about meme most relevant to query from knowyourmeme.com"""
	exact_name = search_meme(query)
	if exact_name is None:
		return None
	title, desc = fetch_meme(exact_name)
	return title+': '+desc

if __name__ == "__main__":
	""" For testing """
	#~ print query_meme('yo dawg')
	#~ print query_meme('rebecca black')
	#~ print query_meme('lolcat')
	print query_meme('leave britney alone')
