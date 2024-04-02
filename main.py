"""
This Python file contains the code to run our program.
"""
import csv
import data_classes
import helper_functions
import test_viz


# Example Code
home_airport = 'YYZ'
graph = data_classes.Graph()

with open('CSV Files/flight_data.csv', 'r') as file:
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

airport_codes = {}
with open('CSV Files/78_airport_info.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader, None)      #skip the header
    for row in reader:
        airport_codes[row[0]] = (float(row[1]), float(row[2]))

for vertex in data_classes.Graph.all_verticies(graph):
    vertex.cordinates = airport_codes[vertex.airport_code]
