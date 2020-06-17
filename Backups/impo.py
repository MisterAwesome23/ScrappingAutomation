from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options
from scraper_api import ScraperAPIClient



#URL="http://api.scraperapi.com/?api_key=76be91c5f3d06fe7644e6023ca478936&url=http://www.mca.gov.in/mcafoportal/showEnquireDIN.do"
DIN_no = "00000001"

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional
driver.get('http://www.mca.gov.in/mcafoportal/showEnquireDIN.do') 
driver.save_screenshot('screen.png') # save a screenshot to disk

user_input= driver.find_element_by_id('DIN')
user_input.send_keys(DIN_no)

#hitting submit button
login_button = driver.find_element_by_class_name("imgButton")
login_button.click()

#using bs4 for scarping the table from next page
soup_level1=BeautifulSoup(driver.page_source, 'lxml')

table = soup_level1.find_all('table')[1]

df = pd.read_html(str(table),header=0)
print(df)
