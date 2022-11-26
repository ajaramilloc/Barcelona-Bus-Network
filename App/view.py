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

def loadData() -> None:
    """
    Load all the information from the archives, transer to the controller
    """
    controller.loadData(analyzer)

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        analyzer = newController()
        print("Loading the information from the archives ....")
        loadData()

    elif int(inputs[0]) == 1:
        origin = input("Enter the origin station: ")
        destiny = input("Enter the destiny station: ")

        controller.requirement1(analyzer, origin, destiny)

    elif int(inputs[0]) == 2:
        origin = input("Enter the origin station: ")
        destiny = input("Enter the destiny station: ")

        controller.requirement2(analyzer, origin, destiny)

    else:
        sys.exit(0)
sys.exit(0)
