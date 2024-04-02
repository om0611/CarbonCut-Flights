"""
This Python file contains all the helper functions that we will use in our project.
"""
import data_classes
import csv
import visualization


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
    """
    Return the most optimal flight packages between home_airport and dest_airport.
    """
    home_vertex = graph.get_vertex(home_airport)
    destination_vertex = graph.get_vertex(dest_airport)

    if home_vertex not in graph.all_verticies() or destination_vertex not in graph.all_verticies():
        raise ValueError

    if destination_vertex not in home_vertex.neighbours:
        return []

    flights = home_vertex.neighbours[destination_vertex]
    flight_scores = calculate_flight_scores(flights, weights)

    sorted_flights = sorted(flight_scores.items(), key=lambda item: item[1])

    all_flights = [(flight[0], flights[flight[0]][0], flights[flight[0]][1], round(flight[1], 5))
                   for flight in sorted_flights]
    if len(all_flights) > 5:
        return all_flights[:4]
    else:
        return all_flights


def all_countries_and_airports(flight_path_file: str) -> tuple[set[str], set[str]]:
    """
    Returns a tuple of all countries and all airports in the flight dataset.
    """
    countries, airports = set(), set()
    with open(flight_path_file, mode='r') as flight_paths:
        reader = csv.reader(flight_paths)
        next(flight_paths)
        for row in reader:
            airports.add(row[0])
            airports.add(row[2])
            countries.add(row[1].lower())
            countries.add(row[3].lower())

    return countries, airports


def carbon_statistics(offset: int) -> set[str]:
    """
    Return a set of statistics based on how much carbon emissions the user saved by choosing
    a flight package suggested by our program.
    """
    all_stats = set()
    avg_c02_percentage_person = round((offset / 4000000) * 100, 2)
    car_km = round(offset / 192, 2)
    plastic_bottles = round(offset / 83, 2)
    light_bulb = round(offset / 42)
    coffee_cups = round(offset / 50)
    all_stats.add(
        f"Over {coffee_cups}! Thats how many coffee cups you saved by flying with VerdeVoyage. Our planet thanks you! ")
    all_stats.add(
        f"{light_bulb}. That is how many hours of having a light bulb turned on you have saved by flying with "
        f"VerdeVoyage.")
    all_stats.add(
        f"{plastic_bottles}. That is how many plastic bottles you saved by choosing the most greenflight "
        f"to your destination! Thank you for flying with VerdeVoyage.")
    all_stats.add(
        f"Choosing this flight over the others, you have saved the equivalent of not driving for {car_km} kilometers. "
        f"Thank you for making a greener planet!")
    all_stats.add(
        f"By flying with VerdeVoyage, you have saved {avg_c02_percentage_person}% of an individuals "
        f"annual carbon usage.")
    return all_stats


def create_graph(home_airport: str = None, dest_airport: str = None,
                 dest_country: str = None) -> data_classes.Graph:
    """
    Return a graph containing home_airport and dest_airport as vertices, if given, and the flights between the airports
    as the edges connecting the two vertices.

    If home_airport and/or dest_airport is not given, return the appropriate graph.

    Preconditions:
        - dest_airport is None or home_airport is not None
    """
    graph = data_classes.Graph()
    with open('flight_data.csv') as file:
        reader = csv.reader(file)
        next(reader, None)              # skip the header

        for row in reader:

            # If any of the values are missing, then move to the next row
            if row[4] == '' or row[12] == '' or row[14] == '':
                continue

            if home_airport is None:
                create_graph_helper(graph, row)

            elif home_airport is not None and dest_airport is not None:
                if row[0] == home_airport and row[2] == dest_airport:
                    create_graph_helper(graph, row)

            elif home_airport is not None and dest_country is not None:
                if row[0] == home_airport and row[3].lower() == dest_country:
                    create_graph_helper(graph, row)

            else:   # home_airport is not None and both dest_airport and dest_country are None
                if row[0] == home_airport:
                    create_graph_helper(graph, row)

    return graph


def create_graph_helper(graph: data_classes.Graph, row: list[str]) -> None:
    """
    Store the flight information in the given row in the graph.
    """
    graph.add_vertex(row[0], row[1])
    graph.add_vertex(row[2], row[3])

    aircrafts = tuple(row[4].split('|'))
    airline = row[6].split('| ')[0].strip('[]')
    stops = int(row[11])
    price = float(row[12])
    emissions = int(row[14])

    flight_package = (airline, aircrafts)
    flight_info = [price, stops, emissions]
    graph.add_edge(row[0], row[2], (flight_package, flight_info))


def run_voyage() -> None:
    """
    Runs the entire program.
    """
    print('Welcome to Verde Voyage! This is your ultimate eco-conscious dream vacation planner!')
    countries, airports = all_countries_and_airports('flight_data.csv')

    home_airport = input('What is your home airport? (Enter airport code) ').strip().upper()
    while home_airport not in airports:
        print('We are sorry! We do not have enough information on this airport. We are constantly trying'
              'to expand our reach. Please try a different airport.')

        home_airport = input('What is your home airport? (Enter airport code) ').strip().upper()

    # Display the graph from home_airport to all connecting airports.
    graph = create_graph(home_airport=home_airport)
    print("These are all the connecting airports from your home airport.")
    visualization.visualize_graph(graph)

    questionare = input('Would you like to answer a few questions to get suggestions for travel destinations '
                        'that are perfect for you? (Y/N) ').strip().upper()
    while questionare == 'Y':
        matches = data_classes.run_country_matchmaker('country_traits.csv')
        questionare = input('Would you like to take the questionare again? (Y/N) ').strip().upper()

    dest_country = input('Which country would you like to fly to? ').strip().lower()
    while dest_country not in countries:
        print('We are sorry! We do not have enough information on this country. We are constantly trying'
              'to expand our reach. Please try a different country.')

        dest_country = input('Which country would you like to fly to? ').strip().lower()

    # Display the graph from home_airport to all airports in dest_country.
    graph = create_graph(home_airport=home_airport, dest_country=dest_country)
    print("These are all the connecting airports in your chosen destination country from "
          "your home airport.")
    visualization.visualize_graph(graph)

    dest_airport = input('Which airport would you like to fly to? (Enter airport code) ').strip().upper()
    while dest_airport not in airports:
        print('We are sorry! We do not have enough information on this airport. We are constantly trying'
              'to expand our reach. Please try a different airport.')

        dest_airport = input('Which airport would you like to fly to? (Enter airport code) ').strip().upper()

    # Display the graph from home_airport to dest_airport with at least 10 flights highlighted.
    graph = create_graph(home_airport=home_airport, dest_airport=dest_airport)
