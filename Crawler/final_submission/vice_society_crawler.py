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
import re
client = MongoClient("mongodb://raghad:ra123@ac-nmbm3el-shard-00-00.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-01.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-02.gqycpcd.mongodb.net:27017/?ssl=true&replicaSet=atlas-zstffa-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.DataScience
collection = db.ViceSociety

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


url='http://ml3mjpuhnmse4kjij7ggupenw34755y4uj7t742qf7jg5impt5ulhkid.onion/partners.html'
browser.get(url) 
#time.sleep(15)
# get attribute onclick value
items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("tag name", "table")) #browser.find_elements("class name", "post-block")
table = items[2]
table_rows= table.find_elements("tag name", "tr")


all_companies = table_rows[3:]
no_data = 0
all_companies_new = all_companies
print("all companies length is: ", len(all_companies_new))
companies = 0
companies_dict = {}
for company in all_companies_new:
    try:
        td_count = company.find_elements("tag name", "td")
        if (len(td_count)< 2):
            continue
        td_count2 = td_count[0].find_elements("tag name", "td")
        if (len(td_count2)> 0):
            continue
        company_data = company.find_elements("tag name", "font")
        if(len(company_data)>0):
            companies+=1
            i =0 
            title = company_data[0].text
            for data in company_data:
                print("data ",i, data.text)
                if (i==0):
                    companies_dict[title] = {}
                elif (i==1):
                    companies_dict[title]["link"] = data.text
                    print("link is: ", companies_dict[title]["link"])
                else:
                    break
                i+=1
        else:
            print("no data")
            no_data+=1
    except Exception as e:
        print("Exception is: ", e)
print("no data is: ", no_data)
print("companies is: ", companies)

for i , title in enumerate(companies_dict):
    print("company no: ", i)
    print("title is: ", title)
    print("link is: ", companies_dict[title]["link"])
    print("##############################################")

############################# API `ORB` #############################


i = 0
for title in companies_dict:
    # check if there's a link
    print ("current loop is: ", i)
    time.sleep(1)
    if(companies_dict[title]["link"]==None):
        i+=1
        continue
    try:
        link = companies_dict[title]["link"]
        print("link is: ", link)
        companies_dict[title]["last_seen"] = datetime.now()
        # get orb answers
        company_data= get_company_info(link)
        if(company_data==None):
            # just update/insert the link and the last_seen and ispublished
            if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished and views
                collection.update_one({"link":link},{"$set": 
                {"ispublished":True,
                "last_seen": companies_dict[title]["last_seen"],
                "views": None,
                "deadline":None,
                "company_name":title,
                
                "source":"Vice Society",}})
                print("#######found in the collection and not existing in ORB######")
                i+=1
                continue
            print("#######not found in the collection and not existing in ORB######")
            collection.insert_one({"link":link,
                            "last_seen":companies_dict[title]["last_seen"],
                            "ispublished":True, 
                            "views":None, 
                            "deadline":None,
                            "company_name":title,
                            "content":None,
                            "source":"Vice Society",
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
        "last_seen":companies_dict[title]["last_seen"],
        "source":"Vice Society",
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
        "last_seen":companies_dict[title]["last_seen"],
        "source":"Vice Society",
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