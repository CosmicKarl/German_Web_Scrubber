from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

link = 'http://connect.mheducation.com/connect/jsp/html/hm/selfstudy.jsp?logout=true&navclick=true&node=connect_app_8_16'
delay = 10
driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get(link)

usrElement = self.wait_until(By.ID, 'userName')
pwdElement = driver.find_element_by_id("password")
#Log into Connect
usrElement.send_keys('mycast@verizon.net')
pwdElement.send_keys('IsE@12345')
pwdElement.send_keys(Keys.ENTER)
print "Log in succes"

#Click german book
driver.find_element_by_xpath('//*[@id="list_2747337_item_15168696_text"]/div[3]/div/div[2]/a').click()
print "German Book click succes"

#Click library
driver.find_element_by_xpath('//*[@id="container_inner"]/div[3]/div/div/div/ul[1]/li[2]/a/span[2]').click()
print "Click library succes"

#Click book again to load it
time.sleep(5)
book = wait_until(By.CLASS_NAME,'textbook-image-container-tbo-lib-30')
ele_to_click = driver.find_element_by_xpath('//*[@id="middleContainer"]/div[2]/div/div/div[1]/div[2]/div[1]/a[2]')
ActionChains(driver).move_to_element(book).click(ele_to_click).perform()
driver.execute_script("arguments[0].setAttribute('style','visibility:visible;')",book)
driver.execute_script('arguments[0].click();',book)
print_to_file()
print "Click book again success"

#switch iframe to table to extract info
frame = wait_until(By.TAG_NAME, 'iframe')
driver.switch_to_frame(frame)
driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
print "Iframe switch"



#driver.find_element_by_xpath('//*[@id="toolbar_jumppg"]').send_keys('18').send_keys(keys.ENTER)
#print "changed to page 18"

"""
Waits until element is present on page then returns that element
"""
def wait_until(by_atr, ele):
	element_present = EC.presence_of_element_located((by_atr, ele))
	return WebDriverWait(driver, delay).until(element_present)


"""
Testing
"""
def print_to_file(static={'count':0}):
	s = BeautifulSoup(driver.page_source,'lxml')
	f = open('out'+str(static['count'])+'.html','w')
	f.write(s.prettify().encode('utf-8'))
	f.close()
	driver.save_screenshot('out'+str(static['count'])+'.png')
	static['count']+=1
