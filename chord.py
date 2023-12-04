import hashlib 
import networkx as nx
import matplotlib.pyplot as plt
K = 4
SIZE = 2 ** K

class Node:
    def __init__(self, id, prev=None):
        self.id = id
        self.data = {}
        self.fingerTable = [] # fingerTable has a length of K+1 {0, 1, ... , K}
        self.prev = prev


    def updateFingerTable(self):
        self.fingerTable[1:] = []
        for i in range(1, K): #start from 1, we do not delete 0
            self.fingerTable.append(self.lookupNode(self.id + 2 ** i))


    def getHashId(self, key):
        return key % SIZE
    

    # in a circle from id1 to id2
    def distance(self, id1, id2):
        if ( id1 <= id2 ):
            return id2 - id1
        else:
            return SIZE - id1 + id2


    def lookupNode(self, node_id, jumps=0):
        hashId = self.getHashId(node_id)

        if (self.id == hashId):
            # print("Jumps: ", jumps)
            return self
        
        # between current node and its successor, successor is returned
        if self.distance(self.id, hashId) <= self.distance(self.fingerTable[0].id, hashId):
            jumps += 1
            # print("Jumps: ", jumps) 
            return self.fingerTable[0]
        
        # iterate through the fingerTable and find the closest node that is __before__ the wanted
        nextNode = self.fingerTable[-1] # initialize as next the final node of the fT. If we don't find a node closer to the wanted this gets returned
        
        for i in range(len(self.fingerTable) -1):
            if (self.distance(self.fingerTable[i].id, hashId) < self.distance(nextNode.id, hashId)):
                nextNode = self.fingerTable[i]
        jumps += 1
        return nextNode.lookupNode(hashId, jumps)

    
    def join(self, newNode): 
        afterNode = self.lookupNode(newNode.id) # each node is joined from its successor

        if afterNode == newNode:
            # First node is being inserted
            self.prev = newNode
            self.fingerTable.append(newNode)


            # updated by stabilization
            # self.updateFingerTable()
            self.stabilization()

        elif (afterNode.id == newNode.id):
            print("Can't have two Nodes with the same ID.")
            return
        
        else: 
            # we found an afternode, update previous and next and FT
            afterNode.prev.fingerTable[0] = newNode
            newNode.prev = afterNode.prev
            afterNode.prev = newNode
            newNode.fingerTable.append(afterNode)

            # transfer suitable data to newNode and delete them from afterNode
            # for key in afterNode.data.keys():
            #     hashId = self.getHashId(key)
            #     if (self.distance(hashId, newNode.ID) < self.distance(hashId, afterNode.ID)):
            #         newNode.data[key] = afterNode.data[key]
            #         del afterNode.data[key]
                    
            # being updated by stabilization
            # newNode.updateFingerTable()
            newNode.stabilization()

    def ins_stabilization(node, startnode):
        node.updateFingerTable()
        next_node = node.fingerTable[0]
        if next_node != startnode:
            next_node.ins_stabilization(startnode)  # Recursive call using the method of the current node

    def stabilization(self):
        startnode = self
        self.ins_stabilization(startnode)
        # add timer so stabilizarion() is running frequently





    def delete(self):
        if (self.prev == self and self.next == self):
            # only node in chord
            # clean its data
            pass
        else:
            self.prev.fingerTable[0] = self.fingerTable[0]
            self.fingerTable[0].prev = self.prev

            # transfer the data to the next node
            # for key, value in self.data.items():
            #     self.fingerTable[0].data[key] = value


            # they are being updated by stabilization anyway
            # self.prev.updateFingerTable()
            # self.fingerTable[0].updateFingerTable()

            self.prev.stabilization()


    def visualize_chord_ring(self):
        G = nx.DiGraph()

        current_node = self
        start_node = self

        while True:
            G.add_node(current_node.id)
            G.add_edge(current_node.id, current_node.fingerTable[0].id)

            current_node = current_node.fingerTable[0]
            if current_node == start_node:
                break

        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, arrowsize=20, node_size=700, node_color="skyblue", font_size=8)
        plt.title("Chord Ring Visualization")
        plt.show()


    def print(self):
        print("Node id: ", self.id)
        print("Node data: ", self.data)
        #print("Node prev: ", self.prev.id)
        if self.fingerTable:
            for node in self.fingerTable:
                print(node.id, end=", ")
        else:
            print("[]")
        print()





nodes = [Node(i) for i in range(16)]


nodes[0].join(nodes[0])
for i in range(1, 16):
    nodes[0].join(nodes[i])
nodes[0].visualize_chord_ring()

nodes[0].delete()

nodes[1].visualize_chord_ring()




