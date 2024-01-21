from chord import Node
import time
import pandas as pd
import csv
import time
from timeit import default_timer as timer
K = 5
SIZE = 2 ** K

join_times = []
delete_times = []

nodes = [Node(i) for i in range(SIZE)]
start = timer()
nodes[0].join(nodes[0])
nodes[0].visualize_chord_ring()

with open("data.csv", 'r') as file:
    for row in file:
        nodes[0].insert_data(row.strip())
end = timer()
join_times.append(end-start)

# PRINT ALL NODE.DATA LENGTHS
# for node in nodes:
#     print(len(node.data), end=" ")
# print()

for i in range(1, SIZE):
    start = timer()
    nodes[0].join(nodes[i])
    end = timer()
    join_times.append(end-start)


nodes[0].visualize_chord_ring()

for i in range(0, SIZE):
    start = timer()
    nodes[i].delete()
    end = timer()
    delete_times.append(end-start)

print("join_times", join_times)
print("delete_times", delete_times)


# for node in nodes:
#     print(len(node.data), end=" ")
# print()

# print(nodes[1].search_education("Massachusetts Institute of Technology", 0))
# 
# results, v= nodes[1].search_scientist("Rehman")
# print(results, v)