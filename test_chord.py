from chord import Node
import time
import pandas as pd
import csv
import time
from timeit import default_timer as timer
import statistics

K = 4
SIZE = 2 ** K

join_times = []
delete_times = []
lookup_times = []

nodes = [Node(i) for i in range(SIZE)]
start = timer()
nodes[0].join(nodes[0])

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

nodes[5].delete()



nodes[0].visualize_chord_ring()

# for i in range(0, SIZE):
#     for j in range(0, SIZE):
#         start = timer()
#         nodes[i].lookupNode(j)
#         end = timer()
#         lookup_times.append(end-start)


# for i in range(0, SIZE):
#     start = timer()
#     nodes[i].delete()
#     end = timer()
#     delete_times.append(end-start)






# print("join_times", join_times)
# print("delete_times", delete_times)
# print("lookup_times", statistics.mean(lookup_times))

# for node in nodes:
#     print(len(node.data), end=" ")
# print()

# result = nodes[1].search_education("Massachusetts Institute of Technology", 0)
# print(result)
# 




results= nodes[1].search_scientist("Blum")
for scientist in results:
    print("Name: ", scientist)
    print("Alma Mater: ", results[scientist]["alma mater"])
    print("Awards: ", results[scientist]["awards"])
    print()