from selenium import webdriver

from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options
from scraper_api import ScraperAPIClient
from io import BytesIO
from PIL import Image
from azcaptchaapi import AZCaptchaApi
api = AZCaptchaApi('wft6rhgpcqfypjznl2kc9yzbdwb73dhn')




def init_phantomjs_driver(*args, **kwargs):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    for key, value in headers.items():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

    driver =  webdriver.PhantomJS(*args, **kwargs)
    driver.set_window_size(1920, 1080)

    return driver

'''
def main():
    service_args = [
        '--proxy=127.0.0.1:9999',
        '--proxy-type=http',
        '--ignore-ssl-errors=true'
        ]

    driver = init_phantomjs_driver(service_args=service_args)

    driver.get('http://cn.bing.com')
'''
from flask import Flask
app = Flask(__name__)

@app.route('/mca/sigdeatails/cin=<CIN>')
def sigdeatails(CIN):
    x=1
    y=1
    count=0
    while x==1 or y==1:
            try:
           
                try:
                 
                    Cin = CIN  
                      
                    #driver = webdriver.PhantomJS() # or add to your PATH
                    driver = webdriver.Chrome('chromedriver.exe')
                    driver.set_window_size(1920,1080) # optional
                    driver.get('http://www.mca.gov.in/mcafoportal/viewSignatoryDetails.do') 
                    driver.save_screenshot('screenshot1.png') # save a screenshot to disk

                    user_input= driver.find_element_by_id('companyID')
                    user_input.send_keys("U70109GJ2019PLC107623")
                    x=0
                
                except:
                    y=0
                    print("Site failed due to blocked IP or network issue!! exiting....")

                if x==0 :
                    driver.save_screenshot('screenshot2.png') # save a screenshot to disk
                    screen = driver.get_screenshot_as_png()

                    box = (1007,400, 1260, 477)
                    im = Image.open(BytesIO(screen))
                    region = im.crop(box)
                    region.save('screen3.png', 'PNG', optimize=True, quality=95)

        
                    with open(r"screen3.png", 'rb') as captchaf:
                        captcha = api.solve(captchaf)

                    print(captcha.await_result())

                    user_input= driver.find_element_by_id("userEnteredCaptcha")
                    user_input.send_keys(captcha.await_result())
                    driver.save_screenshot('screenshot4.png')

                    #hitting submit button
                    login_button = driver.find_element_by_id("submitBtn")
                    login_button.click()
                    driver.save_screenshot('screenshot4.png')
            
                
                    #using bs4 for scarping the table from next page
                    soup_level1=BeautifulSoup(driver.page_source, 'lxml')

                    table1 = soup_level1.find(id="signatoryDetails")

                    df = pd.read_html(str(table1),header=0)
                    
                    df[0].to_json('temp1.json', orient='records', lines=True)
                    driver.close()
                    x=0
                    y=0
                x=0
            except:
                x=1
                count=count + 1
                driver.close()
                print("Failed hit ",count,"retrying now")


    return 'ALL DONE !'

@app.route('/mca/dinequiry/din=<DIN>')
def dinequiry(DIN):
   

    x = 1
    DIN_no = DIN
    try:
        service_args = []
        #driver = webdriver.Chrome('chromedriver.exe') # or add to your PATH
        #driver=webdriver.PhantomJS()
        driver = init_phantomjs_driver(service_args=service_args)
        #driver.set_window_size(1920, 1080) # optional
        driver.get('http://www.mca.gov.in/mcafoportal/showEnquireDIN.do') 
        driver.save_screenshot('screen.png') # save a screenshot to disk

        user_input= driver.find_element_by_id('DIN')
        user_input.send_keys(DIN_no)
    except:
        x=0
        print("Site Failed try again after 30 mins")
    if x!=0:
        #hitting submit button
        login_button = driver.find_element_by_class_name("imgButton")
        login_button.click()

        #using bs4 for scarping the table from next page
        soup_level1=BeautifulSoup(driver.page_source, 'lxml')

        table = soup_level1.find_all('table')[1]

        df = pd.read_html(str(table),header=0)
        df[0].to_json('temp.json', orient='records', lines=True)
    
    return "ALL DONE!"

@app.route('/mca/prosec/cin=<CIN>')
def prosec(CIN):
    cin = CIN
    
    driver = webdriver.Chrome('chromedriver.exe') # or add to your PATH
    driver.set_window_size(1920,1080) # optional
    
    driver.get('http://www.mca.gov.in/mcafoportal/fetchprosecutionDetails.do') 
    driver.save_screenshot('screen.png') # save a screenshot to disk
        
    try:
        user_input= driver.find_element_by_id("userEnteredCaptcha")
        x=1
    except:
        x=0
        
    if x==1:
        driver.save_screenshot('screenshot2.png') # save a screenshot to disk
        screen = driver.get_screenshot_as_png()

        box = (725,365, 862, 420)
        im = Image.open(BytesIO(screen))
        region = im.crop(box)
        region.save('screen3.png', 'PNG', optimize=True, quality=95)

        
        with open(r"screen3.png", 'rb') as captchaf:
            captcha = api.solve(captchaf)

        print(captcha.await_result())

                
        user_input.send_keys(captcha.await_result())
        driver.save_screenshot('screenshot4.png')

    user_input= driver.find_element_by_id('companyID')
    user_input.send_keys(CIN)

#hitting submit button
    login_button = driver.find_element_by_id("fetchprosecutionDetails_0")
    login_button.click()

 #using bs4 for scarping the table from next page
    soup_level1=BeautifulSoup(driver.page_source, 'lxml')
    driver.save_screenshot('screenshot4.png')
    msg = soup_level1.find(id="infoMsgs")
    info=[]
    info.append(msg.text)
    print(info)
    

    return "Report fetched"

@app.route('/mca/masterdata/din=<DIN>')
def masterdata(DIN):
    din=DIN
    service_args=[]
    try:
        driver = init_phantomjs_driver(service_args=service_args)
        driver.set_window_size(1024, 768) # optional
        driver.get('http://www.mca.gov.in/mcafoportal/viewDirectorMasterData.do') 
        driver.save_screenshot('screen.png') # save a screenshot to disk

        user_input= driver.find_element_by_id('din')
        user_input.send_keys(DIN_no)
        x=1
    
    except:
        x=0
        return "Site Failed"
    #hitting submit button
    if x==1:
        login_button = driver.find_element_by_id("showdirectorMasterData_0")
        login_button.click()

    #using bs4 for scarping the table from next page
        soup_level1=BeautifulSoup(driver.page_source, 'lxml')

        table1 = soup_level1.find_all('table')[1]
        table2 = soup_level1.find_all('table')[2]
        tab_list=[table1,table2]
        datalist=[]

        for i in range(0,2):
            df = pd.read_html(str(tab_list[i]),header=0)
            datalist.append(df[0])
            i=i+1

        result = pd.concat([pd.DataFrame(datalist[i]) for i in range(len(datalist))],ignore_index=True)   
        df[0].to_json('temp.json', orient='records', lines=True)
        return "FILES STORED"
    






if __name__ == '__main__':
    app.run(debug=True)