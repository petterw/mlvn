# author: github.com/snorrec
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time
import urllib2
import unicodedata

class NewsHandler:
	def __init__(self):
		pass
	def privmsg(self, user, channel, msg):
		if "!nyheter" in msg:
			site = "http://www.vg.no/rss/create.php"
			lines = ["*** Nyheter fra VG RSS ***"]
			lines.extend(get_news(site))
			return lines

def fetch(url):
	opener = urllib2.build_opener()
	opener.addheaders = [("User-agent", "snorrec-newsbot")]
	response = opener.open(url)
	return response.read()

def mangle(string):
	"""Strip non ascii chars
	"""
	return reduce(lambda x,y: x+y, map(unicode,string)).decode("utf-8").encode("utf-8")

def extract_news(doc):
	soup = BeautifulSoup(doc)
	titles = []
	descriptions = []
	links = []
	times = []

	news = {"titles":titles, "descriptions":descriptions, "links":links, "times":times}

	for title in soup.findAll("title"):
		if("VG RSS" not in title and "VG RSS " not in title):
			titles.append(mangle(title))

	for description in soup.findAll("description"):
		if("VG RSS" not in title and "VG RSS " not in description):
			descriptions.append(mangle(description))

	for link in soup.findAll("guid"):
		links.append(mangle(link))

	for a in soup.findAll("pubdate"):
		times.append(mangle(a)[17:22])

	return news

def get_news(url):
	print "fetching stuff..."
	news = extract_news(fetch(url))

	#Formatting
	news_lines = []

	for i in xrange(len(news["titles"])):
		news_lines.append("("+news["times"][i]+")" +" "+news["titles"][i] +"- " + news["links"][i])
		#news_lines.append(news["descriptions"][i])
		#news_lines.append("")

	print "done"
	return news_lines

if __name__ == "__main__":
	site = "http://www.vg.no/rss/create.php"
	news_lines = get_news(site)
	for line in news_lines:
		print line
