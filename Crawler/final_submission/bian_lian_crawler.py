#!/usr/bin/env python3
from datetime import datetime

start_time = datetime.now()
print(f"Start time: {datetime.now().strftime('%H:%M:%S')}")

# import from selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from selenium import webdriver
import os
import time
import pymongo
from pymongo import MongoClient
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from Bing.example import get_revenue_sector, get_company_info
import openai

client = MongoClient("mongodb://raghad:ra123@ac-nmbm3el-shard-00-00.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-01.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-02.gqycpcd.mongodb.net:27017/?ssl=true&replicaSet=atlas-zstffa-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.DataScience
collection = db.BianLian

binary = '/home/cti/datascience-internship/tor-browser/tor-browser/Browser/firefox'
# the location of firefox package inside Tor
if os.path.exists(binary) is False:
    raise ValueError("The binary path to Tor firefox does not exist.")
firefox_binary = FirefoxBinary(binary)


def get_browser(binary=None,options=None):
    global browser  
    # capapilities = webdriver.DesiredCapabilities.FIREFOX
    # # disable Tor proxy
    # capapilities['proxy']={
    #     "proxyType": "none",
    # }
    profile = FirefoxProfile('/home/cti/datascience-internship/tor-browser/tor-browser/Browser/TorBrowser/Data/Browser/profile.default')
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    profile.set_preference("network.proxy.socks_remote_dns", True)
    profile.update_preferences()
    # only one instance of a browser opens, remove global for multiple instances
    if not browser: 
        browser = webdriver.Firefox(firefox_binary=binary,options=options, firefox_profile=profile,
                                    executable_path="/usr/local/bin/geckodriver")
    return browser


browser = None
options = Options()
options.add_argument('-headless')
browser = get_browser(binary=firefox_binary, options=options)

# click on connect to connect the tor browser to the remote nodes
browser.find_element("xpath", '//*[@id="connectButton"]').click()
time.sleep(3)

# check my IP address
url='http://bianlianlbc5an4kgnay3opdemgcryg2kpfcbgczopmm3dnbz3uaunad.onion/'
browser.get(url) 
#time.sleep(15)
# get attribute onclick value
items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "readmore")) #browser.find_elements("class name", "post-block")
liks_list=[]
links_views_dict={}
current_page = 1
for item in items:
    liks_list.append(item.get_attribute("href"))
    print(item.get_attribute("href"))
while True:
    
    paginations = browser.find_elements("class name", "page-link") #browser.find_elements("class name", "post-block")
    if((current_page==1 and len(paginations)==1) or (current_page>1 and len(paginations)>1)):
        current_page+=1
        print("current page is:", current_page)
        browser.get(paginations[-1].get_attribute("href"))
        items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "readmore")) #browser.find_elements("class name", "post-block")
        for item in items:
            liks_list.append(item.get_attribute("href"))
            print(item.get_attribute("href"))

    else:
        break

print(len(liks_list))   
all_companies_dict = {}
for link in liks_list:
    browser.get(link)
    title = WebDriverWait(browser, timeout=30).until(lambda d: d.find_element("class name", "title")) #browser.find_elements("class name", "post-block")
    print("title is: ",title.text)
    company_name=title.text.replace(" ","")
    
    body = browser.find_element("class name", "body") #browser.find_elements("class name", "post-block")
    links =body.find_elements("tag name", "a") #browser.find_elements("class name", "post-block")
    print("links count is: ",len(links))
    if (len(links)>0):
        all_companies_dict[company_name] = {
        }
        print("link is: ", links[0].get_attribute("href"))
        all_companies_dict[company_name]["link"] = links[0].get_attribute("href")

i =0 
for title in all_companies_dict:
    # check if there's a link
    print ("current loop is: ", i)
    time.sleep(1)
    if(all_companies_dict[title]["link"]==None):
        i+=1
        continue
    try:
        link = all_companies_dict[title]["link"]
        print("link is: ", link)
        all_companies_dict[title]["last_seen"] = datetime.now()
        # get orb answers
        company_data= get_company_info(link)
        if(company_data==None):
            # just update/insert the link and the last_seen and ispublished
            if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished and views
                collection.update_one({"link":link},{"$set": 
                {"ispublished":True,
                "last_seen": all_companies_dict[title]["last_seen"],
                "views": None,
                "deadline":None,
                "company_name":title,
                
                "source":"BianLian",}})
                print("#######found in the collection and not existing in ORB######")
                i+=1
                continue
            print("#######not found in the collection and not existing in ORB######")
            collection.insert_one({"link":link,
                            "last_seen":all_companies_dict[title]["last_seen"],
                            "ispublished":True, 
                            "views":None, 
                            "deadline":None,
                            "company_name":title,
                            "content":None,
                            "source":"BianLian",
                            "branches_count":None,
                            "display_name":None,
                            "country":None,
                            "industry":None,
                            "revenue_range":None,
                            "employees_range":None,
                            "year_founded":None,
                            "description":None,
                            "longitude":None,
                            "latitude":None,
                            "company_status":None,
                            "revenue":None,
                            "employees_count":None,
                            "technologies_used":[],})
            i+=1
            continue

        branches_count=company_data["branches_count"]
        name= company_data["name"]
        country= company_data["address"]["country"]
        industry= company_data["industry"]
        revenue_range= company_data["revenue_range"]
        employees_range=company_data["employees_range"]
        year_founded= company_data["year_founded"]
        description= company_data["description"]
        longitude= company_data["longitude"]
        latitude= company_data["latitude"]
        company_status= company_data["company_status"]
        revenue = company_data["revenue"]
        employees_count = company_data["employees"]
        techs= []
        if (company_data["technologies"]!=None and len(company_data["technologies"])>0):
            for tech in company_data["technologies"]:
                techs.append(tech["name"])
        technologies = techs
        # if the company is already in the collection then jsut update the last_seen and ispublished
        if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished
            collection.update_one({"link":link},{"$set":
            {"deadline":None,
        "company_name":title,
        "content":description,
        "link":link,
        "last_seen":all_companies_dict[title]["last_seen"],
        "source":"BianLian",
        "ispublished":True,
        "views": None,
        "branches_count":branches_count,
        "display_name":name,
        "country":country,
        "industry":industry,
        "revenue_range":revenue_range,
        "employees_range":employees_range,
        "year_founded":year_founded,
        "description":description,
        "longitude":longitude,
        "latitude":latitude,
        "company_status":company_status,
        "revenue":revenue,
        "employees_count":employees_count,
        "technologies_used":technologies,
        
        }
            })
            print("#######found in the collection and exist in ORB######")
            i+=1
            continue
        print("#######not found in the collection and exist in ORB######")
        collection.insert_one({"deadline":None,
        "company_name":title,
        "content":description,
        "link":link,
        "last_seen":all_companies_dict[title]["last_seen"],
        "source":"BianLian",
        "ispublished": True,
        "views": None,
        "branches_count":branches_count,
        "display_name":name,
        "country":country,
        "industry":industry,
        "revenue_range":revenue_range,
        "employees_range":employees_range,
        "year_founded":year_founded,
        "description":description,
        "longitude":longitude,
        "latitude":latitude,
        "company_status":company_status,
        "revenue":revenue,
        "employees_count":employees_count,
        "technologies_used":technologies,
        
        })
        i+=1
    except Exception as e:
        print("Exception is: ", e)
        i+=1
        continue    


browser.close()