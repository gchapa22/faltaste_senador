#Carwler sencillo hecho con beautifulsoup http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup

import requests

url_base = "http://www.senado.gob.mx/"
url_initial = url_base + "?ver=sen&mn=7"

r = requests.get(url_initial)
data = r.text
soup = BeautifulSoup(data)

parent_div = soup.find("div", {"id": "contenido_informacion"})
table = parent_div.find("table")
last_period = table.find_all('a')[-1]

period_url = url_base + last_period['href']

r = requests.get(period_url)
data = r.text
soup = BeautifulSoup(data)

parent_div = soup.find("div", {"id": "main-content"})
table = parent_div.find("table")
last_day = table.find_all('a')[-1]

url_day = url_base + last_day['href']

r = requests.get(url_day)
data = r.text
soup = BeautifulSoup(data)

parent_div = soup.find("div", {"id": "contenido_informacion"})
table = parent_div.find_all("table")[3]

abscents = []

for tbody in table.find_all("tbody"):
	tr = tbody.find("tr")
	if "AUSENTE" in tr.find_all("td")[-1].find("div").find("strong"):
		abscents.append([tr.find_all("td")[0].find('a').contents, url_base + tr.find_all("td")[0].find('a')['href']]) 

abscents
