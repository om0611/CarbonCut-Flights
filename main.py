"""
This Python file contains the main code for our project.
"""
import csv
import data_classes


def calculate_flight_scores(flights: dict[tuple[str, tuple], list[int]],
                            weights: tuple[float, int, int] = (0.1, 0.1, 0.8)) -> dict[tuple[str, tuple], float]:
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


# Example Code
home_airport = 'YYZ'
dest_airport = 'LHR'
graph = data_classes.Graph()

with open('flight_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader, None)          # skip the header
    for row in reader:
        if row[0] == home_airport:
            graph.add_vertex(row[0], row[1])
            graph.add_vertex(row[2], row[3])

            # If any of the values are missing, then move to the next row
            if row[4] == '' or row[12] == '' or row[14] == '':
                continue

            aircrafts = tuple(row[4].split('|'))
            airline = row[6].split('| ')[0].strip('[]')
            stops = int(row[11])
            price = float(row[12])
            emissions = int(row[14])

            flight_package = (airline, aircrafts)
            flight_info = [price, stops, emissions]
            graph.add_edge(row[0], row[2], (flight_package, flight_info))
