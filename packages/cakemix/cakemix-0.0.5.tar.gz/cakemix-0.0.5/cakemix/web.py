from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def openURL(url):
	'''
	It opens the website link and extract the page content.
	'''

	f = Request.urlopen(url)
	# Read from the object, storing the page's contents in 's'.
	s = f.readlines()
	f.close()
	return s


def getLinks(url):
	#It looks for links from the link and populates those links.
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
 
    return links



