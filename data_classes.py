"""
This Python file contains the data classes that we will use in our project.
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
    neighbours: dict[_Vertex, dict[tuple[str, tuple], list[int | float]]]
    cordinates: tuple[float, float]  # latitude and longitude respectively

    def __init__(self, airport_code: str, country_name: str,
                 neighbours: dict[_Vertex, dict[tuple[str, tuple], list[int | float]]]) -> None:
        """
        Initialize a vertex with the given airport_code and country_name.
        """
        self.airport_code = airport_code
        self.country_name = country_name
        self.neighbours = neighbours
        self.cordinates = (0, 0)

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
    def neighbors(self) -> set[str]:
        """
        Return all the airport codes connected to this airport in a set of strings.
        """
        all_neighbors = set()
        for airport in self.neighbours:
            all_neighbors.add(airport.airport_code)

        return all_neighbors


class Graph:
    """
    A graph. In our project, the graph represents a map of various airports around the world.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps airport_code to _Vertex object.
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, airport_code: str, country_name: str) -> None:
        """Add a vertex with the given airport_code and country_name to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if airport_code not in self._vertices:
            self._vertices[airport_code] = _Vertex(airport_code, country_name, {})

    def add_edge(self, airport1: str, airport2: str,
                 conn_flight: tuple[tuple[str, tuple], list[int | float]]) -> None:
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
    A recursive tree data structure.
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
