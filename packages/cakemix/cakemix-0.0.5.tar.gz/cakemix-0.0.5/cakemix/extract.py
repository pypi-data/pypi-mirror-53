from bs4 import BeautifulSoup
import urllib
import re

html_page = urllib.urlopen("https://arstechnica.com")
soup = BeautifulSoup(html_page)
for link1 in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    print(link1.get('href'))

