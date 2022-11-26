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

def loadData(analyzer: dict) -> None:
    """
    Load all the information from the archives, transer to the model
    """
    stops_file = cf.data_dir + 'Barcelona/bus_stops_bcn-utf8-large.csv'
    edges_file = cf.data_dir + 'Barcelona/bus_edges_bcn-utf8-large.csv'
    stops_file = csv.DictReader(open(stops_file, encoding='utf-8'))
    edges_file = csv.DictReader(open(edges_file, encoding='utf-8'))

    for stop in stops_file:
        model.addStop(analyzer, stop)

    for edge in edges_file:
        model.addEdgeDigraph(analyzer, edge)

    model.kosaraju(analyzer)

def requirement1(analyzer: dict, origin: str, destiny: str):
    model.requirement1(analyzer, origin, destiny)

def requirement2(analyzer: dict, origin: str, destiny: str):
    model.requirement2(analyzer, origin, destiny)

def requirement7(analyzer: dict, origin: str):
    model.requirement7(analyzer, origin)