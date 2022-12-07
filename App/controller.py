import config as cf
import model
import csv
import sys

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
csv.field_size_limit(2147483647)

def newController() -> dict:
    """
    Initialize the dictionary that contains all the information, transfer to the model
    """
    analyzer: dict = model.newAnalyzer()
    return analyzer

def loadData(analyzer: dict) -> tuple:
    """
    Load all the information from the archives, transer to the model
    """
    stops_file = cf.data_dir + 'Barcelona/bus_stops_bcn-utf8-small.csv'
    edges_file = cf.data_dir + 'Barcelona/bus_edges_bcn-utf8-small.csv'
    stop_file = csv.DictReader(open(stops_file, encoding='utf-8'))
    edge_file = csv.DictReader(open(edges_file, encoding='utf-8'))

    exclusive_stops = 0
    share_stops = 0

    for stop in stop_file:
        if stop["Transbordo"] == "S":
            share_stops += 1
        else:
            exclusive_stops += 1

        model.addStop(analyzer, stop)

    for edge in edge_file:
        model.addEdge(analyzer, edge)

    model.kosaraju(analyzer)

    return share_stops, exclusive_stops

def requirement1(analyzer: dict, origin: str, destiny: str):
    return model.requirement1(analyzer, origin, destiny)

def requirement2(analyzer: dict, origin: str, destiny: str):
    return model.requirement2(analyzer, origin, destiny)

def requirement3(analyzer: dict):
    return model.requirement3(analyzer)

def requirement5(analyzer, origin):
    return model.requirement5(analyzer, origin)

def requirement6(analyzer: dict, origin: str, neighborhood: str):
    return model.requirement6(analyzer, origin, neighborhood)

def requirement7(analyzer: dict, origin: str):
    return model.requirement7(analyzer, origin)