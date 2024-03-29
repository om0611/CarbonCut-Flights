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
        - neighbours: A mapping of connecting airports to the available flights that connect them.
    """
    airport_code: str
    country_name: str
    neighbours: dict[_Vertex, dict[str, list[str, int, int, int]]]

    def __init__(self, airport_code: str, country_name: str) -> None:
        """
        Initialize a vertex with the given airport_code and country_name.
        """
        self.airport_code = airport_code
        self.country_name = country_name
        self.neighours = {}


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
        self._vertices[airport_code] = _Vertex(airport_code, country_name)
