import hashlib 
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
            for key in afterNode.data.keys():
                hashId = self.getHashId(key)
                if (self.distance(hashId, newNode.ID) < self.distance(hashId, afterNode.ID)):
                    newNode.data[key] = afterNode.data[key]
                    del afterNode.data[key]
                    
            # being updated by stabilization
            # newNode.updateFingerTable()
            newNode.stabilization()

    def ins_stabilization(node, startnode):
        print("another one")
        node.updateFingerTable()
        next_node = node.fingerTable[0]
        if next_node != startnode:
            next_node.ins_stabilization(startnode)  # Recursive call using the method of the current node

    def stabilization(self):
        startnode = self
        self.ins_stabilization(startnode)





    def delete(self):
        if (self.prev == self and self.next == self):
            # only node in chord
            # clean its data
            pass
        else:
            self.prev.fingerTable[0] = self.fingerTable[0]
            self.fingerTable[0].prev = self.prev

            # transfer the data to the next node
            for key, value in self.data.items():
                self.fingerTable[0].data[key] = value


            # they are being updated by stabilization anyway
            # self.prev.updateFingerTable()
            # self.fingerTable[0].updateFingerTable()

            self.prev.stabilization()


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



node0 = Node(0)
node0.join(node0)

node0.print()

print("~~~~~~~~~~")

node1 = Node(1)
node0.join(node1)

node0.print()
node1.print()

print("~~~~~~~~~~")

node2 = Node(2)
node0.join(node2)

node0.print()
node1.print()
node2.print()

print("~~~~~~~~~~")

# node2.delete()
# 
# node0.print()
# node1.print()

print("~~~~~~~~~~")

node15 = Node(15)
node0.join(node15)

node0.print()
node1.print()
node2.print()
node15.print()




