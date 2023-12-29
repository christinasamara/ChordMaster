from chord import Node
import time


K = 4
SIZE = 2 ** K
nodes = [Node(i) for i in range(SIZE)]
nodes[0].join(nodes[0])
for i in range(1, SIZE):
    nodes[0].join(nodes[i])
nodes[0].visualize_chord_ring()
time.sleep(10)
nodes[0].delete()
nodes[1].visualize_chord_ring()





