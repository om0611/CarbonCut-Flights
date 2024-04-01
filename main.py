"""
This Python file contains the code to run our program.
"""
import csv
import data_classes
import helper_functions


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
