import config as cf
from haversine import haversine, Unit
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import bfs
assert cf

def newAnalyzer() -> dict:
    """
    Initialize the dictionary that contains all the information
    """
    analyzer: dict = {}

    analyzer["connections_graph"] = gr.newGraph("ADJ_LIST", False, size=4649)
    analyzer["connections_digraph"] = gr.newGraph("ADJ_LIST", True, size=4649)
    analyzer["stops_info"] = mp.newMap(4649, maptype="PROBING", loadfactor=0.5)

    return analyzer

def addStop(analyzer: dict, stop: dict) -> None:
    """
    Add a vertex(stop) into the graphs
    """
    graph: graph = analyzer["connections_graph"]
    digraph: graph = analyzer["connections_digraph"]

    station_code: str = stop["Code"]
    station_stop: str = stop["Bus_Stop"]
    station_stop: str = station_stop.split("-")[1]
    station_stop: str = station_stop.strip()

    format_station: str = formatStation(station_code, station_stop)

    if stop["Transbordo"] == "S":
        connection_station: str = "T" + "-" + stop["Code"]
        if gr.containsVertex(graph, connection_station):
            gr.insertVertex(graph, format_station)
        else:
            gr.insertVertex(graph, connection_station)
            gr.insertVertex(graph, format_station)

        if gr.containsVertex(digraph, connection_station):
            gr.insertVertex(digraph, format_station)
        else:
            gr.insertVertex(digraph, connection_station)
            gr.insertVertex(digraph, format_station)
    else:
       gr.insertVertex(graph, format_station)
       gr.insertVertex(digraph, format_station)

    addStopInfo(analyzer, stop, format_station)


def formatStation(station_code: str, station_stop: str) -> str:
    """
    Format the station name, to "Code-BusId"
    """
    format_station: str = station_code + "-" + station_stop

    return format_station

def addStopInfo(analyzer: dict, stop: dict, format_station: str) -> None:
    """
    Adds the coordiantes of each station into a hash map
    """
    stops_map: map = analyzer["stops_info"]
    mp.put(stops_map, format_station, stop)

def addEdgeGraph(analyzer: dict, edge: dict) -> None:
    """
    Add the edge on the graph, between vertex A and vertex B
    """
    graph: graph = analyzer["connections_graph"]

    origin_station: str = formatStation(edge["Code"], (edge["Bus_Stop"].split("-")[1].strip()))
    destiny_station: str = formatStation(edge["Code_Destiny"], (edge["Bus_Stop"].split("-")[1].strip()))

    if gr.containsVertex(graph, origin_station):
        if gr.containsVertex(graph, destiny_station):
            vertexA: dict = me.getValue(mp.get(analyzer["stops_info"], origin_station))
            vertexB: dict = me.getValue(mp.get(analyzer["stops_info"], destiny_station))

            coordinateA: tuple = (float(vertexA["Latitude"]), float(vertexA["Longitude"]))
            coordinateB: tuple = (float(vertexB["Latitude"]), float(vertexB["Longitude"]))

            distance: float = haversine(coordinateA, coordinateB, unit='km')

            gr.addEdge(graph, origin_station, destiny_station, distance)
            gr.addEdge(graph, destiny_station, origin_station, distance)

            if vertexA["Transbordo"] == "S":
                connection_stationA: str = "T" + "-" + vertexA["Code"]
                gr.addEdge(graph, origin_station, connection_stationA, 0)
                gr.addEdge(graph, connection_stationA, origin_station, 0)
            
            if vertexB["Transbordo"] == "S":
                connection_stationB: str = "T" + "-" + vertexB["Code"]
                gr.addEdge(graph, destiny_station, connection_stationB, 0)
                gr.addEdge(graph, connection_stationB, destiny_station, 0)

def addEdgeDigraph(analyzer: dict, edge: dict) -> None:
    """
    Add the edge on the digraph, between vertex A and vertex B
    """
    graph: graph = analyzer["connections_digraph"]

    origin_station: str = formatStation(edge["Code"], (edge["Bus_Stop"].split("-")[1].strip()))
    destiny_station: str = formatStation(edge["Code_Destiny"], (edge["Bus_Stop"].split("-")[1].strip()))

    if gr.containsVertex(graph, origin_station):
        if gr.containsVertex(graph, destiny_station):
            vertexA: dict = me.getValue(mp.get(analyzer["stops_info"], origin_station))
            vertexB: dict = me.getValue(mp.get(analyzer["stops_info"], destiny_station))

            coordinateA: tuple = (float(vertexA["Latitude"]), float(vertexA["Longitude"]))
            coordinateB: tuple = (float(vertexB["Latitude"]), float(vertexB["Longitude"]))

            distance: float = haversine(coordinateA, coordinateB, unit='km')

            gr.addEdge(graph, origin_station, destiny_station, distance)

            if vertexA["Transbordo"] == "S":
                connection_stationA: str = "T" + "-" + vertexA["Code"]
                gr.addEdge(graph, origin_station, connection_stationA, 0)
                gr.addEdge(graph, connection_stationA, origin_station, 0)
            
            if vertexB["Transbordo"] == "S":
                connection_stationB: str = "T" + "-" + vertexB["Code"]
                gr.addEdge(graph, destiny_station, connection_stationB, 0)
                gr.addEdge(graph, connection_stationB, destiny_station, 0)

def kosaraju(analyzer: dict) -> None:
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

def requirement1(analyzer: dict, origin: str, destiny: str) -> lt:
    dijikstra: dijikstra = djk.Dijkstra(analyzer["connections_digraph"], origin)
    path = djk.pathTo(dijikstra, destiny)
    print(path)

def requirement2(analyzer: dict, origin: str, destiny: str) -> lt:
    paths = bfs.BreadhtFisrtSearch(analyzer["connections_digraph"], origin)

    if bfs.hasPathTo(paths, destiny):
        path = bfs.pathTo(paths, destiny)
        print(path)

def requirement7(analyzer: dict, origin: str) -> lt:
    components: map = analyzer["components"]
    components_list: lt = mp.keySet(components)

    for component in lt.iterator(components_list):
        component_info: lt = me.getValue(mp.get(components, component))

        if lt.size(component_info) > 1:
            if lt.isPresent(component_info, origin):
                print(component_info)
    