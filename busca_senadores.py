# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests

class Senator:
	"""Senator Class contains senator's data"""
	def __init__(self, name, state, party, email, twitter, phone, url):
		self.name = name
		self.state = state
		self.party = party
		self.email = email
		self.twitter = twitter
		self.phone = phone
		self.url = url
	def csvify(self):
		return self.name, self.state, self.party, self.email, self.twitter, self.phone, self.url

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

def get_content(soup):
	if isinstance(soup, BeautifulSoup):
		if soup.contents.contents:
			return get_content(soup.contents)
		else:
			return str(soup)

def unlist(lista):
	if isinstance(lista,list):
		if len(lista)==1:
			return lista[0]
	return lista

# PRI
http://pri.senado.gob.mx/integrantes-2/
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
		sen = Senator(name, state, party, email, twitter, phone,url)
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
				sen = Senator(name, state, party, email, twitter, phone,a["href"])
				senators_list.append(sen)
			except:
				print "Sin Nombre"

# PRD
http://prd.senado.gob.mx/cs/semblanza.php
url_base = "http://prd.senado.gob.mx/cs/"
url = url_base + "semblanza.php"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
all_as = soup.find_all('a',title=re.compile('^Semblanza'))
for a in all_as:
	url = url_base + a['href']
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	try:
		try:
			name = soup.find("span", {"style":"width:100%; height:180px; margin-top:15px;"}).contents
		except:
			try:
				name = soup.find("div", {"id":"sistema","style":"width:690px;float:left; padding:10px;"}).find_all("h1")[1].contents
			except:
				name = soup.find("div", {"id":"sistema","style":"width:690px;float:left; padding:10px;"}).find_all("h1")[0].contents
		try:
			state = soup.find("font", {"color":"#BDBDBD"}).contents[0]
		except:
			state = ""
		party = "PRD"
		try:
			email = soup.find("a",title=re.compile('^mailto:')).contents
		except:
			email = ""
		try:
			dirs = soup.find("div", {"id": "direccion"}).contents
			index = dirs.index(u'Teléfono:')
			phone = dirs[index+1:index+12]
		except:
			phone = ""
		try:
			twitter = soup.find("a", rel="nofollow")['href']
		except:
			twitter = ""
		sen = Senator(unlist(name).replace("<strong>","").replace("</strong>",""), unlist(state), unlist(party), unlist(email), unlist(twitter), unlist(phone),url)
		senators_list.append(sen)
	except Exception, e:
		print e

# PVEM
http://www.partidoverde.org.mx/pvem/representantes-2/
url = 'http://www.partidoverde.org.mx/pvem/representantes-2/' 
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
divs = soup.find_all("img", {"src":"http://partidoverde.org.mx/pvem/wp-content/themes/verdepad2/images/vermas.png"})
for div in divs:
	# a = div.find("a")
	a = div.parent
	r = requests.get(a['href'])
	data = r.text
	soup = BeautifulSoup(data)
	try:
		name = soup.find('a',title=re.compile('^Enlace permanente a ')).contents[0].replace("  ","").replace("\n","")
		try:
			state = unlist(soup.find("h6").contents).replace("Senador por el ","").replace("Estado de ","")
		except:
			state = ""
		party = "PVEM"
		email = ""
		phone = ""
		twitter = ""
		sen = Senator(name, state, party, email, twitter, phone,a["href"])
		senators_list.append(sen)
	except Exception, e:
 		print e

# PT
# http://dominiociudadano.org/senadores/
url = 'http://dominiociudadano.org/senadores/' 
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
divs = soup.find_all("div", {"class":"su-column"})
for div in divs:
	try:
		name = div.find("div", {"class":"su_au_name"}).contents
		try:
			state = div.find("div", {"class":"su_au_pos"}).contents[0]
		except:
			state = ""
		party = "PT"
		try:
			email = div.find("div",{"class":"su_custom_style_div",'style':"font-size:12px; color: #666;"}).contents
		except:
			email = ""
		phone = ""
		try:
			twitter = div.find("a", href=re.compile("^https://twitter.com/"))['href']
		except:
			twitter = ""
		sen = Senator(unlist(name).replace("<strong>","").replace("</strong>",""), unlist(state), unlist(party), unlist(email), unlist(twitter), unlist(phone),url)
		senators_list.append(sen)
	except Exception, e:
		print e

for sen in senators_list:
	print sen.csvify()
