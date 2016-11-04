import bs4, webbrowser, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np
import urllib2, pickle
import pandas as pd


# This scraper logs into Strava and compiles a dataset of all athletes who participated 
# in the designated challenge. It takes about 30 hrs to run.


def loginStrava():
	challengeUrl = "https://www.strava.com/challenges/strava-races-half-marathon-2016-7"
	global browser
	browser = webdriver.Firefox()
	browser.get(challengeUrl)

	login = browser.find_element_by_link_text('Log In')
	login.click()
	time.sleep(3)

	rememberMe = browser.find_element_by_id('remember_me')
	rememberMe.click()
	time.sleep(2)

	login = browser.find_element_by_link_text('Log in using Facebook')
	login.click()
	time.sleep(3)

	userElem = browser.find_element_by_id('email')
	userElem.send_keys("rudygilman@gmail.com")
	passElem = browser.find_element_by_id('pass')
	passElem.send_keys("1hatefaceb00k")
	time.sleep(2)

	login = browser.find_element_by_id('loginbutton')
	login.click()
	time.sleep(3)


# This list of athlete urls was was compiled earlier
hrefList = pd.read_pickle("stravaUrls.txt")
hrefList['url'] = hrefList.index
hrefDf = hrefList #.sample(10, random_state=14)

loginStrava()

print "there are this many links to click: ", len(hrefDf)

df = pd.DataFrame({})
browser = webdriver.Firefox()

# going through list of urls and compiling df, saving it as pickled df.
for l in range(len(hrefDf)): 

	time.sleep(np.random.normal(5, 1))
	print np.random.normal(5, 1)
	print "iteration number: ", l

	baseUrl = hrefDf.url.iloc[l]
	browser.get(baseUrl)
	time.sleep(3)

	try:
		runBtn = browser.find_element(By.CSS_SELECTOR, "a.button.btn-xs.running-tab")
		runBtn.click()
	except:
		print "Run btn already clicked"
		
	try:
		bigParagraph = browser.find_element(By.CSS_SELECTOR, "div.section.comparison.borderless").text
	except:
		bigParagraph = ''
		print "NO DIV.SECTION.borderless found"		

	try:
		name = str(browser.find_element(By.CSS_SELECTOR, "h2.h1").text)
	except:
		name = ''

	if "10k" not in bigParagraph:
		print name, "IS NOT A RUNNER"
		continue

	v = browser.find_elements(By.CSS_SELECTOR, "td")

	d = {}

	for i in range(len(v)-2):

		try:
			e = str(v[i].text)
		except:
			e=''
		try:
			n = str(v[i+1].text)
		except:
			n = ''
		try:
			nn = str(v[i+2].text)
		except:
			nn = ''

		if "10k" == e:
			d['10k'] = n
		if "Marathon" == e:
			d[e] = n
		if "5k" == e:
			d[e] = n
		if "Half-Marathon" == e:
			d[e] = n
		if "Time" == e:
			d[e] = n
		if ("Distance" == e) & ("Time" == nn):
			d[e] = n
		if "Elev Gain" == e:
			d[e] = n

	d = pd.DataFrame(d, index=[0])
	d['url'] = baseUrl
	d['name'] = name
	d['stravaPro'] = 0
	d['ageGroup'] = hrefDf.age.iloc[l]
	d['weightGroup'] = hrefDf.weights.iloc[l]
	d['sex'] = hrefDf.sex.iloc[l]

	print d

	df = df.append(d)

	df.to_pickle("stravaScraperChallenge.txt")

print df



# Here are some tools used to set up scraper. Don't really need them now.

""" 
#############################################################################
#                   for getting list of href links from Strava pros page:
#############################################################################


prosUrl = "https://www.strava.com/pros"
browser = webdriver.Firefox()
browser.get(prosUrl)
linkList = browser.find_elements(By.CSS_SELECTOR, "a.minimal") 
print len(linkList)
hrefList = []

for l in linkList:
	#name = str(l.text)
	try:
		link = l.get_attribute("href")
		hrefList.append(link)
	except:
		continue

print hrefList
pickle.dump(hrefList, open("hrefList.txt", "wb"))
"""

"""
hrefList = pickle.load(open("hrefList.txt", "rb"))
print "there are this many links to click: ", len(hrefList)

df = pd.DataFrame({})
browser = webdriver.Firefox()

for l in range(len(hrefList)): # got to 348 last time

	time.sleep(np.random.normal(5, 1))
	print np.random.normal(5, 1)
	print "iteration number: ", l

	baseUrl = hrefList[l]
	browser.get(baseUrl)
	bigParagraph = browser.find_element(By.CSS_SELECTOR, "div.section.comparison.borderless").text
	name = browser.find_element(By.CSS_SELECTOR, "h2.h1").text

	if "10k" not in bigParagraph:
		print name, "IS NOT A RUNNER"
		continue

	v = browser.find_elements(By.CSS_SELECTOR, "td")

	d = {}
	for i in range(len(v)-2):

		e = str(v[i].text)
		n = str(v[i+1].text)

		if "10k" == e:
			d['10k'] = n
		if "Marathon" == e:
			d[e] = n
		if "5k" == e:
			d[e] = n
		if "Half-Marathon" == e:
			d[e] = n
		if "Time" == e:
			d[e] = n
		if ("Distance" == e) & ("Time" == str(v[i+2].text)):
			d[e] = n
		if "Elev Gain" == e:
			d[e] = n

		print str(v[i].text)
		#print f.get_attribute('textContent')
		#print browser.execute_script("return arguments[0].textContent", f)
	d = pd.DataFrame(d, index=[0])
	d['url'] = baseUrl
	d['name'] = str(name)
	d['stravaPro'] = 1

	df = df.append(d)

	df.to_pickle("stravaScraper.txt")

print df
"""




"""

######################################################################
#                   By age group
######################################################################
ages = ['24 and under','25 to 34', '25 to 34', '35 to 44', '45 to 54', '55 to 64', '65 and over']
weights = ['124 lbs and under', '125 to 149 lbs', '150 to 164 lbs', '165 to 179 lbs', '180 to 199 lbs', '200 lbs and over']
sexes = ["input#filter_male", "input#filter_female"]
df = pd.DataFrame({})

def bySex():
	df = pd.DataFrame({})
	for s in range(len(sexes)):
		overall = browser.find_element(By.CSS_SELECTOR, "li#overall-tab")
		overall.click()
		time.sleep(np.random.normal(15,2))

		bySex = browser.find_element(By.CSS_SELECTOR, sexes[s])
		bySex.click()
		time.sleep(np.random.normal(15,2))

		for p in range(0, 200, 2):
			print sexes[s], p
			linkList = browser.find_elements(By.CSS_SELECTOR, "a")
			for l in linkList:
				try:
					link = l.get_attribute("href")
					print link
					if "athletes" in link:
						print "GOT ONE" 
						entry = pd.DataFrame({"sex":sexes[s]}, index=[link])
						df = df.append(entry)
				except:
					continue
			print "LINKLIST LENGTH", len(linkList)
			try:
				nextPage = browser.find_element(By.CSS_SELECTOR, "a.button.next_page")
				nextPage.click()
				time.sleep(np.random.normal(15,2))
			except:
				break
	print df
	df.to_pickle("stravaChallengeBySex.txt")

def byAge():
	df = pd.DataFrame({})
	for a in range(len(ages)):
		byAge = browser.find_element(By.CSS_SELECTOR, "li#age-tab")
		byAge.click()
		time.sleep(15)

		ageGroups = browser.find_element(By.CSS_SELECTOR, "div.drop-down-menu.small.enabled")
		ageGroups.click()
		time.sleep(5)

		ageGroup = browser.find_element_by_link_text(ages[a])
		ageGroup.click()
		time.sleep(15)

		for p in range(0, 80, 2):
			print ages[a], p
			linkList = browser.find_elements(By.CSS_SELECTOR, "a")
			for l in linkList:
				try:
					link = l.get_attribute("href")
					print link
					if "athletes" in link:
						print "GOT ONE" 
						entry = pd.DataFrame({"age":ages[a]}, index=[link])
						df = df.append(entry)
				except:
					continue
			print "LINKLIST LENGTH", len(linkList)
			try:
				nextPage = browser.find_element(By.CSS_SELECTOR, "a.button.next_page")
				nextPage.click()
				time.sleep(np.random.normal(15,2))
			except:
				break
	print df
	df.to_pickle("stravaChallengeByAge.txt")

def byWeight():
	df = pd.DataFrame({})
	for a in range(len(weights)):
		byWeight = browser.find_element(By.CSS_SELECTOR, "li#weight-tab")
		byWeight.click()
		time.sleep(15)

		weightGroups = browser.find_element(By.CSS_SELECTOR, "div.drop-down-menu.small.enabled")
		weightGroups.click()
		time.sleep(5)

		weightGroup = browser.find_element_by_link_text(weights[a])
		weightGroup.click()
		time.sleep(15)

		for p in range(0, 80, 2):
			print weights[a], p
			linkList = browser.find_elements(By.CSS_SELECTOR, "a")
			for l in linkList:
				try:
					link = l.get_attribute("href")
					print link
					if "athletes" in link:
						print "GOT ONE" 
						entry = pd.DataFrame({"weights":weights[a]}, index=[link])
						df = df.append(entry)
				except:
					continue
			print "LINKLIST LENGTH", len(linkList)
			try:
				nextPage = browser.find_element(By.CSS_SELECTOR, "a.button.next_page")
				nextPage.click()
				time.sleep(np.random.normal(15,2))
			except:
				break
	print df
	df.to_pickle("stravaChallengeByWeight.txt")

#byWeight()
#byAge()			
#bySex()

a = pd.read_pickle("stravaChallengeByAge.txt")
a['url'] = a.index
a = a.drop_duplicates(subset='url')

w = pd.read_pickle("stravaChallengeByWeight.txt")
w['url'] = w.index
w = w.drop_duplicates(subset='url')

s = pd.read_pickle("stravaChallengeBySex.txt")
s['url'] = s.index
s = s.drop_duplicates(subset='url')

df = pd.concat([a,w,s], axis=1)[['sex', 'weights', 'age']]

df = df[(df.index!="https://www.strava.com/athletes/10319226")&(df.index!="https://www.strava.com/athletes/search")]
df = df.dropna()
df.to_pickle("stravaUrls.txt")
"""
