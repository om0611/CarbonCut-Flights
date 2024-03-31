"""
This Python file contains the data classes that will be used within our project.
"""
from __future__ import annotations


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
    neighbours: dict[_Vertex, dict[tuple[str, tuple], list[int]]]

    def __init__(self, airport_code: str, country_name: str,
                 neighbours: dict[_Vertex, dict[tuple[str, tuple], list[int]]]) -> None:
        """
        Initialize a vertex with the given airport_code and country_name.
        """
        self.airport_code = airport_code
        self.country_name = country_name
        self.neighbours = neighbours

    def average_emissions(self, dest_airport_code: str) -> float:
        """
        Return the average CO2 emissions for a flight between self and the given destination airport.
        """
        for neighbour in self.neighbours:
            if neighbour.airport_code == dest_airport_code:
                flight_packages = self.neighbours[neighbour]
                sum_emissions = 0
                for flight_info in flight_packages.values():
                    sum_emissions += flight_info[2]

                return round(sum_emissions / len(flight_packages), 2)


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

    def get_average_emissions(self, home_airport_code: str, dest_airport_code: str) -> float:
        """
        Return the average CO2 emissions for a flight between the two given airports.
        """
        v1 = self._vertices[home_airport_code]
        return v1.average_emissions(dest_airport_code)