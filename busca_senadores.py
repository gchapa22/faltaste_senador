# -*- coding: utf-8 -*-
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
	def csvify(self):
		return self.name, "," ,self.state, ",", self.party , ",", self.email, ",", self.twitter, ",", self.phone 

senators_list = []

estados =["Aguascalientes","Morelos","Baja California",	
		"Nayarit", "Baja California Sur", "Nuevo León",
		"Campeche",	"Oaxaca", "Coahuila", "Puebla",	
		"Colima", "Querétaro", "Chiapas", "Quintana Roo",
		"Chihuahua", "San Luis Potosí",	"Distrito Federal",	
		"Sinaloa", "Durango", "Sonora",	"Guanajuato",
		"Tabasco", "Guerrero", "Tamaulipas", "Hidalgo",	
		"Tlaxcala",	"Jalisco", "Veracruz", "Yucatán", 
		"Michoacán", "Zacatecas"]
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

# PAN
# http://www.pan.senado.gob.mx/por-estado/
url = "http://www.pan.senado.gob.mx/por-estado/"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
parent = soup.find("td",{"style":"width:300px;height:371px;align:center"})
parent = parent.find("center")
for div in parent.find_all("div"):
	if "id" in div.attrs and div['id'] != '1':
		# div = div.find("a",{"style":"overflow:auto;height:180px"})
		aas = div.find_all("a")
		for a in aas:
			r = requests.get(a["href"])
			data = r.text
			soup = BeautifulSoup(data)
			try:
				name = soup.find("p", {"class":"nombre"}).contents
				try:
					state = soup.find("p", {"class":"estadoperfil"}).contents
				except:
					state = ""
				party = "PAN"
				try:
					email = soup.find("div", {"id": "left"})[-1].contents
				except:
					email = ""
				try:
					phone = soup.find("div", {"id": "left"})[-3].contents
				except:
					phone = ""
				try:
					twitter = soup.find("a", {"class": "twitter"})["href"]
				except:
					twitter = ""
				sen = Senator(name, state, party, email, twitter, phone)
				senators_list.append(sen)
			except:
				print "Sin Nombre"

for sen in senators_list:
	print sen.name, sen.twitter
# PRD

# PVEM

# PT

# MC

# PANAL
