#!/usr/bin/env python3
from datetime import datetime

start_time = datetime.now()
print(f"Start time: {datetime.now().strftime('%H:%M:%S')}")

# import from selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
import time as timer
import pymongo
from pymongo import MongoClient
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from Bing.example import get_revenue_sector, get_company_info
import openai

client = MongoClient("mongodb://raghad:ra123@ac-nmbm3el-shard-00-00.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-01.gqycpcd.mongodb.net:27017,ac-nmbm3el-shard-00-02.gqycpcd.mongodb.net:27017/?ssl=true&replicaSet=atlas-zstffa-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.DataScience
collection = db.Royal

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
timer.sleep(3)

# check my IP address
url='http://royal4ezp7xrbakkus3oofjw6gszrohpodmdnfbe5e4w3og5sm7vb3qd.onion/'
browser.get(url) 
#time.sleep(15)
# get attribute onclick value
items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("tag name", "article")) #browser.find_elements("class name", "post-block")

cards = []
old_card_size = len(cards)
while True:
    # reach the end of the scroll bar
    browser.find_element("tag name", 'body').send_keys(Keys.END)
    
    # # wait 3 seconds for new elements to load
    timer.sleep(3)
    # retrieve all cards
    # # cards = browser.find_elements("xpath", "//*[@class='post' and @class='active']")
    cards = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "post")) #browser.find_elements("class name", "post-block")
    # # WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='post active']")))

    # # for card in cards:
    # #     info = card.find_element("class name", "card")
    # #     print(info.text)
    # # if no new cards were found
    if (old_card_size == len(cards)):
        # break the cycle since the scroll is over
       break

    # # keep track of the number of cards
    # # currently discovered
    old_card_size = len(cards)
    print(old_card_size)
# print(browser.page_source)
all_cards= browser.find_elements("xpath", "//*[@class='post active']")
all_cards.extend(browser.find_elements("xpath", "//*[@class='post']"))
print("all cards len: ",len(all_cards))
all_info = browser.find_elements("class name", "card")
print("all info len: ",len(all_info))
all_companies_dict = {}
for card in all_cards:
    # check if the card is active

    if card.get_attribute("class") == "post active":
        print("active")
    else:
        print("not active")
    time = card.find_element("class name", "time")
    progress = card.find_element("class name", "progress")
    time_list = time.find_elements("tag name", "span")
    progress_text = progress.find_element("tag name", "text")
    day = time_list[0].get_attribute("textContent")
    month= time_list[1].get_attribute("textContent")
    year = time_list[2].get_attribute("textContent")
    print("day is: ", day)
    print("month is: ", month)
    print("year is: ", year)
    date = datetime.strptime(day+" "+month+", "+year, '%d %B, %Y')
    svg_progress= progress.find_element("tag name", "svg")
    progress = svg_progress.get_attribute("data-percentage").replace(" ", "")+"%"
    print("progress: ", progress)
    card_info = card.find_element("class name", "card")
    card_title = card_info.find_element("tag name", "h2")
    info_list = card_info.find_elements("tag name", "li")
    card_title = card_title.get_attribute("textContent")
    print("title is: ", card_title)
    link = None
    revenue = None
    employees_count = None
    i = 0
    for info in info_list:
        texts= info.find_elements("tag name", "span")
        
        if len(texts)>0:
            
            for text in texts:
                if i == 1:
                    revenue = text.get_attribute("textContent")
                    print("revenue is: ", revenue)
                elif i == 2:
                    employees_count = text.get_attribute("textContent")
                    print("employees_count is: ", employees_count)
        i+=1
        links = info.find_elements("tag name", "a")
        if len(links)>0:
            for link in links:
                link = link.get_attribute("href")
                print("link is: ", link)
    
    all_companies_dict[card_title]={
        "date_added": date.strftime('%Y-%m-%d'),
        "progress": progress,
        "revenue": revenue,
        "employees_count": employees_count,
        "link": link
    }
    print(all_companies_dict[card_title])
    print("======= end of card ==========")


i = 0
not_exist_in_orb = 0
for title in all_companies_dict:
    # check if there's a link
    print ("current loop is: ", i)
    
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
                "progress":all_companies_dict[title]["progress"],
                "date_added":all_companies_dict[title]["date_added"],
                "source":"Royal",}})
                print("#######found in the collection and not existing in ORB######")
                i+=1
                not_exist_in_orb +=1
                continue
            print("#######not found in the collection and not existing in ORB######")
            collection.insert_one({"link":link,
                            "last_seen":all_companies_dict[title]["last_seen"],
                            "ispublished":True, 
                            "progress":all_companies_dict[title]["progress"],
                            "date_added":all_companies_dict[title]["date_added"],
                            "views":None, 
                            "deadline":None,
                            "company_name":title,
                            "content":None,
                            "source":"Royal",
                            "branches_count":None,
                            "display_name":None,
                            "country":None,
                            "industry":None,
                            "revenue_range":all_companies_dict[title]["revenue"],
                            "employees_range":all_companies_dict[title]["employees_count"],
                            "year_founded":None,
                            "description":None,
                            "longitude":None,
                            "latitude":None,
                            "company_status":None,
                            "revenue":all_companies_dict[title]["revenue"],
                            "employees_count":all_companies_dict[title]["employees_count"],
                            "technologies_used":[],})
            not_exist_in_orb +=1
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
        if revenue_range == None:
            revenue_range = all_companies_dict[title]["revenue"]
        if employees_range == None:
            employees_range = all_companies_dict[title]["employees_count"]
        if revenue == None:
            revenue = all_companies_dict[title]["revenue"]
        if employees_count == None:
            employees_count = all_companies_dict[title]["employees_count"]
        # if the company is already in the collection then jsut update the last_seen and ispublished
        if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished
            collection.update_one({"link":link},{"$set":
            {"deadline":None,
        "company_name":title,
        "content":description,
        "progress":all_companies_dict[title]["progress"],
        "date_added":all_companies_dict[title]["date_added"],
        "link":link,
        "last_seen":all_companies_dict[title]["last_seen"],
        "source":"Royal",
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
        "source":"Royal",
        "ispublished": True,
        "views": None,
        "progress":all_companies_dict[title]["progress"],
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


print("not_exist_in_orb: ", not_exist_in_orb)
browser.close()