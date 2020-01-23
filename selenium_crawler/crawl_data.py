#download chrome driver from here https://chromedriver.chromium.org/downloads
#remember to do "chmod 777 chromedriver" if running for the first time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

import argparse
import json

import time
import os
from PIL import Image

from multiprocessing import cpu_count
import multiprocessing
import imthread

from sys import platform; p = platform.lower()
if p == "linux" or p == "linux2": chromedriver = "chromedriver/linux64/chromedriver"
elif p == "win32": chromedriver = "chromedriver/win32/chromedriver"
elif p == "darwin": chromedriver = "chromedriver/mac64/chromedriver"

#for loading pages faster
caps = DesiredCapabilities().CHROME 
caps["pageLoadStrategy"] = "eager" #"normal", "eager", "none"

visible = False

if visible:
    #for running chrome with gui
    driver = webdriver.Chrome(chromedriver)
else:
    #for running chrome headlessly
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--window-size=500x1024")
    driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options, executable_path=chromedriver)


def crawl_data(url):
    print(url[0])
    url, image = url[0], url[1]

    driver.get(url)
    if not str(driver.title).startswith("Climate"): return
    # print("page loaded successfully!")

    driver.execute_script("window.scrollTo(0, 1005);")
    driver.save_screenshot(image)

    img = Image.open(image) 
    coords = (5, 50, 158, 887) #left, top, right, bottom
    img = img.crop(coords) 
    img.save(image)


if __name__ == "__main__":
    #input arguments
    #ws_number = "421810" #weather station: delhi
    output_dir_root = "downloads"

    ws_stations = {
    'delhi': '421810',
    'indore': '427540',
    'mumbai': '429210',
    'gujarat': '426470',
    'odissa': '428950',
    'assam': '424100',
    'coimbatore': '433210'
    }

    for city, ws_number in ws_stations.items():
        output_dir = os.path.join(output_dir_root, city+"-ws-"+ws_number)
        if not os.path.exists(output_dir): os.makedirs(output_dir)

        URLS = [] #preparing urls to visit
        for year in range(11, 16): #year 2011 to 2015
            year = "200"+str(year) if len(str(year)) == 1 else "20"+str(year)
            for month in range(1, 13):
                month = "0"+str(month) if len(str(month))== 1 else str(month)
                url = "https://en.tutiempo.net/climate/{}-{}/ws-{}.html".format(month, year, ws_number)
                name = url.split("/climate/")[1].split(".htm")[0].replace("/","-")+".png"
                name = os.path.join(output_dir, name)
                URLS.append((url,name))


        for i, url in enumerate(URLS):
            try:
                crawl_data(url)
            except Exception as e:
                print(e)

         #if i==1:break

    #close browser after task finished
    driver.stop_client()
    driver.close()
    print("finished!")