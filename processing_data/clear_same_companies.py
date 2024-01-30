import os

path = os.path.join('C:\\Users\\Użytkownik\\PycharmProjects\\bizraport_scraper_test\\scraper', 'companies_filtered.txt')

file = open(path, 'r', encoding='utf-8')

# zczytaj linki po wierszach
lines = file.readlines()

# usuń duplikaty
lines = list(dict.fromkeys(lines))

# zapisz do pliku
save_path = os.path.join('C:\\Users\\Użytkownik\\PycharmProjects\\bizraport_scraper_test\\scraper', 'companies_filtered_no_duplicates_new.txt')

file = open(save_path, 'w', encoding='utf-8')

for line in lines:
    file.write(line)

file.close()
