import bs4
from bs4 import BeautifulSoup
import webbrowser
from sys import stdout
import sys
import time
from const import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_element(el,driver,method):
	"""Check if element exists """
	try:
		if method == "xpath":
			driver.find_element_by_xpath(el)
		elif method == "css" :
			driver.find_element_by_css_selector(el)
	except NoSuchElementException:
		return False
	return True


def get_address(driver,address_list):
	count = 0
	not_found = 0
	time.sleep(3) #1.2

	for i in range(0,20):
		count+=1
		xpath_address ="/html/body/jsl/div[3]/div[9]/div[7]/div/div[1]/div/div/div[4]/div[1]/a["+str(count+i)+"]/div[2]/div[1]/div[2]/span[6]"
		xpath2 = 	   "/html/body/jsl/div[3]/div[9]/div[7]/div/div[1]/div/div/div[2]/div[1]/a["+str(count+i)+"]/div[2]/div[1]/div[2]/span[6]"

		if check_element(xpath_address,driver,"xpath"):
			address_list.append(driver.find_element_by_xpath(xpath_address).text)

		elif check_element(xpath2, driver, "xpath"):
			address_list.append(driver.find_element_by_xpath(xpath2).text)
		else:
			not_found+=1
	return address_list,not_found # [str], int



def change_page(driver):
	next_button = "html body.keynav-mode-off.screen-mode jsl div#app-container.vasquette.pane-open-mode div#content-container div#pane div.widget-pane.widget-pane-visible div.widget-pane-content.scrollable-y div.widget-pane-content-holder div.section-layout.section-layout-root div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical div.n7lv7yjyC35__root div.gm2-caption div div.n7lv7yjyC35__right button#n7lv7yjyC35__section-pagination-button-next.n7lv7yjyC35__button.noprint img.n7lv7yjyC35__button-icon"
	if check_element(next_button, driver,"css"):
		button = driver.find_element_by_css_selector(next_button)
		driver.execute_script("arguments[0].click();", button)
		return True
	else:
		print("# No next button found")
		return False

def scrape_addresses(driver,query: str) -> [str]: 
	"""Use selenium to return a list of addresses"""
	query.replace(" ", "+")
	url = "https://www.google.fr/maps/search/"+query+"/13z"
	driver.get(url)
	address_list = []

	while 1:
		address_list,not_found = get_address(driver,address_list)
		a = change_page(driver)
		if a is False or not_found > 10:
			break
	driver.quit()
	if len(list(set(address_list)))+10 <= len(address_list):
		return None
	else:
		return list(set(address_list))


# found at https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 
