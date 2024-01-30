from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import os


def get_html_page(url):
    driver.get(url)
    html = driver.page_source
    return html


def get_html_by_viewsource(url):
    html = get_html_page('view-source:' + url)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.text


def handle_response(response):
    if response:
        print(response.json())  # Przetwarzaj odpowiedź tak, jak jest to wymagane
    else:
        print('Failed to get response')
        print(response.status_code)

    return response


if __name__ == '__main__':
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    chrome_driver_path = 'C:/Windows/chromedriver.exe'
    options.binary_location = "C:/Windows/chrome-win/chrome.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    base_url = 'https://www.bizraport.pl/'

    # wczytywanie listy firm z pliku do listy
    companies_file = 'companies_filtered_no_duplicates_new.txt'
    companies = []
    if os.path.isfile(companies_file):
        with open(companies_file, 'r', encoding='utf-8') as f:
            for line in f:
                companies.append(line.strip())
    else:
        print('File not found. Creating new file.')
        open(companies_file, 'w', encoding='utf-8').close()

    for company in companies:
        print(f'Firma {base_url + company}')
        html = get_html_by_viewsource(base_url + company)
        soup = BeautifulSoup(html, 'html.parser')

        # For debugging and testing selectors in Chrome
        with open('test_parameters.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))

        # NAZWA FIRMY | KRS | NIP | REGON
        params_selector_name = 'body > div > div.flex.justify-center > div > div:nth-child(2) > div > div.lg\\:col-span-8.mt-1.lg\\:mt-24 > div.grid.grid-flow-row-dense.lg\\:grid-cols-10 > h1 > span.flex.justify-center.lg\\:justify-start.text-2xl.font-semibold.tracking-tight.mb-1.ml-2'
        params_selector_KRS_NIP_REGON = 'body > div.min-h-screen > div.flex.justify-center > div > div:nth-child(2) > div > div.lg\\:col-span-8.mt-1.lg\\:mt-24 > div.grid.grid-flow-row-dense.lg\\:grid-cols-10 > h1 > span.grid.grid-flow-row-dense.grid-cols-3.mx-2.lg\\:mx-5.mb-1.lg\\:mb-0 > span'
        params_selector_rest = 'body > div.min-h-screen > div.flex.justify-center > div > div:nth-child(2) > div > div.lg\\:col-span-8.mt-1.lg\\:mt-24 > div:nth-child(2) > div.grid.grid-cols-2.gap-3.mx-3.mt-3.lg\\:grid-cols-4.lg\\:gap-8.lg\\:mx-8 > div > div > div'
        params_selector_basic_info = 'body > div.min-h-screen > div.flex.justify-center > div > div:nth-child(2) > div > div.lg\\:col-span-8.mt-1.lg\\:mt-24 > div:nth-child(2) > div.mt-5.mx-3.lg\\:mx-8 > div > div.lg\\:col-span-3 > div > div.collapse-content.px-0 > div'
        params_selector_relations = 'body > div > div.flex.justify-center > div > div:nth-child(2) > div > div.lg\\:col-span-8.lg\\:mt-24 > div:nth-child(18) > section > noscript > ul > li > a'
        params_tr_1 = soup.select(params_selector_KRS_NIP_REGON)
        params_tr_2 = soup.select(params_selector_rest)
        params_tr_3 = soup.select(params_selector_basic_info)
        params_tr_4 = soup.select(params_selector_relations)
        params = {}

        params['Nazwa'] = soup.select(params_selector_name)[0].text.strip()

        for param in params_tr_1:
            params[param.text.split(' ')[0]] = param.text.split(' ')[-1]

        for param in params_tr_2:
            params[param.text.split(' ')[1]] = ' '.join(param.text.split(' ')[-2:])

        for param in params_tr_3:
            value = param.select('div')[0].text
            name = param.find(string=True, recursive=False).strip()
            params[name] = value

        params['Relacje'] = []
        for a in soup.select(params_selector_relations):
            params['Relacje'].append(a.text.split('-', 1)[0].strip())

        print(params)

        # Dopisz do pliku firmę i jej parametry
        with open('companies_persons_data_filtered.json', 'a', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False)
            f.write('\n')
