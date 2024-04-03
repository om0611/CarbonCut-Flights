"""Verde Voyage: ALL classes used for a green flight path result

Module Description
==================
This Python module integrates a graph-based representation of the global airport network with a decision-tree-based
country matchmaker system. The `Graph` class models airports as vertices and flights as edges, including functionalities
to manage airport details, flight connections, and calculate maximum CO2 emissions for flights. The `Tree` class
constructs a decision tree for the country matchmaker system. This system utilizes user responses to travel preference
questions to recommend countries,

Copyright and Usage Information
===============================
This file is provided exclusively for the use and benefit of customers of VerdeVoyage. Any form of
distribution, reproduction, or modification of this code outside of its intended use within the VerdeVoyage
platform is strictly prohibited. All rights reserved.

This file is Copyright (c) 2024 Verde Voyage

"""
from __future__ import annotations
import networkx as nx
import csv
from typing import Any, Optional


class _Vertex:
    """
    A vertex in a graph. In our project, each vertex represents a unique airport in the world.

    Instance Attributes:
        - airport_code: A code that uniquely identifies this airport.
        - country_name: The country where this airport is located.
        - neighbours: A mapping of airports that are connected to self by available flights.
            The flights are stored as a mapping between different flight packages and their
            ticket price, number of stops, and CO2 emissions.
    """
    airport_code: str
    country_name: str
    neighbours: dict[_Vertex, dict[tuple[str, tuple], list[float, int, int]]]
    coordinates: tuple[float, float]  # latitude and longitude respectively

    def __init__(self, airport_code: str, country_name: str,
                 neighbours: dict[_Vertex, dict[tuple[str, tuple], list[float, int, int]]],
                 coordinates: tuple[float, float]) -> None:
        """
        Initialize a vertex with the given airport_code and country_name.
        """
        self.airport_code = airport_code
        self.country_name = country_name
        self.neighbours = neighbours
        self.coordinates = coordinates

    def max_emissions(self, dest_airport_code: str) -> int:
        """
        Return the max CO2 emissions for a flight between self and the given destination airport.
        """
        for neighbour in self.neighbours:
            if neighbour.airport_code == dest_airport_code:
                flight_packages = self.neighbours[neighbour]
                max_emissions = 0
                for flight_info in flight_packages.values():
                    if flight_info[2] > max_emissions:
                        max_emissions = flight_info[2]

                return max_emissions

    def get_neighbors(self) -> set[str]:
        """
        Return all the airport codes connected to this airport in a set of strings.
        """
        all_neighbors = set()
        for airport in self.neighbours:
            all_neighbors.add(airport.airport_code)

        return all_neighbors


class Graph:
    """
    Represents a graph data structure, specifically modeling a network of airports and their connections.
    Airports are vertices with attributes like code and country, and edges represent flights, including
    details such as ticket prices, number of stops, and CO2 emissions. Supports operations to add vertices
    (airports), add edges (flight connections), calculate maximum CO2 emissions between airports, and convert
    the graph to a NetworkX graph for visualization.

    Private Instance Attributes:
        - _vertices: A collection of the vertices contained in this graph and maps airport_code to _Vertex object.
    """
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, airport_code: str, country_name: str, coords: tuple[float, float]) -> None:
        """Add a vertex with the given airport_code and country_name to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if airport_code not in self._vertices:
            self._vertices[airport_code] = _Vertex(airport_code, country_name, {}, coords)

    def add_edge(self, airport1: str, airport2: str,
                 conn_flight: tuple[tuple[str, tuple[str]], list[float, int, int]]) -> None:
        """
        Add an edge between the two vertices with the given ariport codes in this graph.

        Raise a ValueError if ariport1 or airport2 do not appear as vertices in this graph.

        Preconditions:
            - airport1 != airport2
        """
        if airport1 in self._vertices and airport2 in self._vertices:
            v1 = self._vertices[airport1]
            v2 = self._vertices[airport2]

            flight_package, flight_info = conn_flight[0], conn_flight[1]

            if v2 not in v1.neighbours:
                v1.neighbours[v2] = {}
                v2.neighbours[v1] = {}

            v1.neighbours[v2].update({flight_package: flight_info})
            v2.neighbours[v1].update({flight_package: flight_info})

    def get_max_emissions(self, home_airport_code: str, dest_airport_code: str) -> float:
        """
        Return the max CO2 emissions for a flight between the two given airports.
        """
        v1 = self._vertices[home_airport_code]
        return v1.max_emissions(dest_airport_code)

    def to_networkx(self, max_vertices: int = 100) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)
        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.airport_code)
            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.airport_code)
                if u.airport_code in graph_nx.nodes:
                    graph_nx.add_edge(v.airport_code, u.airport_code)
            if graph_nx.number_of_nodes() >= max_vertices:
                break
        return graph_nx

    def get_vertex(self, airport: str) -> _Vertex:
        """
        Return the vertex object associated with the given airport code.
        """
        if airport not in self._vertices:
            raise ValueError
        else:
            return self._vertices[airport]

    def all_verticies(self) -> set[_Vertex]:
        """
        Return a set of all the vertex objects in this graph.
        """
        all_vert = set()
        for vertex in self._vertices.values():
            all_vert.add(vertex)
        return all_vert

    def all_airport_codes(self) -> set[str]:
        """
        Return a set of all the airport codes in this graph.

        """
        airport_codes = set()
        for vertex in self._vertices.values():
            airport_codes.add(vertex.airport_code)
        return airport_codes


class Tree:
    """
    Represents a recursive tree data structure.
    Each tree node can contain any type of data and have multiple subtrees, allowing for a recursive structure.

    Instance Attributes:
        - _root: The data stored in the root node of the tree. If the tree is empty, _root is None.
        - _subtrees: A list of Tree instances that are the subtrees of the current tree node.
    """

    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.
        """
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def traverse(self, path: list[bool]) -> list[Any]:
        """
        This function traverses a decision tree and returna all the leafs at the end of a given path.
        """
        if self.is_empty():
            return []

        if not path:
            leaves = []
            for subtree in self._subtrees:
                leaves.extend([subtree._root])
            return leaves

        direction = path[0]
        next_path = path[1:]

        for subtree in self._subtrees:
            if subtree._root == direction:
                return subtree.traverse(next_path)

        return []

    def create_tree(self, items: list) -> Tree:
        """
        Create a tree from the provided list, ensuring that each subsequent item is a child of the previous.

        Preconditions:
            - self.is_empty()
        """
        root = items[0]
        subtrees = []
        if len(items) > 1:
            subtree = self.create_tree(items[1:])
            subtrees.append(subtree)

        return Tree(root, subtrees)

    def insert_sequence(self, items: list) -> None:
        """
        Insert the given items into this tree.
        """
        if not items:
            return
        elif not self._subtrees:
            empty_tree = Tree(None, [])
            self._subtrees.append(empty_tree.create_tree(items))
            return
        else:
            root = items[0]
            rest_items = items[1:]
            for subtree in self._subtrees:
                if subtree._root == root:
                    subtree.insert_sequence(rest_items)
                    return

            empty_tree = Tree(None, [])
            self._subtrees.append(empty_tree.create_tree(items))
            return


def build_decision_tree(file: str) -> Tree:
    """
    Build a decision tree storing the country data from the given file.
    """
    tree = Tree('', [])

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            values = [False if x == 'No' else True for x in row[1:]]
            tree.insert_sequence(values + [row[0]])

    return tree


def get_user_input(questions: list[str]) -> list[bool]:
    """Return the user's answers to a list of Yes/No questions."""
    answers_so_far = []

    for question in questions:
        print(question)
        s = input('Y/N: ').strip().upper()
        answers_so_far.append(s == 'Y')  # Any other input is interpreted as False

    return answers_so_far


TRAVEL_QUESTIONS = [
    'Do you prefer a vacation in a climate that is primarily warm and sunny, rather than cold?',
    'Would you like to be near beaches, lakes, rivers?',
    'Are you looking for destinations where you can engage in outdoor activities, such as hiking, '
    'skiing, or wildlife watching?',
    'Do you prefer a destination that offers a vibrant nightlife?',
]


def run_country_matchmaker(file: str) -> None:
    """Run a country matching program based on the given file.
    """
    decision_tree = build_decision_tree(file)
    char = get_user_input(TRAVEL_QUESTIONS)
    matches = decision_tree.traverse(char)
    if not matches:
        print("There are no countries with this match.")
    else:
        print(f"The following country(s) match your inputs: {matches}")


if __name__ == '__main__':
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 170,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'random', 'data_classes', 'flight_visualization'],
        'allowed-io': ['run_voyage', 'get_airport_coordinates', 'countries_and_airports', 'optimal_routes',
                       'create_graph'],
        'max-nested-blocks': 4,
        'max-locals': 25,
        'max-statements': 80
    })
