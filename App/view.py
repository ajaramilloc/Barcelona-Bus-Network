import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
assert cf

def printMenu():
    print("Bienvenido")
    print("0- Load information")
    print("1- Buscar un camino posible entre dos estaciones")
    print("2- Buscar el camino con menos paradas entre dos estaciones")
    print("3- Reconocer los componentes conectados de la Red de rutas de bus")
    print("6- Buscar el camino con mínima distancia entre una estación de origen y un vecindario de destino")
    print("7- Encontrar un posible camino circular desde una estación de origen")

analyzer = None

def newController() -> dict:
    """
    Initialize the dictionary that contains all the information, transfer to the controller
    """
    control: dict = controller.newController()
    return control

def loadData() -> tuple:
    """
    Load all the information from the archives, transer to the controller
    """
    return controller.loadData(analyzer)

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        analyzer = newController()
        print("Loading the information from the archives ....")
        area = loadData()
        digraph = analyzer["connections_digraph"]
        graph = analyzer["connections_graph"]

        print("\n===================================")
        print("# Latitude: " + "min latitude: " + area[0][1] + " | " + "max latitude: " + area[0][0])
        print("# Longitude: " + "min longitude: " + area[0][3] + " | " + "max longitude: " + area[0][2])
        print("===================================\n")

        print("===================================")
        print("# Exclusive Stops: " + str(area[1]))
        print("# Share Stops: " + str(area[2]))
        print("===================================\n")

        print("===================================")
        print("DIGRAPH:")
        print("# Vertices: " + str(lt.size(gr.vertices(digraph))))
        print("# Edges: " + str(lt.size(gr.edges(digraph))))
        print("===================================\n")
        
        for i in lt.iterator(area[0][4]):
            print("ID: " + i["ID"] + " | Code: " + i["Code"] + " | Bus Stop: " + i["Bus_Stop"] + " | Longitude: " + i["Longitude"] + " | Latitude: " + i["Latitude"] + " | Indegree: " + str(i["indegree"]) + " | Outdegree: " + str(i["outdegree"]))

        for i in lt.iterator(area[0][5]):
            print("ID: " + i["ID"] + " | Code: " + i["Code"] + " | Bus Stop: " + i["Bus_Stop"] + " | Longitude: " + i["Longitude"] + " | Latitude: " + i["Latitude"] + " | Indegree: " + str(i["indegree"]) + " | Outdegree: " + str(i["outdegree"]))

        print("\n")
        
        print("\n===================================")
        print("GRAPH:")
        print("# Vertices: " + str(lt.size(gr.vertices(graph))))
        print("# Edges: " + str(graph["edges"]))
        print("===================================\n")

        for i in lt.iterator(area[0][6]):
            print("ID: " + i["ID"] + " | Code: " + i["Code"] + " | Bus Stop: " + i["Bus_Stop"] + " | Longitude: " + i["Longitude"] + " | Latitude: " + i["Latitude"] + " | Degree: " + str(i["degree"]))

        for i in lt.iterator(area[0][7]):
            print("ID: " + i["ID"] + " | Code: " + i["Code"] + " | Bus Stop: " + i["Bus_Stop"] + " | Longitude: " + i["Longitude"] + " | Latitude: " + i["Latitude"] + " | Degree: " + str(i["degree"]))

        print("\n")

    elif int(inputs[0]) == 1:
        origin = input("Enter the origin station: ")
        destiny = input("Enter the destiny station: ")

        path = controller.requirement1(analyzer, origin, destiny)

        if path == 0:
            print(f'No hay camino desde la estación {origin} hacia la estación {destiny}')
        else:
            print("\n===================================")
            print(f"Total distance: {path[2]}")
            print("===================================\n")

            print("===================================")
            print(f"Total transfers: {path[1]}")
            print("===================================\n")

            print("===================================")
            print(f"Path:")
            print("===================================\n")

            for i in lt.iterator(path[0]):
                print(i["vertexA"] + " -> " + i["vertexB"] + " | distNext: " + str(i["weight"]))

        print("\n")

    elif int(inputs[0]) == 2:
        origin = input("Enter the origin station: ")
        destiny = input("Enter the destiny station: ")

        path = controller.requirement2(analyzer, origin, destiny)

        if path == 0:
            print(f'No hay camino desde la estación {origin} hacia la estación {destiny}')
        else:

            print("\n===================================")
            print(f"Total distance: {path[2]}")
            print("===================================\n")

            print("===================================")
            print(f"Total transfers: {path[1]}")
            print("===================================\n")

            print("===================================")
            print(f"Path:")
            print("===================================\n")

            for i in lt.iterator(path[0]):
                print(i["vertexA"] + " -> " + i["vertexB"] + " | distNext: " + str(i["weight"]))

        print("\n")

    elif int(inputs[0]) == 3:
        components = controller.requirement3(analyzer)

        print("\n===================================")
        print(f"Total components: {components[1]}")
        print("===================================\n")

        for component in lt.iterator(components[0]):
            component_size = lt.size(component["component"])
            first_3 = lt.subList(component["component"], 1, 3)
            last_3 = lt.subList(component["component"], component_size - 2, 3)

            print("===================================")
            print(f"Total stations: {component_size}\n")
            print("First 3 stations: ")

            for station in lt.iterator(first_3):
                print(station)

            print("\n")

            print("Last 3 stations: ")
            
            for station in lt.iterator(last_3):
                print(station)

            print("===================================\n")

        print("\n")

    elif int(inputs[0]) == 6:
        origin = input("Enter the origin station: ")
        neighborhood = input("Enter the neighborhood: ")

        path = controller.requirement6(analyzer, origin, neighborhood)

        print("\n===================================")
        print(f"Total distance: {path[1]}")
        print("===================================\n")

        print("===================================")
        print(f"Total stations: {path[2]}")
        print("===================================\n")

        print("===================================")
        print(f"Path:")
        print("===================================\n")

        for i in lt.iterator(path[0]):
            print(i["vertexA"] + " -> " + i["vertexB"] + " | distNext: " + str(i["weight"]))

        print("\n")

    elif int(inputs[0]) == 7:
        origin = input("Enter the origin station: ")

        cycles = controller.requirement7(analyzer, origin)

        for i in lt.iterator(cycles):
            print(i["vertexA"] + " -> " + i["vertexB"])

        print("\n")

    else:
        sys.exit(0)
sys.exit(0)
