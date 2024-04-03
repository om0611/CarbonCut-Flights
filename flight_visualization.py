import plotly.graph_objects as go
import data_classes
import numpy as np


def create_curve_path(lon1: float, lat1: float, lon2: float, lat2: float,
                      num_points: int = 100, curve_height: float = 0) -> tuple[np.array, np.array]:

    # Convert the values to radians because numpy functions work with radian values.
    lon1, lat1, lon2, lat2 = np.radians(lon1), np.radians(lat1), np.radians(lon2), np.radians(lat2)

    # Create num_points points between lat1 and lat2, and between lon1 and lon2
    lat_array = np.linspace(lat1, lat2, num_points)
    lon_array = np.linspace(lon1, lon2, num_points)

    # To add curvature, we will use the sin function.
    # We create num_points points between 0 and pi, and apply sin to it.
    # Then, we multiply by curve_height to stretch or compress the points,
    # giving us distinguishable paths between 0 and pi.
    modifier = np.sin(np.linspace(0, np.pi, num_points)) * curve_height

    if abs(lat1 - lat2) > abs(lon1 - lon2):
        lon_array = lon_array + modifier
    else:
        lat_array = lat_array + modifier

    # Add modifier to lat_array to apply the curvature.
    # At the endpoints (0 and pi), sin is 0 so no change is applied to the endpoints of lat_array.
    # new_lat_array = lat_array + modifier

    # Convert back to degrees and return.
    return np.degrees(lon_array), np.degrees(lat_array)

"""
def visualize_new_graph(graph: data_classes.Graph, home_airport_code: str = None,
                        dest_country: str = None, dest_airport_code: str = None) -> None:
    airport_to_coords = {}                      # maps airport to its coordinates
    connected_set = set()                       # stores a tuple containing airport_code and a neighbouring airport
    airport_code_to_country = {}                # maps airport_code to its country
    for vertex in graph.all_verticies():
        if vertex.airport_code not in airport_to_coords:
            airport_to_coords[vertex.airport_code] = vertex.coordinates
        for neighbor in vertex.get_neighbors():                                     # neighbor is an airport code
            if home_airport_code:
                if vertex.airport_code == home_airport_code:
                    connected_set.add((vertex.airport_code, neighbor))
            else:
                connected_set.add((vertex.airport_code, neighbor))
        if vertex.airport_code not in airport_code_to_country:
            airport_code_to_country[vertex.airport_code] = vertex.country_name

    graph_figure = go.Figure()

    ocean_color = "rgb(33, 158, 188)"  # blue for ocean
    land_color = "rgb(128, 237, 153)"  # green for land
    path_color = "rgb(242, 188, 49)"  # Gold for flight paths
    marker_color = "rgb(229, 56, 59)"  # Red for markers
    text_color = "rgb(85, 166, 48)"  # Green for Text

    for flight in connected_set:
        start = airport_to_coords[flight[0]]        # get the coordinates of the home_airport
        end = airport_to_coords[flight[1]]          # get the coordinates of the dest_airport
        flight_name = f"{flight[0]} to {airport_code_to_country[flight[1]]}"
        graph_figure.add_trace(go.Scattergeo(
            lon=[start[1], end[1]],
            lat=[start[0], end[0]],
            mode='lines',
            line=dict(width=2, color=path_color),
            name=flight_name  # Set the name for the flight path

        ))
    for airport in airport_to_coords:
        marker_name = airport
        graph_figure.add_trace(go.Scattergeo(
            lon=[airport_to_coords[airport][1]],
            lat=[airport_to_coords[airport][0]],
            mode='markers',
            marker=dict(size=5, color=marker_color),
            name=marker_name

        ))

    graph_figure.update_layout(
        title_text='<b>VerdeVoyage </b>',
        title_font=dict(size=24, color=text_color),
        showlegend=True,
        legend_title_text='Flight Paths',
        legend_title_font=dict(color=text_color),
        legend_font=dict(color=text_color),
        geo=dict(
            projection_type="orthographic",
            showland=True,
            landcolor=land_color,
            countrycolor=text_color,
            oceancolor=ocean_color,
            lakecolor=ocean_color,
            showocean=True,
        )
    )

    graph_figure.show()
"""


def visualize_new_graph(graph: data_classes.Graph, airport_coords: dict[str, tuple[float, float]],
                        home_airport: str = None, dest_airport: str = None) -> None:
    """
    Visualize the given graph using plotly.

    Preconditions:
        - home_airport in airport_coords and dest_airport in airport_coords
        - dest_airport is None or home_airport is not None
        - The given graph is created based on the given specifications for home_airport and dest_airport.
    """
    graph_figure = go.Figure()

    ocean_color = "rgb(33, 158, 188)"  # blue for ocean
    land_color = "rgb(128, 237, 153)"  # green for land
    path_color = "rgb(242, 188, 49)"  # Gold for flight paths
    marker_color = "rgb(229, 56, 59)"  # Red for markers
    text_color = "rgb(85, 166, 48)"  # Green for Text

    if dest_airport is not None:
        lat1, lon1 = airport_coords[home_airport]
        lat2, lon2 = airport_coords[dest_airport]
        v1 = graph.get_vertex(home_airport)
        v2 = graph.get_vertex(dest_airport)
        flights = list(v1.neighbours[v2].keys())

        # Visualize at most 5 paths between home_airport and dest_airport
        for i in range(min(5, len(flights))):
            lon_array, lat_array = create_curve_path(lon1, lat1, lon2, lat2, curve_height=((-1)**i)*(0.05*i))
            flight = flights[i]
            flight_name = f"{flight[0]}: {flight[1]}"
            graph_figure.add_trace(go.Scattergeo(
                lon=lon_array,
                lat=lat_array,
                mode='lines',
                line=dict(width=2, color=path_color),
                name=flight_name                                 # Set the name for the flight path
            ))

        for airport in [home_airport, dest_airport]:
            graph_figure.add_trace(go.Scattergeo(
                lon=[airport_coords[airport][1]],
                lat=[airport_coords[airport][0]],
                mode='markers',
                marker=dict(size=5, color=marker_color),
                name=airport
            ))

    elif home_airport is not None:
        visited = set()
        v1 = graph.get_vertex(home_airport)
        lat1, lon1 = airport_coords[home_airport]
        visited.add(v1)

        for v2 in v1.neighbours:
            if v2 not in visited:
                lat2, lon2 = airport_coords[v2.airport_code]
                flight_name = f"{home_airport} to {v2.country_name}"

                graph_figure.add_trace(go.Scattergeo(
                    lon=[lon1, lon2],
                    lat=[lat1, lat2],
                    mode='lines',
                    line=dict(width=2, color=path_color),
                    name=flight_name
                ))

                visited.add(v2)

        for v in visited:
            lat, lon = airport_coords[v.airport_code]
            graph_figure.add_trace(go.Scattergeo(
                lon=[lon],
                lat=[lat],
                mode='markers',
                marker=dict(size=5, color=marker_color),
                name=v.airport_code
            ))

    else:
        visited = set()
        for v1 in graph.all_verticies():                # graph.all_vertices() returns a set of all vertex objects
            lat1, lon1 = airport_coords[v1.airport_code]
            for v2 in v1.neighbours:
                if (v1, v2) not in visited and (v2, v1) not in visited:
                    lat2, lon2 = airport_coords[v2.airport_code]
                    flight_name = f"{v1.airport_code} to {v2.country_name}"

                    graph_figure.add_trace(go.Scattergeo(
                        lon=[lon1, lon2],
                        lat=[lat1, lat2],
                        mode='lines',
                        line=dict(width=2, color=path_color),
                        name=flight_name
                    ))

                    visited.add((v1, v2))

            graph_figure.add_trace(go.Scattergeo(
                lon=[lon1],
                lat=[lat1],
                mode='markers',
                marker=dict(size=5, color=marker_color),
                name=v1.airport_code
            ))

    graph_figure.update_layout(
        title_text='<b>VerdeVoyage: FLy the Dreak Keep it Green </b>',
        title_font=dict(size=24, color=text_color),
        showlegend=True,
        legend_title_text='Flight Paths',
        legend_title_font=dict(color=text_color),
        legend_font=dict(color=text_color),
        geo=dict(
            projection_type="orthographic",
            showland=True,
            landcolor=land_color,
            countrycolor=text_color,
            oceancolor=ocean_color,
            lakecolor=ocean_color,
            showocean=True,
        )
    )

    graph_figure.show()
