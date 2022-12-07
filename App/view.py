import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
assert cf

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- ")

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
        share_stops, exclusive_stops = loadData()
        print(share_stops)
        print(exclusive_stops)
        print(lt.size(gr.vertices(analyzer["connections_digraph"])))
        print(lt.size(gr.edges(analyzer["connections_digraph"])))
        print("\n")
        print(lt.size(gr.vertices(analyzer["connections_graph"])))
        print(lt.size(gr.edges(analyzer["connections_graph"])))

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

    elif int(inputs[0]) == 5:
        origin = input("Enter the origin station: ")

        controller.requirement5(analyzer, origin)

    elif int(inputs[0]) == 7:
        origin = input("Enter the origin station: ")

        controller.requirement7(analyzer, origin)

    else:
        sys.exit(0)
sys.exit(0)
