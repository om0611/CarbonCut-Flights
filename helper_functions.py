"""
This Python file contains all the helper functions that we will use in our project.
"""
import data_classes
import csv


def calculate_flight_scores(flights: dict[tuple[str, tuple], list[int]],
                            weights: tuple[float, float, float] = (0.1, 0.1, 0.8)) -> dict[tuple[str, tuple], float]:
    """
    Calculate a score for each flight in flights based on the given weights for price, stops, and
    carbon emissions.

    Return a mapping between each flight and its score.
    """
    weight_price, weight_stops, weight_emissions = weights
    max_price = max(flights[flight][0] for flight in flights)
    max_stops = max(flights[flight][1] for flight in flights)
    max_emissions = max(flights[flight][2] for flight in flights)

    flight_scores = {}

    for flight in flights:
        flight_info = flights[flight]
        price, stops, emissions = flight_info[0], flight_info[1], flight_info[2]

        # Normalize the values (puts the values between 0 and 1)
        norm_price = price / max_price
        norm_stops = stops / max_stops
        norm_emissions = emissions / max_emissions

        flight_scores[flight] = (norm_price * weight_price + norm_stops * weight_stops +
                                 norm_emissions * weight_emissions)

    return flight_scores


def optimal_routes(graph: data_classes.Graph, home_airport: str, dest_airport: str,
                   weights: tuple[float, float, float] = (0.1, 0.1, 0.8)) -> list[tuple]:
    home_vertex = graph.get_vertex(home_airport)
    destination_vertex = graph.get_vertex(dest_airport)

    if home_vertex not in graph.all_verticies() or destination_vertex not in graph.all_verticies():
        raise ValueError

    if destination_vertex not in home_vertex.neighbours:
        return []

    flights = home_vertex.neighbours[destination_vertex]
    flight_scores = calculate_flight_scores(flights, weights)

    sorted_flights = sorted(flight_scores.items(), key=lambda item: item[1])

    all_flights = [(flight[0], flights[flight[0]][0], flights[flight[0]][1], round(flight[1], 5)) for flight in
                   sorted_flights]
    if len(all_flights) > 5:
        return all_flights[:4]
    else:
        return all_flights


def all_countries(flight_path_file: str) -> set:
    """
    Returns a set of all the countries that are in the flight dataset.
    """
    countries = set()
    with open(flight_path_file, mode='r') as flight_paths:
        reader = csv.reader(flight_paths)
        next(flight_paths)
        for row in reader:
            countries.add(row[1])
            countries.add(row[3])

    return countries
