import sys
from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser
from bs4 import BeautifulSoup

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept-Encoding': 'identity'
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    print("Status code %s"%r.status_code)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    # print("r.text %s"%r.json())
    soup=BeautifulSoup(r.text)
    print("soup %s"%r.text)
    a_file = open("sample.txt", "w")
    print(soup.encode("utf-8"), file=a_file)
    a_file.close()
    
    return e.extract(r.text)

# product_data = []
with open("urls.txt",'r') as urllist, open('data.csv','w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["title","content","date","variant","images","verified","author","rating","product","url"],quoting=csv.QUOTE_ALL)
    writer.writeheader()
    print("urllist")
    for url in urllist.readlines():
        print("url")
        print(url)
        data = scrape(url) 
        print("data")
        # a_fiile = open("sample2.txt", "w")
        json.dump(data, sys.stdout)
        print(data)

        # print(data, file=a_fiile)
        # a_fiile.close()        
        if data is not None:
            for r in data['reviews']:
                r["product"] = data["product_title"]
                r['url'] = url
                if 'verified' in r:
                    if 'Verified Purchase' in r['verified']:
                        r['verified'] = 'Yes'
                    else:
                        r['verified'] = 'Yes'
                r['rating'] = r['rating'].split(' out of')[0]
                date_posted = r['date'].split('on ')[-1]
                if r['images']:
                    r['images'] = "\n".join(r['images'])
                r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
                # a_file = open("sample.txt", "w")
                # print(r.encode("utf-8"), file=a_file)
                # a_file.close()
                print("the r is")
                print(r)
                # writer.writerow(r)
            # sleep(5)
    