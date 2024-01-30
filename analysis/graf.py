import os
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import csv
import numpy as np

# Otwórz pliki z imionami żeńskimi i męskimi
female_names_file = 'imiona_zenskie.csv'
male_names_file = 'imiona_meskie.csv'

with open(female_names_file, 'r', encoding='utf-8') as female_file:
    female_names = set(row[0].lower() for row in csv.reader(female_file))

with open(male_names_file, 'r', encoding='utf-8') as male_file:
    male_names = set(row[0].lower() for row in csv.reader(male_file))

path = os.path.join('C:\\Users\\Użytkownik\\PycharmProjects\\bizraport_scraper_test\\scraper',
                    'companies_persons_data_filtered.json')

file = open(path, 'r', encoding='utf-8')

# wczytaj dane z pliku, każdą linię jako słownik
lines = [eval(line) for line in file]

# weź 2000 pierwszych
lines = lines[:20000]

# usuń przykłady z NoneType w relacjach
lines = [line for line in lines if line['Relacje'] is not None]

G = nx.Graph()
for line in lines:
    if line['Nazwa'] not in G:
        G.add_node(line['Nazwa'])
        G.nodes[line['Nazwa']]['type'] = 'firma'
    for person in line['Relacje']:
        if person not in G:
            G.add_node(person)
        # jeżeli zawiera więcej niż dwa słowa, to nie jest to imię i nazwisko
        if len(person.split()) != 2:
            G.nodes[person]['type'] = 'firma'
        else:
            # Sprawdź czy imię w nazwie wierzchołka jest żeńskie lub męskie
            if person.split()[-1].lower() in female_names:
                G.nodes[person]['type'] = 'osoba'
            elif person.split()[-1].lower() in male_names:
                G.nodes[person]['type'] = 'osoba'
            else:
                G.nodes[person]['type'] = 'firma'
        G.add_edge(line['Nazwa'], person)

# Znalezienie największej spójnej składowej
largest_component = max(nx.connected_components(G), key=len)

# Tworzenie podgrafu z największej spójnej składowej
largest_subgraph = G.subgraph(largest_component)

# połącz wierzchołki firm jeśli stykają się ze sobą w jedną całość, a osoby połączone z firmami przenieś do tej firmy
for node1 in largest_subgraph.nodes():
    for node2 in largest_subgraph.nodes():
        # jeżeli oba są firmami i mają połączenie
        if (
            G.nodes[node1]['type'] == 'firma' and
            G.nodes[node2]['type'] == 'firma' and
            node1 != node2 and
            largest_subgraph.has_edge(node1, node2)
        ):
            # sprawdź stopnie wierzchołków
            degree_node1 = largest_subgraph.degree[node1]
            degree_node2 = largest_subgraph.degree[node2]

            # wybierz wierzchołek o wyższym stopniu
            if degree_node1 >= degree_node2:
                main_node = node1
                merge_node = node2
            else:
                main_node = node2
                merge_node = node1

            # połącz wierzchołki
            largest_subgraph = nx.contracted_nodes(largest_subgraph, main_node, merge_node, self_loops=False)


# Generowanie wykresu z networkx
pos = nx.spring_layout(largest_subgraph)  # Ustawienie układu grafu
# Dodaj kolor czerwony dla firm, niebieski dla osób
node_color = ['red' if G.nodes[node]['type'] == 'firma' else 'blue' for node in largest_subgraph]
# Podpisz wierzchołki korzystając z etykiet
labels = {node: node for node in largest_subgraph.nodes()}
nx.draw_networkx(largest_subgraph, pos, node_size=50, node_color=node_color, edge_color='grey', with_labels=True,
                 labels=labels)
plt.show()

# pokoloruj wierzchołki tak samo jak w networkx
node_color = {'firma': 'red', 'osoba': 'blue'}
for node in largest_subgraph:
    largest_subgraph.nodes[node]['color'] = node_color[largest_subgraph.nodes[node]['type']]

nt = Network()
nt.from_nx(largest_subgraph)
# Generowanie pliku HTML
html_file = 'nx.html'
nt.save_graph(html_file)
