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
    gr.addEdge(graph, destiny_format, origin_format, distance)

def addTransfer(analyzer, stop, format_station):
    transfer = "T" + "-" + stop["Code"]

    gr.addEdge(analyzer["connections_digraph"], format_station, transfer, 0.0)
    gr.addEdge(analyzer["connections_digraph"], transfer, format_station, 0.0)

    gr.addEdge(analyzer["connections_graph"], format_station, transfer, 0.0)
    gr.addEdge(analyzer["connections_graph"], transfer, format_station, 0.0)

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

    if dfs.hasPathTo(paths, destiny):
        path = dfs.pathTo(paths, destiny)
        print(path)

def requirement2(analyzer: dict, origin: str, destiny: str) -> lt:
    paths = bfs.BreadhtFisrtSearch(analyzer["connections_digraph"], origin)

    if bfs.hasPathTo(paths, destiny):
        path = bfs.pathTo(paths, destiny)
        print(path)

def requirement3(analyzer: dict) -> lt:
    components: map = analyzer["components"]
    components_list: lt = mp.keySet(components)
    format_components: lt = lt.newList("ARRAY_LIST")

    for component in lt.iterator(components_list):
        component_info: lt = me.getValue(mp.get(components, component))
        component_dict: dict = {"size": lt.size(component_info), "component": component_info}
        lt.addLast(format_components, component_dict)

    sorted_list: lt = sortList(format_components, cmp_function_components)

    for i in lt.iterator(sorted_list):
        print(i["size"])

def requirement5(analyzer, origin):
    graph = analyzer["connections_graph"]
    mst = prim.PrimMST(graph, origin)
    prim.weightMST(graph, mst)
    print(mst["mst"])
    """
    for transfer in lt.iterator(mst["mst"]):
        print(transfer)
    """

def requirement6(analyzer: dict, origin: str, neighborhood: str) -> lt:
    graph: gr = analyzer["connections_digraph"]
    neighborhood_stops = me.getValue(mp.get(analyzer["neighborhoods"], neighborhood))
    dijikstra: djk = djk.Dijkstra(graph, origin)
    stops = lt.newList("ARRAY_LIST")

    for stop in lt.iterator(neighborhood_stops):
        distance: float = djk.distTo(dijikstra, stop)
        stop_info: dict = {"size": distance, "component": stop}
        lt.addLast(stops, stop_info)

    sorted_list: lt = sortList(stops, cmp_function_components)
    
    path = djk.pathTo(dijikstra, lt.getElement(sorted_list, lt.size(sorted_list) - 1)["component"])
    print(path)

def requirement7(analyzer: dict, origin: str) -> lt:
    """
    graph_cycles = cycles.DirectedCycle(analyzer["connections_digraph"])
    cycles_list = cycles.dfs(analyzer["connections_digraph"], graph_cycles, origin)["cycle"]
    print(cycles_list)
    """

    search = dfo.DepthFirstOrder(analyzer["connections_digraph"])
    reverse = search["reversepost"]
    while not stack.isEmpty(reverse):
        n = stack.pop(reverse)
        print(n)

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


def sortList(list: lt, cmp_function: bool) -> None:
    """
    Sort the list based con the cmp_function
    """
    return merge.sort(list, cmp_function)
    