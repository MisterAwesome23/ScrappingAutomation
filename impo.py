from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options
from scraper_api import ScraperAPIClient
from io import BytesIO
from PIL import Image
from azcaptchaapi import AZCaptchaApi
import json
api = AZCaptchaApi('wft6rhgpcqfypjznl2kc9yzbdwb73dhn')


'''
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
'''

UID = "U70109GJ2019PLC107623"     
driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1920,1080) # optional
driver.get('http://www.mca.gov.in/mcafoportal/prosecutionDetailsAction.do') 

user_input= driver.find_element_by_id('companyID')
user_input.send_keys("U70109GJ2019PLC107623")

driver.save_screenshot('screenshot.png') # save a screenshot to disk
screen = driver.get_screenshot_as_png()

# box = (1007,400, 1260, 477)
# im = Image.open(BytesIO(screen))
# region = im.crop(box)
# region.save('screen7.png', 'PNG', optimize=True, quality=95)


# with open(r"screen7.png", 'rb') as captchaf:
#     captcha = api.solve(captchaf)

# print(captcha.await_result())

# user_input= driver.find_element_by_id("userEnteredCaptcha")
# user_input.send_keys(captcha.await_result())
# driver.save_screenshot('screenshot1.png')

# #hitting submit button
# login_button = driver.find_element_by_id("submitBtn")
# login_button.click()
# driver.save_screenshot('screenshot2.png')


# #using bs4 for scarping the table from next page
# soup_level1=BeautifulSoup(driver.page_source, 'lxml')

# table1 = soup_level1.find(id="signatoryDetails")

# df = pd.read_html(str(table1),header=0)
# # print(df[0])

# df[0].to_json('temp.json', orient='records', lines=True)

# driver.close()

