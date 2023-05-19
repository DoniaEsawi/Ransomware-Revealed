from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
import time
import pymongo
from pymongo import MongoClient
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from Bing.example import get_revenue_sector, get_region, get_year_of_foundation

client = MongoClient("mongodb://raghad:ra123@ac-nmbm3el-shard-00-00.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-01.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-02.gqycpcd.mongodb.net:27017/?ssl=true&replicaSet=atlas-zstffa-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.DataScience
collection = db.lockbit

binary = '/home/cti/datascience-internship/tor-browser/tor-browser/Browser/firefox'
# the location of firefox package inside Tor
if not os.path.exists(binary):
    raise ValueError("The binary path to Tor firefox does not exist.")

service = Service(executable_path=binary)
options = Options()
options.add_argument('-headless')
browser = webdriver.Firefox(service=service, options=options)

# click on connect to connect the tor browser to the remote nodes
browser.find_element("xpath", '//*[@id="connectButton"]').click()
time.sleep(3)

# check my IP address
url='http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion'
browser.get(url)
#time.sleep(15)
# get attribute onclick value
items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "post-block")) #browser.find_elements("class name", "post-block")
liks_list=[]
for item in items:
    attribute_val=item.get_attribute("onclick")
    link=attribute_val[attribute_val.find("/post"):-4]
    liks_list.append(url+link)

print(len(liks_list))   
# get the urrent time
now = datetime.now()

for link in liks_list:
    # to make sure the page is loaded
    #time.sleep(10)
    try:
        browser.get(link)
        deadline=items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "post-banner-p")) #browser.find_elements("class name", "post-block")
        #browser.find_elements("class name", "post-banner-p")[0].text
        deadline=deadline[0].text
        # remove Deadline: from deadline
        deadline=deadline.replace("Deadline: ","")
        company_name=browser.find_elements("class name", "post-big-title")[0].text
        connect=browser.find_elements("class name", "desc")[0].text
        ispublished=browser.find_elements("class name", "danger")[0].text
        ispublished= ispublished=="All available data published !"
        # remove any <br> and \n in connect
        connect=connect.replace("<br>","")
        print(deadline,company_name,connect)
        print("##########",ispublished)
        # check if the link in the coluction if yes then updated the published status and the last seen time
        if collection.find_one({"link":link}):
            collection.update_one({"link":link},{"$set":{"ispublished":ispublished,"last_seen":now}})
            continue
        # insert into mongodb
        revenue=get_revenue_sector("(industrial goods and services, technology, construction and materials, travel and leisure, healthcare) from these sectors could you tell me which sector is most related to" + link + "company? and what is its avarge revenue?")
        region = get_region("in what country is " + link + " comapny located ? reply in one word")
        year_of_foundation = get_year_of_foundation("when was " + link + "comapny founded?")
        collection.insert_one({"deadline":deadline,"company_name":company_name,"connect":connect,"link":link,"last_seen":now,"source":"lockbit","ispublished":ispublished,"revenue":revenue,"region":region,"year_of_foundation":year_of_foundation})

    except:
        continue
