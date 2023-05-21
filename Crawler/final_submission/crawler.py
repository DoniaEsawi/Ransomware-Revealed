import time
import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import socks
import os

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9051'
}

# Set the number of links to crawl
num_links_to_crawl = 5#0

# Set the user agent to use for the request

user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'

# Set the headers for the request
headers = {'User-Agent': user_agent}

# Initialize the controller for the Tor network
with Controller.from_port(port=9051) as controller:
    # Set the controller password
    controller.authenticate(password="Nada")
    # Set the starting URL
    url = "https://www.example.com/"   ## lockBit http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion
    # url = "http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion/"    ## Ransomware Group Sites
 
    # Initialize the visited set and the link queue
    visited = set()
    queue = [url]

    # Get the list of keywords to search for
    # keywords = input('Enter a list of keywords to search for, separated by commas: ').split(',')

    # Set the new IP address
    controller.signal(Signal.NEWNYM)
    # Crawl the links
    while queue:
        # Get the next link in the queue
        link = queue.pop(0)

        # Skip the link if it has already been visited
        if link in visited:
            continue


        # Send the request to the URL
        try:
            print(link)
            response = requests.get(link,proxies=proxies)
            print(response)
        except:
            continue


        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a')

        # Add any links that contain the keywords to the queue
        for a in links:
            href = a.get('href')
            # if any(keyword in href for keyword in keywords):
            queue.append(href)

        # Add the link to the visited set
        visited.add(link)

        # Print the title and URL of the page
        print(soup.title.string, link)

        # Check if the number of visited links has reached the limit
        if len(visited) >= num_links_to_crawl:
            break

# Print the visited links
print('Visited links:')
for link in visited:
    print(link)
