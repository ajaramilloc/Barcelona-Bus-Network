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

        controller.requirement1(analyzer, origin, destiny)

    elif int(inputs[0]) == 2:
        origin = input("Enter the origin station: ")
        destiny = input("Enter the destiny station: ")

        controller.requirement2(analyzer, origin, destiny)

    elif int(inputs[0]) == 3:
        controller.requirement3(analyzer)

    elif int(inputs[0]) == 6:
        origin = input("Enter the origin station: ")
        neighborhood = input("Enter the neighborhood: ")

        controller.requirement6(analyzer, origin, neighborhood)

    elif int(inputs[0]) == 5:
        origin = input("Enter the origin station: ")

        controller.requirement5(analyzer, origin)

    elif int(inputs[0]) == 7:
        origin = input("Enter the origin station: ")

        controller.requirement7(analyzer, origin)

    else:
        sys.exit(0)
sys.exit(0)
