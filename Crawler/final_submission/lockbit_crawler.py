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
collection = db.lockbit2

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
url='http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion'
browser.get(url) 
#time.sleep(15)
# get attribute onclick value
items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "post-block")) #browser.find_elements("class name", "post-block")
liks_list=[]
links_views_dict={}

for item in items:
    views = item.text.split("\n")[-1]
    
    attribute_val=item.get_attribute("onclick")
    link=attribute_val[attribute_val.find("/post"):-4]
    liks_list.append(url+link)
    links_views_dict[url+link]=views


print(len(liks_list))   
i =0
# get the urrent time
now = datetime.now()
openai.api_key = "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"

for link in liks_list:
    # to make sure the page is loaded
    #time.sleep(10)
    try:
        print ("current loop is: ", i)
        print("link is: ", link)

        browser.get(link)

        deadline=items = WebDriverWait(browser, timeout=30).until(lambda d: d.find_elements("class name", "post-banner-p")) #browser.find_elements("class name", "post-block")
        #browser.find_elements("class name", "post-banner-p")[0].text
        deadline=deadline[0].text
        # remove Deadline: from deadline
        deadline=deadline.replace("Deadline: ","")
        company_name=browser.find_elements("class name", "post-big-title")[0].text
        connect=browser.find_elements("class name", "desc")[0].text
        ispublished=browser.find_elements("class name", "danger")[0].text
        # print("is published is: ", ispublished)
        
        ispublished=ispublished.replace("\n", "")
        ispublished=ispublished.replace("\t", "")
        ispublished=ispublished.replace("\r", "")
        ispublished=ispublished.replace(" ", "")

        ispublished= ispublished=="ALLAVAILABLEDATAPUBLISHED!"
        # remove any <br> and \n in connect
        connect=connect.replace("<br>","")
        # print(deadline,company_name,connect)
        # print("##########",ispublished)

        
        # get orb answers
        company_data= get_company_info(company_name)
        if(company_data==None):
            # just update/insert the link and the last_seen and ispublished
            if collection.find_one({"link":link}): # if the link is already in the collection then update the last_seen and ispublished and views
                collection.update_one({"link":link},{"$set": {"ispublished":ispublished,"last_seen":now, "views": links_views_dict[link],"deadline":deadline,
                "company_name":company_name,"content":connect,"source":"lockbit",}})
                print("#######found in the collection and not existing in ORB######")
                i+=1
                continue
            print("#######not found in the collection and not existing in ORB######")
            collection.insert_one({"link":link,
                            "last_seen":now,
                            "ispublished":ispublished, 
                            "views": links_views_dict[link], 
                            "deadline":deadline,
                            "company_name":company_name,
                            "content":connect,
                            "source":"lockbit",
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
            {"deadline":deadline,
        "company_name":company_name,
        "content":connect,
        "link":link,
        "last_seen":now,
        "source":"lockbit",
        "ispublished":ispublished,
        "views": links_views_dict[link],
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
        collection.insert_one({"deadline":deadline,
        "company_name":company_name,
        "content":connect,
        "link":link,
        "last_seen":now,
        "source":"lockbit",
        "ispublished":ispublished,
        "views": links_views_dict[link],
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



        #############CHATGPT#########################
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #             {"role": "system", "content": "You are a chatbot"},
        #             {"role": "user", "content": "(industrial goods and services, technology, construction and materials, travel and leisure, healthcare) from these sectors could you tell me which sector is most related to" + company_name + " company? and what is its avarge revenue in dollar? put ** around the answer specific word"},
        #             {"role": "user", "content": "in what country is " + company_name + " comapny located ? provide the answer with <> around the country name"},
        #             {"role": "user", "content": "when was " + company_name + " comapny founded? reply in 1 word with ** around it"},
        #         ]
        # )

        # result = ''
        # for choice in response.choices:
        #     print("result:", choice.message.content)
        #     result += choice.message.content
        # print("Chat Answer is :", result)
        ######################################

        # check if the link in the coluction if yes then updated the published status and the last seen time

        # if collection.find_one({"link":link}):
        #     collection.update_one({"link":link},{"$set":{"ispublished":ispublished,"last_seen":now}})
        #     print("#######found in the collection######")
        #     continue
        
        
        # insert into mongodb
        # revenue, sector, year, location=get_revenue_sector("(industrial goods and services, technology, construction and materials, travel and leisure, healthcare) from these sectors could you tell me which sector is most related to" + company_name + " company? and what is its avarge revenue (in dollar)?", result )
        # print("revenue, sector, year, location is: ", revenue, sector, year, location)
        # region = get_region("in what country is " + company_name + " comapny located ? reply in one word")
        # print("region is: ", region)
        # year_of_foundation = get_year_of_foundation("when was " + company_name + " comapny founded?")
        # print("year_of_foundation is: ", year_of_foundation)


        # print the whole page
        # print(browser.page_source)
        # store the html in a file
        # with open("lockbit.html", "w") as file:
        #     file.write(browser.page_source)
        #     file.close()

        # with open("new_link.html", "w") as file:
        #     file.write(browser.page_source)
        #     file.close()
        # i+=1
        # if (i> 20):
        #     break
        # continue
browser.close()
