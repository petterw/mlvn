# author: github.com/emagnus
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import NavigableString
from BeautifulSoup import BeautifulSoup

import urllib2
import urllib
import unicodedata

class DefineHandler:
	def __init__(self):
		pass
	def privmsg(self, user, channel, msg):
		msg = msg.split(" ")
		if msg[0] == "!define":
			line = udquery(msg[1:])
			return [line]
		return []

def fetch(url):
    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", "defino")]
    response = opener.open(url)
    return response.read()

def udquery(query):
    """ Prepare and query urban dictionary
    """
    queryurl = "+".join(urllib.quote(q, '') for q in query)
    url = "http://www.urbandictionary.com/define.php/?term="+queryurl
    soup = BeautifulSoup(fetch(url))    
    try:
        html = extract_text(soup.find("div",{"class":"definition"}).contents).replace("\r","")
        text = BeautifulStoneSoup(html,convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
        text = shortify(text,400)
        definition = unicode(text).decode("utf-8").encode("utf-8")
    except:
        definition = "Ingen definisjon."
    return definition

def extract_text(contents):
    if type(contents).__name__ == 'list':
        s = ""
        for c in contents:
            if type(c) != NavigableString:
                c = extract_text(c.contents)
            s += unicode(c)
        return s
    if type(contents) == NavigableString:
        return contents

def shortify(text, charlimit):
    if len(text) > charlimit:
        short = text[:text.rfind(".",0,charlimit)+1]
        if len(short) > 40:
            return short
    return text 
