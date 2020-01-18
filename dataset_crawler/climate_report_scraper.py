from bs4 import BeautifulSoup as BS
import time
import requests
import imthread
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

def scrape_climate_report(url):
    print('scraping: {}'.format(url))
    web = requests.get(url, headers=headers)
    soup = BS(web.content,"html.parser")
    soup = soup.findAll("tr")

    headings = {}
    days = {}
    for i, tr in enumerate(soup[3:]):
        if i == 32: break
        if not i ==0: days[i] = {}
        
        for j, td in enumerate(tr):
            if i==0: #extracting Headings
                if j==0: #Day column
                    key, val = str(td).split("<th>")[1].split("</th>")[0], str(td).split("<th>")[1].split("</th>")[0]
                    headings[key] = val
                    #print(i, j, key, val)

                else: #other columns
                    key, val = str(td).split("\">")[1].split("</abbr>")[0], str(td).split("title=\"")[1].split("\">")[0]
                    headings[key] = val
                    #print(i, j, key, val)

            else:
                try:
                    key, val = list(headings.keys())[j], str(td).split("<td>")[1].split("</td>")[0] #table rows for each day
                    if j==0: val = val.split("<strong>")[1].split("</strong>")[0] #removing boldness from day number
                    val = '-' if len(val.strip()) == 0 or val.strip().startswith("<span") else val #removing
                    days[i][key] = val
                    #print(i, j, key, val)
                except Exception as e:
                    pass

        #print(days)
        #if i >= 4: input(">>> enter to continue")
    return days


ws_number = "421810" #weather station number
#print('scraping: https://en.tutiempo.net/climate/<month>-<year>/ws-<ws_number>.html')

URLS = [] #preparing urls to visit
for year in range(9, 16): #year 2009 to 2015
    year = "200"+str(year) if len(str(year)) == 1 else "20"+str(year)
    for month in range(1, 13):
        month = "0"+str(month) if len(str(month))== 1 else str(month)
        url = "https://en.tutiempo.net/climate/{}-{}/ws-{}.html".format(month, year, ws_number)
        URLS.append(url)


data = {} #for storing all retrieved information

for i, url in enumerate(URLS):
    res = scrape_climate_report(url)
    data[url] = res


#results = imthread.start(scrape_climate_report, data=URLS, max_threads=100)

#collecting retrieved information from different threads
# for url, res in zip(URLS, results):
#     res = scrape_climate_report(url)
#     data[url] = res

#saving to a json file
with open("climate_report.json", "w") as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))

print(">> finished")