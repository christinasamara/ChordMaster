from chord import Node
import time
import pandas as pd
import csv

K = 4
SIZE = 2 ** K
nodes = [Node(i) for i in range(SIZE)]
nodes[0].join(nodes[0])

with open("data.csv", 'r') as file:
    for row in file:
        nodes[0].insert_data(row.strip())

for node in nodes:
    print(len(node.data), end=" ")
print()

for i in range(1, SIZE):
    nodes[0].join(nodes[i])

for node in nodes:
    print(len(node.data), end=" ")
print()

nodes[0].visualize_chord_ring()
nodes[0].delete()
nodes[1].visualize_chord_ring()

for node in nodes:
    print(len(node.data), end=" ")
print()

print(nodes[1].search_query("Massachusetts Institute of Technology", 0))