import os

path = os.path.join('C:\\Users\\Użytkownik\\PycharmProjects\\bizraport_scraper_test\\scraper', 'companies_data_filtered.json')

file = open(path, 'r', encoding='utf-8')

# wczytaj dane z pliku, każdą linię jako słownik
lines = []
for line in file:
    lines.append(eval(line))

# # sprawdź czy są duplikaty, jeśli tak to wypisz
# duplicates = []
# for line in lines:
#     if lines.count(line) > 1:
#         duplicates.append(line)
#
# print(duplicates)
#
# # usuń duplikaty
# lines = list(dict.fromkeys(lines))
#
# # zapisz do pliku
# save_path = os.path.join('C:\\Users\\Użytkownik\\PycharmProjects\\bizraport_scraper_test\\scraper', 'companies_data_filtered_no_duplicates.json')
#
# file = open(save_path, 'w', encoding='utf-8')
#
# for line in lines:
#     file.write(line)
#
# file.close()

for company in lines:
    # usuń 'mln' lub 'tys' z wartości
    if company['zysk'][-3:] == 'mln':
        company['zysk'] = company['zysk'][:-4]
        # zamień , na .
        company['zysk'] = company['zysk'].replace(',', '.')
        if float(company['zysk']) > 2:
            print(company['zysk'])
