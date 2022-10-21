import os
import argparse
import json
from bs4 import BeautifulSoup
import pandas as pd
from get_names import cache_page

# clean input
def clean_input(config: dict[str]) -> list[str]:
    
    # put names into single list
    names = []
    for v in config.values():
        names += v

    # remove duplicates
    names = list(dict.fromkeys(names))
    
    return names

# fetch data
def fetch_data(page: str, name: str) -> dict:

    # open file with beautifulsoup to start scraping
    soup = BeautifulSoup(open(page, 'r'), 'html.parser')

    # fetch info & relations
    data = fetch_info(soup)
    relations = fetch_relations(name, soup)
    data['num_relations'] = len(relations) 

    return data

# fetch relationship & corresponding data
def fetch_relations(name: str, soup: BeautifulSoup) -> list[str]:

    # list to add relations to
    relations = list()

    # find div that contains paragraphs that list relations
    block = soup.find('div', class_='ff-block-content dating-profile')

    # get all types of relationships
    types = ['was previously married to', 'has been in relationships with', 'has had encounters with', 
                'is rumoured to have hooked up with', 'has been engaged to']

    # if currently in relationship
    try:
        current = soup.find('div', style='position:relative;width:51%;padding-left:108px;height:130px;margin-bottom:20px;')
        a = current.find('a')
        # make sure it's returning the relation not the person themselves
        # (depends on how the sentence was written)
        first_name = a.string.split()[0].lower()
        # if it's the target, get their relation instead
        if first_name in name:
            a = current.find_all('a')
            relations.append(a[1].string)
        else:
            relations.append(a.string)
    except:
        pass

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
    return relations

def fetch_info(soup: BeautifulSoup) -> dict:

    # dict to add info to
    info = {}

    # get age, eye colour, zodiac, sexuality, religion, ethnicity, nationality, occupation

    features = ["Age", "Eye Color", "Zodiac Sign", "Sexuality", "Religion", "Ethnicity", "Nationality", "Occupation"]

    table = soup.find('h4', class_="ff-auto-details").find_next_sibling()

    # iterate through list of features
    for feature in features:

        # try to find each feature
        label = table.find('td', text=feature)

        if label != None:
            # if found, add data
            value = label.find_next_sibling('td').text.split()
            if len(value) == 1 or feature=="Age" or feature=="Eye Color":
                info[feature] = value[0]
            else:
                info[feature] = ' '.join(value)

    return info

def main():
    
    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help = "config filename")
    parser.add_argument("-o", help = "output filename")
    args = parser.parse_args()
    input = args.c
    output = "data/" + args.o

    # get info from config file
    with open(input, 'r') as f:
        config = json.load(f)

    cleaned_input_names = clean_input(config)

    cache_dir = "data/wdw_cache"
    # make cache dir if not already there
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    # make new list of urls
    urls = []
    for name in cleaned_input_names:
        url = "https://www.whosdatedwho.com/dating/" + name
        urls.append(url)

    # make paired list of names & urls
    pairs = zip(cleaned_input_names, urls)
    
    # get data
    final = {}
    for name, url in pairs:

        # cache file &/or get path to cache file
        path_to_cachef = cache_page(cache_dir, url)

        if (path_to_cachef != None):

            # fetch info from the cache file
            info = fetch_data(path_to_cachef, name)

            # output json of relations
            final[name] = info
    
    # turn dict into df and df into csv
    df = pd.DataFrame(final).transpose()
    with open(output, "w") as out_file:
        df.to_csv(out_file)

if __name__ == '__main__':
    main()