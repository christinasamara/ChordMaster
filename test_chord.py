from chord import Node, K, SIZE
import time
import pandas as pd
import csv
import time
from timeit import default_timer as timer
import statistics

join_times = []
deletion_times = []
lookup_times = []

nodes = [Node(i) for i in range(SIZE)]

# First node joining
start = timer()
nodes[0].join(nodes[0])

# Data into Chord
with open("data.csv", 'r') as file:
    for row in file:
        nodes[0].insert_data(row.strip())
end = timer()
join_times.append(end-start)

# Other nodes joining - data is being distributed 
for i in range(1, SIZE):
    start = timer()
    nodes[0].join(nodes[i])
    end = timer()
    join_times.append(end-start)

# print("join_times", join_times)

# VISUAL
nodes[0].visualize_chord_ring()

# LOOKUP TIMES
# for i in range(0, SIZE):
#     for j in range(0, SIZE):
#         start = timer()
#         nodes[i].lookupNode(j)
#         end = timer()
#         lookup_times.append(end-start)

# print("lookup_times", statistics.mean(lookup_times))
# print("lookup_times standard dev", statistics.stdev(lookup_times))


# DELETION TIMES
# for i in range(0, SIZE):
#     start = timer()
#     nodes[i].delete(i)
#     end = timer()
#     deletion_times.append(end-start)


# print("deletion_times", deletion_times)


# SEARCH BY ALMA MATER
# start = timer()
# result = nodes[1].search_education("Massachusetts Institute of Technology", 2)
# end = timer()
# search_time = end-start
# print(result)
# print(search_time)




# SEARCH BY SURNAME AND NAME
# start = timer()
# results= nodes[1].search_scientist("Blum", "Lenore")
# end = timer()
# search_time = end-start
# print(search_time)
# 
# for scientist in results:
#     print("Name: ", scientist)
#     print("Alma Mater: ", results[scientist]["alma mater"])
#     print("Awards: ", results[scientist]["awards"])
#     print()


# PRINT ALL NODE.DATA LENGTHS
# for node in nodes:
#     print(len(node.data), end=" ")
# print()
