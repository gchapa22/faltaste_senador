from bs4 import BeautifulSoup

import requests

class Senator:
	"""Senator Class contains senator's data"""
	def __init__(self, name, state, party, email, twitter, phone):
		self.name = name
		self.state = state
		self.party = party
		self.email = email
		self.twitter = twitter
		self.phone = phone

senators_list = []

# PRI
# http://pri.senado.gob.mx/integrantes-2/
url = "http://"+"pri.senado.gob.mx/integrantes-2/"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

parent = soup.find("ul", {"class":"wpmtp-filterable wpmtp-four-columns wpmtp-icon-show-before"}) 

for li in parent:
	url = li.find_all("a")[1]["href"]
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	try:
		name = soup.find("h2", {"class":"entry-title"}).contents[0]
		try:
			state = soup.find("h2", {"class":"entry-title"}).contents[2]
		except:
			state = ""
		party = "PRI"
		try:
			email = soup.find("span", {"class": "wpmtp-meta wpmtp-meta-email"}).find("a").contents
		except:
			email = ""
		try:
			phone = soup.find("span", {"class": "wpmtp-meta wpmtp-meta-contact"}).contents
		except:
			phone = ""
		try:
			twitter = soup.find("a", {"class": "wpmtp-twitter"})["href"]
		except:
			twitter = ""
		sen = Senator(name, state, party, email, twitter, phone)
		senators_list.append(sen)
	except:
		print "Sin Nombre"

for sen in senators_list:
	print sen.name, sen.twitter
# PAN

# PRD

# PVEM

# PT

# MC

# PANAL
