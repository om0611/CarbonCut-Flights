"""
This Python file contains all the helper functions that we will use in our project.
"""
import data_classes
import csv
import visualization
import random
import test_viz


def calculate_flight_scores(flights: dict[tuple[str, tuple], list[int]],
                            weights: tuple[float, float, float] = (0.1, 0.1, 0.8)) -> dict[tuple[str, tuple], float]:
    """
    Calculate a score for each flight in flights based on the given weights for price, stops, and
    carbon emissions.

    Return a mapping between each flight and its score.

    The input weights has the following format: (price, stops, emissions)
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

    The input weights has the following format: (price, stops, emissions).
    The returned tuple has the following format: ((airline, (aircraft)), price, stops, emissions, flight_score).
    """
    home_vertex = graph.get_vertex(home_airport)
    destination_vertex = graph.get_vertex(dest_airport)

    if home_vertex not in graph.all_verticies() or destination_vertex not in graph.all_verticies():
        raise ValueError

    if destination_vertex not in home_vertex.neighbours:
        return []

    flights = home_vertex.neighbours[destination_vertex]
    flight_scores = calculate_flight_scores(flights, weights)
    print(flight_scores.items())
    sorted_flights = sorted(flight_scores.items(), key=lambda item: item[1])

    all_flights = [(flight[0], flights[flight[0]][0], flights[flight[0]][1], flights[flight[0]][2],
                    round(flight[1], 5)) for flight in sorted_flights]
    return all_flights[:5]


def countries_and_airports(flight_path_file: str) -> tuple[set[str], set[str], set[str], set[str]]:
    """
    Returns a tuple of home countries, dest countries, home airports, and dest airports in the flight dataset.
    """
    home_countries, home_airports = set(), set()
    dest_countries, dest_airports = set(), set()

    with open(flight_path_file, mode='r') as flight_paths:
        reader = csv.reader(flight_paths)
        next(flight_paths)
        for row in reader:
            home_airports.add(row[0])
            dest_airports.add(row[2])
            home_countries.add(row[1].lower())
            dest_countries.add(row[3].lower())

    return home_airports, home_countries, dest_airports, dest_countries


def get_airport_coordinates() -> dict[str, tuple[float, float]]:
    """
    Return a mapping between airport codes and their latitude and longitude coordinates.
    """
    airport_coords = {}
    with open('CSV Files/78_airport_info.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip the header
        for row in reader:
            airport_coords[row[0]] = (float(row[1]), float(row[2]))

    return airport_coords


def carbon_statistics(offset: int) -> set[str]:
    """
    Return a set of statistics based on how much carbon emissions the user saved by choosing
    a flight package suggested by our program.
    """
    all_stats = set()
    avg_c02_percentage_person = round((offset / 4000000) * 100, 2)
    car_km = round(offset / 192, 2)
    plastic_bottles = round(offset / 83)
    light_bulb = round(offset / 42)
    coffee_cups = round(offset / 50)
    all_stats.add(
        f"Over {coffee_cups} cups! Thats how many coffee cups you saved by flying with VerdeVoyage. "
        f"Our planet thanks you! ")
    all_stats.add(
        f"{light_bulb} hours. That is how many hours of having a light bulb turned on you have saved by flying with "
        f"VerdeVoyage.")
    all_stats.add(
        f"{plastic_bottles} bottles. That is how many plastic bottles you saved by choosing the most greenflight "
        f"to your destination!")
    all_stats.add(
        f"Choosing this flight over the others, you have saved the equivalent of not driving for {car_km} kilometers.")
    all_stats.add(
        f"By flying with VerdeVoyage, you have saved {avg_c02_percentage_person}% of an individuals "
        f"annual carbon usage.")
    return all_stats


def create_graph(airport_coords: dict[str, tuple[float, float]], home_airport: str = None, dest_airport: str = None,
                 dest_country: str = None) -> data_classes.Graph:
    """
    Return a graph containing home_airport and dest_airport as vertices, if given, and the flights between the airports
    as the edges connecting the two vertices.

    If home_airport and/or dest_airport is not given, return the appropriate graph.

    Preconditions:
        - dest_airport is None or home_airport is not None
    """
    graph = data_classes.Graph()
    with open('CSV Files/flight_data.csv') as file:
        reader = csv.reader(file)
        next(reader, None)              # skip the header

        for row in reader:

            # If any of the values are missing, then move to the next row
            if row[4] == '' or row[12] == '' or row[14] == '':
                continue

            if home_airport is None:
                create_graph_helper(graph, row, airport_coords)

            elif home_airport is not None and dest_airport is not None:
                if row[0] == home_airport and row[2] == dest_airport:
                    create_graph_helper(graph, row, airport_coords)

            elif home_airport is not None and dest_country is not None:
                if row[0] == home_airport and row[3].lower() == dest_country:
                    create_graph_helper(graph, row, airport_coords)

            else:   # home_airport is not None and both dest_airport and dest_country are None
                if row[0] == home_airport:
                    create_graph_helper(graph, row, airport_coords)

    return graph


def create_graph_helper(graph: data_classes.Graph, row: list[str],
                        airport_coords: dict[str, tuple[float, float]]) -> None:
    """
    Store the flight information in the given row in the graph.
    """
    graph.add_vertex(row[0], row[1], airport_coords[row[0]])
    graph.add_vertex(row[2], row[3], airport_coords[row[2]])

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
    print('Welcome to Verde Voyage! This is your ultimate eco-conscious dream vacation planner! \n')
    home_airports, home_countries, dest_airports, dest_countries = countries_and_airports('CSV Files/flight_data.csv')
    airport_coords = get_airport_coordinates()

    home_airport = input('What is your home airport? (Enter airport code) ').strip().upper()
    while home_airport not in home_airports:
        print('We are sorry! We do not have enough information on this airport. We are constantly trying '
              'to expand our reach. Please try a different airport.')

        home_airport = input('What is your home airport? (Enter airport code) ').strip().upper()

    # Display the graph from home_airport to all connecting airports.
    graph = create_graph(home_airport=home_airport, airport_coords=airport_coords)
    print("\nThese are all the connecting airports from your home airport.\n")
    test_viz.visualize_new_graph(graph, home_airport)

    questionare = input('Would you like to answer a few questions to get suggestions for travel destinations '
                        'that are perfect for you? (Y/N) ').strip().upper()
    while questionare == 'Y':
        data_classes.run_country_matchmaker('CSV Files/country_traits.csv')
        questionare = input('Would you like to take the questionare again? (Y/N) ').strip().upper()

    print()
    dest_country = input('Which country would you like to fly to? ').strip().lower()
    while dest_country not in dest_countries:
        print('We are sorry! We do not have enough information on this country. We are constantly trying '
              'to expand our reach. Please try a different country.')

        dest_country = input('Which country would you like to fly to? ').strip().lower()

    # Display the graph from home_airport to all airports in dest_country.
    graph = create_graph(home_airport=home_airport, dest_country=dest_country, airport_coords=airport_coords)
    print("\nThese are all the connecting airports in your chosen destination country from "
          "your home airport.\n")
    visualization.visualize_graph(graph)

    dest_airport = input('Which airport would you like to fly to? (Enter airport code) ').strip().upper()
    while dest_airport not in dest_airports:
        print('We are sorry! We do not have enough information on this airport. We are constantly trying '
              'to expand our reach. Please try a different airport.')

        dest_airport = input('Which airport would you like to fly to? (Enter airport code) ').strip().upper()

    # Display the graph from home_airport to dest_airport with at least 10 flights highlighted.
    graph = create_graph(home_airport=home_airport, dest_airport=dest_airport, airport_coords=airport_coords)

    print()
    emissions_weight = float(input('How much do you care about lowering your carbon footprint (5 - 10): '))
    while emissions_weight < 5 or emissions_weight > 10:
        print('Invalid input. The value must be between 5 and 10.')
        emissions_weight = float(input('How much do you care about lowering your carbon footprint (5 - 10): '))

    price_weight = float(input('How much do you care about the ticket price (0 - 5): '))
    while price_weight < 0 or price_weight > 5:
        print('Invalid input. The value must be between 0 and 5.')
        price_weight = float(input('How much do you care about the ticket price (0 - 5): '))

    stops_weight = float(input('How much do you care about the number of stops taken during your flight (0 - 5): '))
    while stops_weight < 0 or stops_weight > 5:
        print('Invalid input. The value must be between 0 and 5.')
        stops_weight = float(input('How much do you care about the number of stops taken during '
                                   'your flight (0 - 5): '))

    total_weight = emissions_weight + price_weight + stops_weight
    weights = (price_weight / total_weight), (stops_weight / total_weight), (emissions_weight / total_weight)

    routes = optimal_routes(graph, home_airport, dest_airport, weights)
    print('\nHere are the most optimal flight packages from your home airport to your chosen destination airport: ')
    print()
    for i in range(len(routes)):
        route = routes[i]
        print('Flight Package', i+1)
        print(f"Airline: {route[0][0]}")
        print(f"Aircrafts: {route[0][1]}")
        print(f"Price: ${route[1]} USD")
        print(f"Number of stops: {route[2]}")
        print(f"Carbon Emissions: {route[3]}g")
        print()

    chosen_route_num = int(input(f'Which flight package would you like to choose? (1 - {len(routes)}) '))
    while chosen_route_num > len(routes) or chosen_route_num < 1:
        print('Invalid input.')
        chosen_route_num = int(input(f'Which flight package would you like to choose? (1 - {len(routes)}) '))
    chosen_route = routes[chosen_route_num - 1]
    offset = graph.get_vertex(home_airport).max_emissions(dest_airport) - chosen_route[3]

    # Summary Block

    co2_stats = carbon_statistics(offset)
    print(random.choice(list(co2_stats)))
    print()
    print('Thank you for flying with VerdeVoyage.')
