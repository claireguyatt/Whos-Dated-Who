import argparse
import json
import os
import random
import hashlib
import requests
from bs4 import BeautifulSoup
import time

# inputs: first names json file, route to cache file

def add_all_names(category_names: list[str]) -> list[str]:

    new_names = []

    # get names from all original names' relations
    for name in category_names:

        # turn name into url
        url = "https://www.whosdatedwho.com/dating/" + name

        # get relations from name
        newer_names = add_names_from_existing(url)
        if newer_names != None:
            new_names = new_names + newer_names

    # if there aren't enough names in the category, continue by randomly picking names until there are
    # want 250 per category, get 300 incase of dups
    while (len(new_names) < 300):

        print(len(new_names))

        url = "https://www.whosdatedwho.com/dating/" + random.choice(new_names)
        newer_names = add_names_from_existing(url)
        if newer_names != None:
            new_names = new_names + newer_names

    return new_names
    
# add new names from input name relations
def add_names_from_existing(url: str) -> list[str]:

    # cache the page of the input url (if not already)
    path = cache_page("data/wdw_cache", url)

    if path == None:
        return None

    # open file with beautifulsoup to start scraping
    soup = BeautifulSoup(open(path, 'r'), 'html.parser')

    # list to add relations to
    relations = list()

    # find div that contains paragraphs that list relations
    block = soup.find('div', class_='ff-block-content dating-profile')

    # get all types of relationships
    types = ['was previously married to', 'has been in relationships with', 'has had encounters with', 
                'is rumoured to have hooked up with', 'has been engaged to']

    # find paragraphs within div
    paragraphs = block.find_all('p')
    for p in paragraphs:
        # only get the relations paragraphs
        for t in types:
            if t in p.text:
                # get anchors from relation paragraph
                anchors = p.find_all('a')
                for a in anchors:
                    relations.append(a.string)

    # put names in correct formatat
    formatted_names = []
    for name in relations:
        name = name.replace(" ","-")
        name = name.lower()
        formatted_names.append(name)

    return formatted_names


# cache files (so don't visit website multiple times when not needed)
def cache_page(dir: str, url: str) -> str:

    # check if in cache
    hash = hashlib.sha1(url.encode("UTF-8")).hexdigest()
    path = dir + "/" + hash
    full_cache_file_path = (os.path.abspath(os.getcwd()) + "/" + path)
    if (os.path.isfile(full_cache_file_path)==False):

        # if not get it and add it to cache dir
        req = requests.get(url, timeout=10)

        # random number of seconds to delay between requests (so they don't block)
        time.sleep(random.randint(0,9))

        if req.status_code == 200:
            print('Success!')
            page = req.text
            with open(path, 'w') as fh:
                fh.write(str(page))
        elif req.status_code == 404:
            print('Not Found.')
            return None

    # return path to file in the cache dir either way
    return path

def main():

    # get info from file
    with open("starter_names.json", 'r') as f:
        starter_names = json.load(f)

    # make cache dir if not already there
    cache_dir = "data/wdw_cache"
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    # new dict of names
    got_names = {}
    
    # add names to list for each category
    for category in starter_names.keys():
        new_names = add_all_names(starter_names.get(category))
        category_list = starter_names.get(category) + new_names
        got_names[category] = category_list

        # longer delay between categories
        time.sleep(random.randint(60, 120))

    # save names to json file
    with open("data/names_to_scrape.json", 'w') as outfile:
        json.dump(got_names, outfile, indent=4)

if __name__ == '__main__':
    main()