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
collection = db.PlayNews

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


url='http://k7kg3jqxang3wh7hnmaiokchk7qoebupfgoik6rha6mjpzwupwtj25yd.onion/index.php?page='
browser.get(url+'1') 
#time.sleep(15)
# get attribute onclick value
table = WebDriverWait(browser, timeout=30).until(lambda d: d.find_element("tag name", "tbody")) #browser.find_elements("class name", "post-block")

table_rows= table.find_elements("tag name", "tr")
pages = table_rows[-1].find_elements("tag name", "span")
max_page = pages[-1].text.replace(" ","")
print("max page is: ", max_page)
current_page = int(max_page) + 1
while (int(current_page) > int(max_page)):
  max_page = str(current_page)
  browser.get(url+str(max_page))
  table_rows=WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("tag name", "tr")) #browser.find_elements("class name", "post-block")
  pages = table_rows[-1].find_elements("tag name", "span")
  current_page = pages[-1].text.replace(" ","")
  print("current page is: ", current_page)
max_page= str(current_page)

i = 0
loops = int(max_page)
print("number of pages is: ", int(max_page))
all_companies_dict = {}
for j in range(loops):
  browser.get(url+str(j+1))
  table_rows=WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("tag name", "tr")) #browser.find_elements("class name", "post-block")
  pages = table_rows[-1].find_elements("tag name", "span")
  # wait for the page to load
  cards=WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "News")) #browser.find_elements("class name", "post-block")
  for card in cards:
    print(card.text.split("\n"))
    list_of_info = card.text.split("\n")
    title =list_of_info[0].replace(" ","")
    print("title is: ", title)
    all_companies_dict[title] = {}
    country = list_of_info[1].split(",")[-1]
    country = country.strip()
    print("country is: ", country)
    all_companies_dict[title]["country"] = country
    all_companies_dict[title]["link"] = list_of_info[2].replace(" ","")
    print("link is: ", all_companies_dict[title]["link"])
    all_companies_dict[title]["last_seen"] = datetime.now()
    views = list_of_info[3].split(" ")[-1]
    print("views is: ", views)
    all_companies_dict[title]["views"] = views
    date_added = list_of_info[4].split(" ")[-1]
    # convert date to datetime object
    date_added = datetime.strptime(date_added, '%Y-%m-%d')
    print("date_added is: ", date_added)
    all_companies_dict[title]["date_added"] = date_added
    publication_date = list_of_info[5].split(" ")[-1]
    # convert date to datetime object
    publication_date = datetime.strptime(publication_date, '%Y-%m-%d')
    print("publication_date is: ", publication_date)
    all_companies_dict[title]["publication_date"] = publication_date
    if (list_of_info[6] == "PUBLISHED" or list_of_info[6] == "PUBLISHED FULL"):
      all_companies_dict[title]["ispublished"] = True
    else:
      all_companies_dict[title]["ispublished"] = False
    print("ispublished is: ", all_companies_dict[title]["ispublished"])

    print("===========================================")
  print("=====================Page",j+1,"======================")

############################ API `ORB` #############################


i = 0
not_found = 0
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
            not_found+=1
            # just update/insert the link and the last_seen and ispublished
            if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished and views
                collection.update_one({"link":link},{"$set": 
                {
                "ispublished":all_companies_dict[title]["ispublished"],
                "last_seen": all_companies_dict[title]["last_seen"],
                "views": all_companies_dict[title]["views"],
                "deadline":all_companies_dict[title]["publication_date"],
                "company_name":title,
                "date_added":all_companies_dict[title]["date_added"],
                "source":"Play News",
                }})
                print("#######found in the collection and not existing in ORB######")
                i+=1
                continue
            print("#######not found in the collection and not existing in ORB######")
            collection.insert_one({"link":link,
                            "last_seen":all_companies_dict[title]["last_seen"],
                            "ispublished":all_companies_dict[title]["ispublished"],
                            "views": all_companies_dict[title]["views"], 
                            "deadline":all_companies_dict[title]["publication_date"],
                            "company_name":title,
                            "date_added":all_companies_dict[title]["date_added"],
                            "content":None,
                            "source":"Play News",
                            "branches_count":None,
                            "display_name":None,
                            "country":all_companies_dict[title]["country"],
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
            {"deadline":all_companies_dict[title]["publication_date"],
        "company_name":title,
        "content":description,
        "link":link,
        "last_seen":all_companies_dict[title]["last_seen"],
        "source":"Play News",
        "ispublished":all_companies_dict[title]["ispublished"],
        "views": all_companies_dict[title]["views"],
        "date_added":all_companies_dict[title]["date_added"],
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
        collection.insert_one({"deadline":all_companies_dict[title]["publication_date"],
        "company_name":title,
        "content":description,
        "link":link,
        "last_seen":all_companies_dict[title]["last_seen"],
        "source":"Play News",
        "ispublished": all_companies_dict[title]["ispublished"],
        "views": all_companies_dict[title]["views"],
        "date_added":all_companies_dict[title]["date_added"],
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


print("number of not found companies is: ", not_found)
browser.close()