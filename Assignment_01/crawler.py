# Usage:
#          python crawl.py

import re
import json
import requests
import os
from utils import load_categories, save_data, get_info, generate_url


def make_request(url):
    response = requests.get(url)
    html_text = response.text
    main_section_rg_str = '(?=<section).*?(?<=</section>)'
    main_section_rg = re.compile(main_section_rg_str, flags=re.I | re.S)
    html_text = re.sub(main_section_rg, '', html_text)
    return html_text


def crawl_by_category(cateName):
    day = 1
    data = []
    while True:
        # print(day)
        text = make_request(generate_url(cateName, day))
        # print(text)
        article_rg_str = '(?=<h3).*?(?<=</h3>)'
        article_regex = re.compile(article_rg_str, flags=re.I | re.S)
        articles = re.findall(article_regex, text)
        if day >= 30:
            break
        if not articles:
            day += 1
            continue

        for article in articles:
            content = get_info(article)
            content["category"] = cateName
            data.append(content)
        day += 1
    return data


def crawby_categories(categories):
    data = []

    for i in range(len(categories)):
        print('{:4d} . Crawling {cate}...'.format(i, cate=categories[i]))
        data = data + crawl_by_category(categories[i])
        print(' -----> Crawl done !')

    return data


if __name__ == '__main__':
    # Load the categoies
    categories = load_categories(os.path.join(os.getcwd(), 'config.json'))
    
    # Crawl data from the categorical config
    crawled_data = crawby_categories(categories)

    # Print the number of crawled data
    print(" ---> The number of articles crawled is {}".format(len(crawled_data)))
    
    # Save crawled data to disk
    path = save_data(data=crawled_data, filepath='./output.jl')
