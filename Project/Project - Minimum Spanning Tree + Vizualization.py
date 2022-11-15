import csv
import numpy 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from pathlib import Path

path = Path(__file__).parent.absolute()

number = input("Wybierz numer pliku z danymi do oczytania (0-5): ")
name=""

if number == '0':
    name = str(path) +"\data_0"
elif number == '1':
    name = str(path) +"\data_1"
elif number == '2':
    name = str(path) +"\data_2"
elif number == '3':
    name = str(path) +"\data_3"
elif number == '4':
    name = str(path) +"\data_4"
elif number == '5':
    name = str(path) +"\data_5"


parsedCSV = numpy.array(list(csv.reader(open(name + ".csv", "r"), delimiter=",")))[1:]
points = numpy.array([[float(x), float(y), int(z)] for x, y, z in parsedCSV])

size = (len(parsedCSV)) 

cluster_number = set()

for i in range(0,size):
    cluster_number.add(parsedCSV[i][2])
 

class Graph:

    def __init__(self, vertices):
        self.V = vertices # No. of vertices
        self.graph = [] # default dictionary
        # to store graph

    # function to add an edge to graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        # If ranks are same, then make one as root
        # and increment its rank by one
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    # The main function to construct MST using Kruskal's
        # algorithm
    def KruskalMST(self):

        result = [] # This will store the resultant MST
        
        # An index variable, used for sorted edges
        i = 0
        
        # An index variable, used for result[]
        e = 0

        # Step 1: Sort all the edges in
        # non-decreasing order of their
        # weight. If we are not allowed to change the
        # given graph, we can create a copy of graph
        self.graph = sorted(self.graph,
                            key=lambda item: item[2])

        parent = []
        rank = []

        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while e < self.V - 1:

            # Step 2: Pick the smallest edge and increment
            # the index for next iteration
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            
            # If including this edge doesn't
            # cause cycle, include it in result
            # and increment the indexof result
            # for next edge
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            # Else discard the edge

        arr = numpy.empty(len(result),dtype=float)
        
        
        minimumCost = 0
        iter = 0
        arr = list()

        print ("Edges in the constructed MST")
        for u, v, weight in result:
            
            arr.append(weight)
            iter += 1
            minimumCost += weight
            
            print("%d -- %d == %f" % (u, v, weight))
        print('\n')     
        print("Minimum Spanning Tree" , minimumCost)  
        print('\n')  
                               
def MAX(sets):
    return (max(sets))

graph = Graph(size)

for i in range(0,size):

    for j in range(0,size):
        
        if(i!=j):
            
            a = numpy.array([parsedCSV[i][0],parsedCSV[i][1]],dtype='f')
            b = numpy.array([parsedCSV[j][0],parsedCSV[j][1]],dtype='f')
            weight = numpy.linalg.norm(a-b) 
            graph.addEdge(i, j, weight) 
 

graph.KruskalMST() 


model = SpectralClustering(n_clusters=((int)(MAX(cluster_number))+1), affinity='nearest_neighbors',assign_labels='kmeans')
labels = model.fit_predict(points)
plt.scatter(points[:, 0], points[:, 1], c=labels,s=50, cmap='viridis')


plt.show()     