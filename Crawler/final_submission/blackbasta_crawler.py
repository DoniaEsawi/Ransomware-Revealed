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
collection = db.BlackBasta

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


url='http://stniiomyjliimcgkvdszvgen3eaaoz55hreqqx6o77yvmpwt7gklffqd.onion/'
browser.get(url) 
#time.sleep(15)
# get attribute onclick value
items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "card")) #browser.find_elements("class name", "post-block")
links_list=[]
links_views_dict={}
links=0
urls_found = 0
all_companies_dict = {}
for item in items:
    # views = item.text.split("\n")[-1]
    title = item.find_element("class name", "blog_name_link").text
    all_companies_dict[title] = {}
    all_companies_dict[title]["last_seen"] = datetime.now()
    print("item title is: ", title)
    info=item.find_element("class name", "vuepress-markdown-body")
    info = info.find_elements("tag name", "p")
    urls= []
    for inf in info:
        text = inf.text
        
        res = re.findall('website.+\..+(?:\n|$)', text.lower())
        if(res!=None and len(res)>0):
            urls.extend(res)
        res = re.findall('site.+\..+(?:\n|$)', text.lower())
        if(res!=None and len(res)>0):
            urls.extend(res)
        for url in urls:
            url = url.replace("\n","")
            url = url.replace("website:","")
            url = url.replace("site:","")
            url = url.replace("website","")
            url = url.replace("site","")
            url = url.replace("*","")
            all_companies_dict[title]["link"]=url.split(" ")[-1]
            links_list.append(all_companies_dict[title]["link"])
            break
    if len(urls)>0:
        urls_found +=1
    views_puplished = item.find_elements("class name", "counter_container")
    if(len(views_puplished)>0):
        for container in views_puplished:
            all_companies_dict[title][container.find_element("class name", "counter_title").text] = container.find_element("class name", "counter_value").text
            

    links+=1
next_page = browser.find_elements("class name", "next-page-btn")
while(len(next_page)>0):
    next_page[0].click()
    time.sleep(3)
    items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "card")) #browser.find_elements("class name", "post-block")
    for item in items:
        # views = item.text.split("\n")[-1]
        title = item.find_element("class name", "blog_name_link").text
        all_companies_dict[title] = {}
        all_companies_dict[title]["link"] = None
        all_companies_dict[title]["last_seen"] = datetime.now()
        print("item title is: ", title)
        info=item.find_element("class name", "vuepress-markdown-body")
        info = info.find_elements("tag name", "p")
        urls= []
        for inf in info:
            text = inf.text
            
            res = re.findall('website.+\..+(?:\n|$)', text.lower())
            if(res!=None and len(res)>0):
                urls.extend(res)
            res = re.findall('site.+\..+(?:\n|$)', text.lower())
            if(res!=None and len(res)>0):
                urls.extend(res)
            for url in urls:
                url = url.replace("\n","")
                url = url.replace("website:","")
                url = url.replace("site:","")
                url = url.replace("website","")
                url = url.replace("site","")
                url = url.replace("*","")

                all_companies_dict[title]["link"]=url.split(" ")[-1]
                links_list.append(all_companies_dict[title]["link"])
                break
        if len(urls)>0:
            urls_found +=1
        views_puplished = item.find_elements("class name", "counter_container")
        if(len(views_puplished)>0):
            for container in views_puplished:
                all_companies_dict[title][container.find_element("class name", "counter_title").text] = container.find_element("class name", "counter_value").text
                

        links+=1
    next_page = browser.find_elements("class name", "next-page-btn")


print("links count is: ", links)
print("urls found is: ", urls_found)
no_link = 0
for title in all_companies_dict:
    print("title is: ", title)
    # check if there's a link
    if(all_companies_dict[title]["link"]==None):
        print("has no link")
        no_link+=1
        continue
    print("link is:", all_companies_dict[title]["link"])


############################# API `ORB` #############################


i = 0
for title in all_companies_dict:
    # to make sure the page is loaded
    #time.sleep(10)
    # check if there's a link
    print ("current loop is: ", i)
    time.sleep(1)
    if(all_companies_dict[title]["link"]==None):
        i+=1
        continue
    try:
        link = all_companies_dict[title]["link"]
        print("link is: ", link)

        # get orb answers
        company_data= get_company_info(link)
        if(company_data==None):
            # just update/insert the link and the last_seen and ispublished
            if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished and views
                collection.update_one({"link":link},{"$set": 
                {"ispublished":all_companies_dict[title]["Published"],
                "last_seen": all_companies_dict[title]["last_seen"],
                "views": all_companies_dict[title]["Visits"],
                "deadline":None,
                "company_name":title,
                
                "source":"black basta",}})
                print("#######found in the collection and not existing in ORB######")
                i+=1
                continue
            print("#######not found in the collection and not existing in ORB######")
            collection.insert_one({"link":link,
                            "last_seen":all_companies_dict[title]["last_seen"],
                            "ispublished":all_companies_dict[title]["Published"], 
                            "views":all_companies_dict[title]["Visits"], 
                            "deadline":None,
                            "company_name":title,
                            "content":None,
                            "source":"black basta",
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
        "source":"black basta",
        "ispublished":all_companies_dict[title]["Published"],
        "views": all_companies_dict[title]["Visits"],
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
        "source":"black basta",
        "ispublished":all_companies_dict[title]["Published"],
        "views": all_companies_dict[title]["Visits"],
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