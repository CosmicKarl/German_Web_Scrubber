#!/usr/bin/env python

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import itertools
import csv
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class ConnectJobScraper(object):
	link = 'http://connect.mheducation.com/connect/jsp/html/hm/selfstudy.jsp?logout=true&navclick=true&node=connect_app_8_16'
	delay = 10
	pages = [18,49,81,109,140,170,200,228,254]

	def __init__(self):
		self.driver = webdriver.PhantomJS()
		#self.driver = webdriver.Chrome()
		self.driver.set_window_size(1120, 550)
		self.driver.get(self.link)


	"""
	Manualy logs into connect and take you to the correct link to be parsed
	"""
	def log_in(self):
		usrElement = self.wait_until(By.ID, 'userName')
		#usrElement = self.wait_until(By.ID, 'usr')
		pwdElement = self.driver.find_element_by_id("password")
		#pwdElement = self.driver.find_element_by_id("pwd")
		#Log into Connect
		usrElement.send_keys('EMAIL GOES HERE')
		pwdElement.send_keys('PWD GOES HERE')
		pwdElement.send_keys(Keys.ENTER)
		print "Log in succes"

		#Click german book
		self.driver.find_element_by_xpath('//*[@id="list_2747337_item_15168696_text"]/div[3]/div/div[2]/a').click()
		print "German Book click succes"

		#Click library
		self.driver.find_element_by_xpath('//*[@id="container_inner"]/div[3]/div/div/div/ul[1]/li[2]/a/span[2]').click()
		print "Click library succes"

		#Click book again to load it
		book = self.wait_until(By.CLASS_NAME,'textbook-image-container-tbo-lib-30').find_element_by_css_selector('a:nth-child(1)').click()
		print "Click book again success"

		#switch to iframe to be able to extract indo from table
		time.sleep(5)
		frame = self.wait_until(By.TAG_NAME, 'iframe')
		self.driver.switch_to_frame(frame)
		print "Iframe switch"

	"""
	Waits until element is present on page then returns that element
	"""
	def wait_until(self, by_atr, ele):
		element_present = EC.presence_of_element_located((by_atr, ele))
		return WebDriverWait(self.driver, self.delay).until(element_present)
		

	"""
	Testing
	"""
	def print_to_file(self,static={'count':0}):
		s = BeautifulSoup(self.driver.page_source,'lxml')
		f = open('./out/out'+str(static['count'])+'.html','w')
		f.write(s.prettify().encode('utf-8'))
		f.close()
		self.driver.save_screenshot('./out/out'+str(static['count'])+'.png')
		static['count']+=1

	def change_page(self,page):
		#change page to extract info
		tb_page = self.driver.find_element_by_xpath('//*[@id="toolbar_jumppg"]')
		tb_page.clear()
		tb_page.send_keys(str(page))
		self.driver.find_element_by_id('toolbaricon_jumpgo').click()
		time.sleep(2)
		print "changed to page ", str(page)

		
	"""
	Scrapes vocab into dictionary
	"""
	def scrape_vocab(self,page):
		try:
			self.change_page(page)

			s = BeautifulSoup(self.driver.page_source,'lxml')
			cardSet = {}

			#Grab title for this card set
			cardSet['title'] = ''.join(s.find_all("div",id=("maincaption"))[0].get_text().split())

			#grab only all the tables with vocab
			tables = s.find_all('div', {'class':'ch_end'})

			cardSet['ger'] = []
			cardSet['eng'] = []

			#Grab each vocab pair
			for table in tables:
				for tr in table.find_all('tr'):
					data = tr.find_all('td')

					#deal with row with only one element
					if len(data) > 1:
						cardSet['ger'].append(' '.join((data[0].get_text().split())))
						cardSet['eng'].append(' '.join((data[1].get_text().split())))
					elif len(data) == 1:
						#print ' '.join((data[0].get_text().split())) 
						cardSet['ger'].append(' '.join((data[0].get_text().split())))
						cardSet['eng'].append(' ')

			self.write_card_set_file(cardSet)
		except:
			self.print_to_file()
			print "Failed to read %d  page" %(page)

	"""
	Save cards to csv file
	"""
	def write_card_set_file(self, cardSet):
		csvfile = open('./csv/' + str(cardSet['title']) + '.csv','w')
		writer = csv.writer(csvfile)
		for ger,eng in itertools.izip_longest(cardSet['ger'], cardSet['eng']):
			writer.writerow((str(ger), '\t', str(eng)))

		print "Done writing "+ str(cardSet['title']) +  " to file"
		csvfile.close()
		

	"""
	Print results
	"""
	def scrape(self):
		self.log_in()
		map(self.scrape_vocab,  self.pages)
		self.driver.close()


if __name__ == '__main__':
	scraper = ConnectJobScraper()
	scraper.scrape()
