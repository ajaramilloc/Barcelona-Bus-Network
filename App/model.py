import config as cf
from haversine import haversine, Unit
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import cycles
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dfo
assert cf
import sys

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
NEW ANALYZER
"""

def newAnalyzer() -> dict:
    """
    Initialize the dictionary that contains all the information
    """
    analyzer: dict = {}

    analyzer["connections_graph"] = gr.newGraph("ADJ_LIST", False, size=4649)
    analyzer["connections_digraph"] = gr.newGraph("ADJ_LIST", True, size=4649)
    analyzer["stops_info"] = mp.newMap(4649, maptype="PROBING", loadfactor=0.5)
    analyzer["neighborhoods"] = mp.newMap(100, maptype="PROBING", loadfactor=0.5)
    analyzer["longitude"] = lt.newList("ARRAY_LIST")
    analyzer["latitude"] = lt.newList("ARRAY_LIST")

    return analyzer

"""
LOADING FUNCTIONS
"""

def addStop(analyzer, stop):
    digraph = analyzer["connections_digraph"]
    graph = analyzer["connections_graph"]
    format_station = formatStation(stop["Code"], stop["Bus_Stop"])

    if stop["Transbordo"] == "S":
        connection_station = "T" + "-" + stop["Code"]

        connection_info = stop
        connection_info["Transport"] = "Transfer Bus"

        if not mp.contains(analyzer["stops_info"], connection_station):
            mp.put(analyzer["stops_info"], connection_station, connection_info)

        if gr.containsVertex(digraph, connection_station):
            gr.insertVertex(digraph, format_station)
        else:
            gr.insertVertex(digraph, format_station)
            gr.insertVertex(digraph, connection_station)

        if gr.containsVertex(graph, connection_station):
            gr.insertVertex(graph, format_station)
        else:
            gr.insertVertex(graph, format_station)
            gr.insertVertex(graph, connection_station)

    else:
        gr.insertVertex(digraph, format_station)
        gr.insertVertex(graph, format_station)


    mp.put(analyzer["stops_info"], format_station, stop)

    if stop["Transbordo"] == "S":
        addTransfer(analyzer, stop, format_station)

    addNeighborhood(analyzer, stop, format_station)
    lt.addLast(analyzer["latitude"], stop["Latitude"])
    lt.addLast(analyzer["longitude"], stop["Longitude"])

def area(analyzer):
    digraph = analyzer["connections_digraph"]
    first_5 = lt.subList(gr.vertices(digraph), 1, 5)
    last_5 = lt.subList(gr.vertices(digraph), lt.size(gr.vertices(digraph)) - 4, 5)

    first_5_list = lt.newList("ARRAY_LIST")
    last_5_list = lt.newList("ARRAY_LIST")
        
    for i in lt.iterator(first_5):
        station = me.getValue(mp.get(analyzer["stops_info"], i))
        station["ID"] = i
        station["indegree"] = gr.indegree(digraph, i)
        station["outdegree"] = gr.outdegree(digraph, i)
        lt.addLast(first_5_list, station)

    for j in lt.iterator(last_5):
        station = me.getValue(mp.get(analyzer["stops_info"], j))
        station["ID"] = j
        station["indegree"] = gr.indegree(digraph, j)
        station["outdegree"] = gr.outdegree(digraph, j)
        lt.addLast(last_5_list, station)

    graph = analyzer["connections_graph"]
    graph_5 = lt.subList(gr.vertices(graph), 1, 5)
    graph_last_5 = lt.subList(gr.vertices(graph), lt.size(gr.vertices(graph)) - 4, 5)

    graph_5_list = lt.newList("ARRAY_LIST")
    graph_last_5_list = lt.newList("ARRAY_LIST")
        
    for i in lt.iterator(graph_5):
        station = me.getValue(mp.get(analyzer["stops_info"], i))
        station["ID"] = i
        station["degree"] = gr.degree(graph, i)
        lt.addLast(graph_5_list, station)

    for j in lt.iterator(graph_last_5):
        station = me.getValue(mp.get(analyzer["stops_info"], j))
        station["ID"] = j
        station["degree"] = gr.degree(graph, j)
        lt.addLast(graph_last_5_list, station)

    latitudes = analyzer["latitude"]
    sorted_latitudes = sortList(latitudes, cmp_elements)
    max_latitude = lt.getElement(sorted_latitudes, 1)
    min_latitude = lt.getElement(sorted_latitudes, lt.size(sorted_latitudes) - 1)

    longitudes = analyzer["longitude"]
    sorted_longitudes = sortList(longitudes, cmp_elements)
    max_longitude = lt.getElement(sorted_longitudes, 1)
    min_longitude = lt.getElement(sorted_longitudes, lt.size(sorted_longitudes) - 1)

    return max_latitude, min_latitude, max_longitude, min_longitude, first_5_list, last_5_list, graph_5_list, graph_last_5_list

def formatStation(station_code, station_stop):
    format_stop = station_stop.split("-")[1]
    format_stop = format_stop.strip()
    format_station = station_code + "-" + format_stop

    return format_station

def addEdge(analyzer, edge):
    digraph = analyzer["connections_digraph"]
    graph = analyzer["connections_graph"]

    origin_format = formatStation(edge["Code"], edge["Bus_Stop"])
    destiny_format = formatStation(edge["Code_Destiny"], edge["Bus_Stop"])
    origin_station = me.getValue(mp.get(analyzer["stops_info"], origin_format))
    destiny_station = me.getValue(mp.get(analyzer["stops_info"], destiny_format))

    coordinateA = (float(origin_station["Latitude"]), float(origin_station["Longitude"]))
    coordinateB = (float(destiny_station["Latitude"]), float(destiny_station["Longitude"]))

    distance = haversine(coordinateA, coordinateB, unit="km")

    gr.addEdge(digraph, origin_format, destiny_format, distance)

    gr.addEdge(graph, origin_format, destiny_format, distance)

def addTransfer(analyzer, stop, format_station):
    transfer = "T" + "-" + stop["Code"]

    gr.addEdge(analyzer["connections_digraph"], format_station, transfer, 0.0)
    gr.addEdge(analyzer["connections_digraph"], transfer, format_station, 0.0)

    gr.addEdge(analyzer["connections_graph"], format_station, transfer, 0.0)


def kosaraju(analyzer: dict) -> None:
    """
    Find the connected components of the digraph
    """
    analyzer["components"]: dict = scc.KosarajuSCC(analyzer["connections_digraph"])

    connected_components: map = analyzer['components']['idscc'] 
    num_elements: int = scc.connectedComponents(analyzer['components'])
    vertices: lt = mp.keySet(connected_components)

    components: map = mp.newMap(num_elements, maptype="PROBING", loadfactor=0.5)

    for vertix in lt.iterator(vertices):
        num_component: int = me.getValue(mp.get(connected_components, vertix))

        if mp.contains(components,num_component):
            lt.addLast(me.getValue(mp.get(components,num_component)), vertix)

        else:
            vertices_list: lt = lt.newList()
            lt.addLast(vertices_list, vertix)
            mp.put(components,num_component, vertices_list)

    analyzer["components"]: map = components

def addNeighborhood(analyzer: dict, stop: dict, format_station: str) -> None:
    """
    Adds the stations in the map, key-> neighborhood - value-> stop
    """
    neighborhoods: map = analyzer["neighborhoods"]
    stop_neighborhood = stop["Neighborhood_Name"]

    if mp.contains(neighborhoods, stop_neighborhood):
        stops: lt = me.getValue(mp.get(neighborhoods, stop_neighborhood))
        lt.addLast(stops, format_station)
    else:
        stops: lt = lt.newList("ARRAY_LIST")
        lt.addLast(stops, format_station)
        mp.put(neighborhoods, stop_neighborhood, stops)

"""
REQUIREMENTS
"""

def requirement1(analyzer: dict, origin: str, destiny: str) -> lt:
    paths = dfs.DepthFirstSearch(analyzer["connections_digraph"], origin)
    path_list = lt.newList("ARRAY_LIST")
    transfers = 0

    if dfs.hasPathTo(paths, destiny):
        path = dfs.pathTo(paths, destiny)
    else:
        path = None

    if path == None:
        return 0
    else:
        while not stack.isEmpty(path):
            transfer = stack.pop(path)
            lt.addLast(path_list, transfer)

        dist_to = 0
        path_info = lt.newList("ARRAY_LIST")

        i = 1

        while i < lt.size(path_list):
            if i + 1 <= lt.size(path_list):
                edge = gr.getEdge(analyzer["connections_digraph"], lt.getElement(path_list, i), lt.getElement(path_list, i + 1))
                lt.addLast(path_info, edge)
                dist_to += edge["weight"]

                route1 = lt.getElement(path_list, i).split("-")[1]
                bus1 = lt.getElement(path_list, i).split("-")[0]
                route2 = lt.getElement(path_list, i+1).split("-")[1]
                bus2 = lt.getElement(path_list, i+1).split("-")[0]

                if bus1 != "T":
                    if bus2 != "T":
                        if route1 != route2:
                            transfers += 1
            
            i += 1
                
        return path_info, transfers, dist_to


def requirement2(analyzer: dict, origin: str, destiny: str) -> lt:
    paths = bfs.BreadhtFisrtSearch(analyzer["connections_digraph"], origin)
    path_list = lt.newList("ARRAY_LIST")
    transfers = 0

    if bfs.hasPathTo(paths, destiny):
        path = bfs.pathTo(paths, destiny)
    else:
        path = None

    if path == None:
        return 0
    else:
        while not stack.isEmpty(path):
            transfer = stack.pop(path)
            lt.addLast(path_list, transfer)

        dist_to = 0
        path_info = lt.newList("ARRAY_LIST")

        i = 1

        while i < lt.size(path_list):
            if i + 1 <= lt.size(path_list):
                edge = gr.getEdge(analyzer["connections_digraph"], lt.getElement(path_list, i), lt.getElement(path_list, i + 1))
                lt.addLast(path_info, edge)
                dist_to += edge["weight"]

                route1 = lt.getElement(path_list, i).split("-")[1]
                bus1 = lt.getElement(path_list, i).split("-")[0]
                route2 = lt.getElement(path_list, i+1).split("-")[1]
                bus2 = lt.getElement(path_list, i+1).split("-")[0]

                if bus1 != "T" or bus2 != "T":
                    if route1 != route2:
                        transfers += 1
            
            i += 1
                
        return path_info, transfers, dist_to

def requirement3(analyzer: dict) -> lt:
    components: map = analyzer["components"]
    components_list: lt = mp.keySet(components)
    format_components: lt = lt.newList("ARRAY_LIST")

    for component in lt.iterator(components_list):
        component_info: lt = me.getValue(mp.get(components, component))
        component_dict: dict = {"size": lt.size(component_info), "component": component_info}
        lt.addLast(format_components, component_dict)

    sorted_list: lt = sortList(format_components, cmp_function_components)
    top_5 = lt.subList(sorted_list, 1, 5)

    return top_5, lt.size(sorted_list)

def requirement5(analyzer, origin):
    graph = analyzer["connections_graph"]
    mst = prim.PrimMST(graph, origin)
    prim.weightMST(graph, mst)
    

    x = prim.edgesMST(analyzer["connections_graph"], mst)

    
    
    i = 1

    while i <=5:
        print(lt.getElement(mst["mst"], i))
        i += 1

def requirement6(analyzer: dict, origin: str, neighborhood: str) -> lt:
    graph: gr = analyzer["connections_digraph"]
    neighborhood_stops = me.getValue(mp.get(analyzer["neighborhoods"], neighborhood))
    dijikstra: djk = djk.Dijkstra(graph, origin)
    stops = lt.newList("ARRAY_LIST")
    path_list = lt.newList("ARRAY_LIST")

    for stop in lt.iterator(neighborhood_stops):
        distance: float = djk.distTo(dijikstra, stop)
        stop_info: dict = {"size": distance, "component": stop}
        lt.addLast(stops, stop_info)

    sorted_list: lt = sortList(stops, cmp_function_components)
    
    path = djk.pathTo(dijikstra, lt.getElement(sorted_list, lt.size(sorted_list) - 1)["component"])
    dist_to = djk.distTo(dijikstra, lt.getElement(sorted_list, lt.size(sorted_list) - 1)["component"])

    while not stack.isEmpty(path):
            transfer = stack.pop(path)
            lt.addLast(path_list, transfer)

    for i in lt.iterator(path_list):
        if i["vertexA"].split("-")[0] != "T":
            vertexA = me.getValue(mp.get(analyzer["stops_info"], i["vertexA"]))
            i["vertexA"] = i["vertexA"] + " | " + vertexA["Neighborhood_Name"]
        else:
            i["vertexA"] = i["vertexA"] + " | " + "Transfer"

        if i["vertexB"].split("-")[0] != "T":
            vertexB = me.getValue(mp.get(analyzer["stops_info"], i["vertexB"]))
            i["vertexB"] = i["vertexB"] + " | " +  vertexB["Neighborhood_Name"]
        else:
            i["vertexB"] = i["vertexB"] + " | " + "Transfer"

    return path_list, dist_to, lt.size(path_list) + 1

def requirement7(analyzer: dict, origin: str) -> lt:
    graph_cycles = cycles.DirectedCycle(analyzer["connections_digraph"])
    cycles_list = cycles.dfs(analyzer["connections_digraph"], graph_cycles, origin)["cycle"]
    print(cycles_list)

"""
SORTINGS
"""

def cmp_function_components(element1: dict, element2: dict) -> None:
    """
    Compare function for the connected components
    """
    if element1["size"] > element2["size"]:
        return True
    else:
        return False

def cmp_elements(element1: dict, element2: dict) -> None:
    """
    Compare function for the connected components
    """
    if element1 > element2:
        return True
    else:
        return False


def sortList(list: lt, cmp_function: bool) -> None:
    """
    Sort the list based con the cmp_function
    """
    return merge.sort(list, cmp_function)
    