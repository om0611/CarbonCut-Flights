import plotly.graph_objects as go
import data_classes


def viusualize_new_graph(graph: data_classes.Graph, home_airport_code: str = None):
    airport_to_coords = {}
    connected_set = set()
    airport_code_to_country = {}
    for vertex in graph.all_verticies():
        if vertex.airport_code not in airport_to_coords:
            airport_to_coords[vertex.airport_code] = vertex.cordinates
        for neighbor in vertex.neighbors():
            if home_airport_code:
                if vertex.airport_code == home_airport_code:
                    connected_set.add((vertex.airport_code, neighbor))
            else:
                if (vertex.airport_code, neighbor) not in connected_set or (
                    neighbor, vertex.airport_code) not in connected_set:
                        connected_set.add((vertex.airport_code, neighbor))
        if vertex.airport_code not in airport_code_to_country:
            airport_code_to_country[vertex.airport_code] = vertex.country_name

    graph_figure = go.Figure()

    for flight in connected_set:
        start = airport_to_coords[flight[0]]
        end = airport_to_coords[flight[1]]
        flight_name = f"{flight[0]} to {airport_code_to_country[flight[1]]}"
        graph_figure.add_trace(go.Scattergeo(
            lon=[start[1], end[1]],
            lat=[start[0], end[0]],
            mode='lines',
            line=dict(width=2, color='blue'),
            name=flight_name  # Set the name for the flight path

        ))
    for airport in airport_to_coords:
        marker_name = airport
        graph_figure.add_trace(go.Scattergeo(
            lon=[airport_to_coords[airport][1]],
            lat=[airport_to_coords[airport][0]],
            mode='markers',
            marker=dict(size=5, color='red'),
            name=marker_name

        ))

    graph_figure.update_layout(
        title_text='Example Flight Paths',
        showlegend=True,
        geo=dict(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
    )

    graph_figure.show()
