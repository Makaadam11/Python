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

cluster_method =''

cluster_input = input("Wpisz metodę klastrowania: \n1) Funkcja używająca jądra Gaussa (RBF) z odległością euklidesową wpisz: rbf \n2) Funkcja używająca K-macierz łączności najbliższych sąsiadów wpisz: knn\n")

if cluster_input == 'knn':
    cluster_method = 'nearest_neighbors'
if cluster_input == 'rbf':
    cluster_method = 'rbf'    

cluster_number = input("Wpisz ilość klastrów: ")


result = []
csv_result = []

def MAX(sets):
    return (max(sets))

# SpectralClustering to metoda agregacji danych, która działa poprzez znajdowanie skupień w danych za pomocą analizy spektralnej
# macierzy sąsiedztwa. # Jeśli użyjesz parametru `assign_labels='kmeans' algorytm ten działa w następujący sposób:

# 1) Obliczenie macierzy sąsiedztwa: Na początku algorytm oblicza macierz sąsiedztwa dla danych wejściowych. Macierz sąsiedztwa 
# jest macierzą rzędową, w której wiersze i kolumny odpowiadają poszczególnym próbkom danych, a wartości na jej przekątnej są równe 0. 
# Wartości poza przekątną są równe 1, jeśli dane próbki są sąsiadami, lub 0, jeśli nie są. Sąsiadami nazywamy próbki, które są blisko siebie według określonej miary odległości.

# 2) Obliczenie macierzy laplasjanu: Następnie algorytm oblicza macierz laplasjanu, która jest pochodną macierzy sąsiedztwa.
#  Macierz ta jest używana do określenia podobieństwa między próbkami danych.

# 3) Redukcja wymiarów: Następnie algorytm wykonuje redukcję wymiarów na macierzy laplasjanu, aby zmniejszyć wymiar danych wejściowych. 
# Redukcja wymiarów polega na znalezieniu kombinacji składowych macierzy, które najlepiej opisują dane wejściowe.

# 4) Grupowanie danych: Na końcu algorytm grupuje dane wejściowe za pomocą metody k-średnich (kmeans), 
# wykorzystując zredukowane wymiary jako cechy. Metoda k-średnich działa poprzez iteracyjne przypisywanie każdej 
# próbki do najbliższej grupy (centroidu) i aktualizowanie centroidów w oparciu o nowe przypisania.


# Jeśli ustawisz parametr affinity na 'rbf' podczas wywoływania funkcji SpectralClustering z biblioteki scikit-learn, 
# algorytm będzie używać jądrowej funkcji RBF (Radial Basis Function, funkcja bazowa radialna) 
# do obliczenia macierzy podobieństwa między punktami danych. Jądrowa funkcja RBF to funkcja, która jest znormalizowana tak, 
# aby mieć wartość równą 1 dla punktu, w którym jest wywoływana, oraz malejącą wartość wraz z oddalaniem się od tego punktu.
# W praktyce oznacza to, że algorytm SpectralClustering będzie używał macierzy podobieństwa opartej na odległości euklidesowej między punktami danych. 
# Punkty blisko siebie będą miały wysokie podobieństwo, a punkty daleko od siebie będą miały niskie podobieństwo. 
# Algorytm klasteryzacji będzie następnie używał tej macierzy podobieństwa do grupowania punktów w klastry.
# Jądrowa funkcja RBF jest często używana w algorytmach klasteryzacji, ponieważ pozwala ona na uzyskanie dobrych wyników dla danych o dużym rozmiarze 
# lub gdy istnieją silne powiązania między punktami danych. 
# Jeśli jednak dane są szczególnie skomplikowane lub nieregularne, inne rodzaje jądrowych funkcji podobieństwa mogą działać lepiej.

# Jeśli ustawisz parametr affinity na 'nearest_neighbors' podczas wywoływania funkcji SpectralClustering z biblioteki scikit-learn, 
# algorytm będzie używał macierzy podobieństwa opartej na najbliższych sąsiadach punktów danych do obliczenia macierzy laplasjanu. 
# W tym przypadku macierz podobieństwa będzie miała wartość 1 dla par punktów, które są najbliższymi sąsiadami,  a 0 dla pozostałych par punktów.

# Ogólnie rzecz biorąc, algorytm SpectralClustering będzie używał macierzy podobieństwa opartej na najbliższych sąsiadach 
# do grupowania punktów w klastry w sposób, w którym punkty blisko siebie są bardziej prawdopodobne, że znajdą się w tym samym klasterze. 
# Ten rodzaj macierzy podobieństwa jest szczególnie przydatny w przypadku danych, w których istnieją silne powiązania między punktami blisko siebie.

# n_clusters: liczba klastrów.


model = SpectralClustering(n_clusters=(int)(MAX(cluster_number)), affinity=cluster_method,assign_labels='kmeans')
labels = model.fit_predict(points)

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

         # This will store the resultant MST
        
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
            
            array2 = [int(u),weight,int(v)]
            csv_result.append(array2)
            arr.append(weight)
            iter += 1
            minimumCost += weight

            print("%d -- %d == %f" % (u, v, weight))
        print('\n')     
        print("Minimum Spanning Tree" , minimumCost)  
        print('\n')  
                               


graph = Graph(size)

for i in range(0,size):

    for j in range(0,size):
        
        if(i!=j):
            
            
            a = numpy.array([parsedCSV[i][0],parsedCSV[i][1]],dtype='f')
            b = numpy.array([parsedCSV[j][0],parsedCSV[j][1]],dtype='f')
            weight = numpy.linalg.norm(a-b)
            graph.addEdge(i, j, weight) 
 

graph.KruskalMST() 

csv_result2 = []

csv_result = numpy.asarray(csv_result)

with open(str(path)+"\\distances.csv", 'a',newline='' ) as file:
    writer = csv.writer(file)
    
    points_header = ['point 1','distance p1-p2','point 2']
   
    writer.writerow(points_header) 

    for px in range (0,size-1):       
        writer.writerow(csv_result[px]+labels[px])

with open(str(path)+"\\clusters.csv", 'a',newline='' ) as file:
    writer = csv.writer(file)
    
    points_header2 = ['cord_x','cord_y','cluster']
   
    for px in range (0,len(points)-1):
        array3 = [points[px,0],points[px,1],labels[px]]
        csv_result2.append(array3)

    writer.writerow(points_header2) 

    for px in range (0,size-1):       
        writer.writerow(csv_result2[px])        
    

plt.scatter(points[:, 0], points[:, 1], c=labels,s=25, cmap='viridis')


plt.show()     