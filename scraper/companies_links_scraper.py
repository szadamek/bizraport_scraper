import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_html_page(url):
    driver.get(url)
    html = driver.page_source
    return html


def get_html_by_viewsource(url):
    html = get_html_page('view-source:' + url)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.text


if __name__ == '__main__':
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    chrome_driver_path = 'C:/Windows/chromedriver.exe'
    options.binary_location = "C:/Windows/chrome-win/chrome.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # https://www.bizraport.pl/organizacje?page=2&zysk_netto_od=500000&zysk_netto_do=2000000
    base_url_part1 = 'https://www.bizraport.pl/organizacje'
    base_url_part2 = 'zysk_netto_od=500000&zysk_netto_do=2000000'
    companies_file = 'companies_filtered.txt'

    companies = []

    if os.path.isfile(companies_file):
        with open(companies_file, 'r', encoding='utf-8') as f:
            for line in f:
                companies.append(line.strip())
    else:
        print('File not found. Creating new file.')
        open(companies_file, 'w', encoding='utf-8').close()

    total_new_companies = 0
    page_num = 2
    while True:
        url = f'{base_url_part1}?page={page_num}&{base_url_part2}'
        print(f'Strona {page_num}: {url}')
        html = get_html_by_viewsource(url)
        soup = BeautifulSoup(html, 'html.parser')

        # For debugging and testing selectors in Chrome
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))

        new_companies = 0
        company_selectors = 'li.card > div > a'

        for a in soup.select(company_selectors):
            print("Found the URL:", a['href'])
            if a['href'] not in companies:
                companies.append(a['href'])
                new_companies += 1
                total_new_companies += 1

        if new_companies == 0:
            break

        with open(companies_file, 'a', encoding='utf-8') as f:
            for company in companies:
                f.write(company + '\n')

        page_num += 1
        time.sleep(random.randint(1, 3))

    print(f'Found {total_new_companies} new companies.')

