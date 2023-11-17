import hashlib 
K = 4
SIZE = 2 ** K

class Node:
    def __init__(self, id, prev=None, next=None):
        self.id = id
        self.data = {}
        self.fingerTable = [next] #fingerTable has a length of K+1 {0, 1, ... , K}
        self.prev = prev


    def updateFingerTable(self):
        self.fingerTable[1:] = []
        for i in range(K):
            self.fingerTable.append(self.lookupNode(self.id + 2 ** i))


    def getHashId(self, key):
        return key % SIZE
    

    #in a circle from id1 to id2
    def distance(self, id1, id2):
        if ( id1 <= id2 ):
            return id2 - id1
        else:
            return SIZE - id1 + id2


    def lookupNode(self, node_id, jumps=0):
        hashId = self.getHashId(node_id)

        if (self.id == hashId):
            #print("Jumps: ", jumps)
            return self
        
        #between current node and its successor, successor is returned
        if self.distance(self.id, hashId) <= self.distance(self.fingerTable[0].id, hashId):
            jumps += 1
            #print("Jumps: ", jumps) 
            return self.fingerTable[0]
        
        #iterate through the fingerTable and find the closest node that is __before__ the wanted
        i = 0
        nextNode = self.fingerTable[-1] #initialize as next the final node of the fT. If we don't find a node closer to the wanted this gets returned
        
        for i in range(len(self.fingerTable) -1):
            if (self.distance(self.fingerTable[i].id, hashId) < self.distance(self.fingerTable[i+1].id, hashId)):
                nextNode = self.fingerTable[i]
        jumps += 1
        return nextNode.lookupNode(hashId, jumps)

    
    def join(self, newNode): #each node is joined from its successor
        afterNode = self.lookupNode(newNode.id)

        if (afterNode.id == newNode.id):
            print("Can't have two Nodes with the same ID.")
            return
        
        #update previous and next 
        afterNode.prev.fingerTable[0] = newNode
        newNode.prev = afterNode.prev
        afterNode.prev = newNode
        newNode.fingerTable[0] = afterNode


        #transfer suitable data to newNode and delete them from afterNode
        for key in afterNode.data.keys():
            hashId = self.getHashId(key)
            if (self.distance(hashId, newNode.ID) < self.distance(hashId, afterNode.ID)):
                newNode.data[key] = afterNode.data[key]
                del afterNode.data[key]


    def print(self):
        print("Node id: ", self.id)
        print("Node data: ", self.data)
        print("Node prev: ", self.prev.id)
        for node in self.fingerTable:
            print(node.id, end=", ")
        print()



node0 = Node(0)
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

node0.fingerTable[0] = node1
node0.prev = node2
node1.fingerTable[0] = node2
node1.prev = node0
node2.fingerTable[0] = node0
node3.prev = node1

node0.print()

node0.updateFingerTable()
node1.updateFingerTable()
node2.updateFingerTable()

node0.print()

node0.join(node3)

node0.updateFingerTable()
node1.updateFingerTable()
node2.updateFingerTable()
node3.updateFingerTable()

node1.print()



#πρόβλημα στην getHashId
