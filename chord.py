import hashlib 
import networkx as nx
import matplotlib.pyplot as plt
import holoviews as hv
from holoviews import opts, dim
hv.extension('bokeh')
import pandas as pd
import hashing


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
        for i in range(1, K): #start from 1, we do not delete 0, which is the next one
            self.fingerTable.append(self.lookupNode(self.id + 2 ** i))


    def getHashId(self, key):
        return key % SIZE
    


    # in a circle from id1 to id2
    def distance(self, id1, id2):
        if ( id1 <= id2 ):
            return id2 - id1
        else:
            return SIZE - id1 + id2


    def lookupNode(self, node_id):
        hashId = self.getHashId(node_id)

        if (self.id == hashId):
            return self
        
        # between current node and its successor, successor is returned
        if self.distance(self.id, hashId) <= self.distance(self.fingerTable[0].id, hashId):
            return self.fingerTable[0]
        
        # iterate through the fingerTable and find the closest node that is __before__ the wanted
        nextNode = self.fingerTable[-1] # initialize as next the final node of the fT. If we don't find a node closer to the wanted this gets returned
        
        for i in range(len(self.fingerTable) -1):
            if (self.distance(self.fingerTable[i].id, hashId) < self.distance(nextNode.id, hashId)):
                nextNode = self.fingerTable[i]
        return nextNode.lookupNode(hashId)

    
    def join(self, newNode): 
        afterNode = self.lookupNode(newNode.id) # each node is joined from its successor

        if afterNode == newNode:
            # First node is being inserted
            self.prev = newNode
            self.fingerTable.append(newNode)

            # updated by stabilization
            self.updateFingerTable()
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
            to_delete = []

            # transfer suitable data to newNode and delete them from afterNode
            for key, value in afterNode.data.items():
                hashId = hashing.hashed(key) % SIZE
                if (self.distance(hashId, newNode.id) < self.distance(hashId, afterNode.id)):
                    newNode.data[key] = afterNode.data[key]
                    # mark which entries are to be deleted since transfered
                    to_delete.append(key)
            # delete them
            for key in to_delete:
                del afterNode.data[key]
            
            # being updated by stabilization ??? enas elegxos edw
            newNode.updateFingerTable()
            newNode.stabilization()


    def insert_data(self, row):
        name, universities, awards = row.split(",")

        # find corresponding chord node
        education = universities.split("@") # it's a list
        for edu in education:
            hashed_key = hashing.hashed(edu)
            node_home = self.lookupNode(hashed_key)

            if edu not in node_home.data.keys():
                node_home.data[edu] = {name: awards}
            
            else:
                node_home.data[edu][name] = awards

    def search_education(self, education_string, awards):
        hashed_education = hashing.hashed(education_string) % SIZE
        result_list = []
        search_node = self.lookupNode(hashed_education)
        if education_string in search_node.data.keys():
            for value in search_node.data.values():
                for name, n_awards in value.items():
                    if int(n_awards) >= awards:
                        result_list.append(name)
            

        return result_list
    

    def search_scientist(self, scientist_surname, scientist_name=None):
        result_list = []

        # Search in the current node
        for key, value in self.data.items():
            for key2 in value.keys():
                if scientist_surname in value.keys(): # and (scientist_name is None or scientist_name == value.get('name', '')):
                    result_list.append(key)

        # Search in the finger table nodes
        current_node = self.fingerTable[0]
        visited_nodes = set()
        visited_nodes.add(self.id)
        while current_node != self and current_node.id not in visited_nodes:
            visited_nodes.add(current_node.id)

            for key, value in current_node.data.items():
                for key2 in value.keys():
                    if scientist_surname in key2: # and (scientist_name is None or scientist_name == value.get('name', '')):
                        result_list.append(key)

            # Move to the next node in the finger table
            current_node = current_node.fingerTable[0] if current_node.fingerTable else self

        return result_list, visited_nodes


    def stabilization(self):
        self.updateFingerTable()
        current = self.fingerTable[0]
        while current != self:
            current.updateFingerTable()
            current = current.fingerTable[0]

        # add timer so stabilizarion() is running frequently


    def delete(self):
        if (self.prev == self and self.fingerTable[0] == self):
            self.data.clear()
            pass
        else:
            extra_node = self.prev
            self.prev.fingerTable[0] = self.fingerTable[0]
            self.fingerTable[0].prev = self.prev


            # transfer the data to the next node
            for key, value in self.data.items():
                self.fingerTable[0].data[key] = value
            self.data.clear()

            # they are being updated by stabilization anyway
            self.prev.updateFingerTable()
            self.fingerTable[0].updateFingerTable()
            
            deleted_node = self
            startnode = self.prev
            current_node = startnode.fingerTable[0]
            while True:
                if current_node == startnode:
                    break
                for i in range(len(current_node.fingerTable)):
                    if current_node.fingerTable[i] == deleted_node:
                        current_node.fingerTable[i] = deleted_node.fingerTable[0]
                current_node = current_node.fingerTable[0]



            self.prev.stabilization()



    def visualize_chord_ring(self):
        links = []
        current_node = self
        start_node = self
        while True:
            # Add links for finger table connections
            for finger_node in current_node.fingerTable:
                links.append((current_node.id, finger_node.id))

            current_node = current_node.fingerTable[0]
            if current_node == start_node:
                break
        # Convert links to a DataFrame
        links_df = pd.DataFrame(links, columns=['source', 'target'])
        # Create Chord diagram using Holoviews
        chord_diagram = hv.Chord(links_df)
        # Customize appearance
        chord_diagram.opts(
            opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), labels='index', node_color='index')
        )
        # Display the Chord diagram
        hv.save(chord_diagram, 'chord_diagram.html')  # Optionally save as HTML file
        hv.render(chord_diagram)

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


