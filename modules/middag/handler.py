# author: github.com/petterw
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import urllib2

class MiddagHandler:
	def __init__(self):
		self.sites = sites = {
				"Realfag":"http://www.sit.no/content/36447/Ukas-middagsmeny-pa-Realfag", 
				"Hangaren":"http://www.sit.no/content/36444/Ukas-middagsmeny-pa-Hangaren"}
	def privmsg(self, user, channel, msg):
		return todays_menu(self.sites)
	
def fetch(url):
	opener = urllib2.build_opener()
	opener.addheaders = [("User-agent", "sit-dinner-bot")]
	response = opener.open(url)
	return response.read()

def mangle(string):
	""" Hacky fix for Twisted unicode issues and general charset conversion problems.
		ugh
	"""
	return reduce(lambda x,y: x+y, map(ut, string))

def ut(string):
	try:
		return unicode(string)
	except:
		return string

def extract_menu(doc):
	""" Input: html from sit.no with a menu table, output: menu as list
	"""
	soup = BeautifulSoup(doc)
	menu = []
	for tag in soup.findAll("table", {"id":"menytable"}):
		for table in tag.findAll("table"):
			day_menu = []
			day_prices = []
			for item in table.findAll("td", {"class":"menycelle"}):
				day_menu.append(mangle(BeautifulSoup(item.prettify().replace("\n","")).findAll("td")[0].contents))
			for item in table.findAll("td", {"class":"priscelle"}):
				day_prices.append(mangle(BeautifulSoup(item.prettify().replace("\n","")).findAll("td")[0].contents))
			menu.append(zip(day_menu,day_prices))
	return menu
		
def todays_menu(urls):
	""" Given a set of URLs pointing to menu pages on sit.no, this returns todays menu as a list of lists, containing lines
		for the IRC bot to display.
	"""
	print "Henter meny.."
	today = datetime.now().weekday()
	if today > 4:
		return ["Kantina er stengt i helgene."]
	r = []
	for title in urls.keys():
		r.append(title)
		try:
			lines =  extract_menu(fetch(urls[title]))[today]
			for x in xrange(len(lines)):
				r.append(str(x+1)+". " + lines[x][0] + ", "+lines[x][1])
		except:
			r.append("Feil under henting av meny :(")
	print ".. ferdig"
	return r

if __name__ == "__main__":
	""" For testing """
	sites = { "Realfag":"http://www.sit.no/content/36447/Ukas-middagsmeny-pa-Realfag", "Hangaren":"http://www.sit.no/content/36444/Ukas-middagsmeny-pa-Hangaren"}
	for l in todays_menu(sites):
		print l
