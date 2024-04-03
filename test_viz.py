import plotly.graph_objects as go
import data_classes


def visualize_new_graph(graph: data_classes.Graph, home_airport_code: str = None):
    airport_to_coords = {}
    connected_set = set()
    airport_code_to_country = {}
    for vertex in graph.all_verticies():
        if vertex.airport_code not in airport_to_coords:
            airport_to_coords[vertex.airport_code] = vertex.coordinates
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

    ocean_color = "rgb(64, 89, 128)"  # blue for ocean
    land_color = "rgb(163, 204, 163)"  # green for land
    path_color = "rgb(242, 188, 49)"  # Gold for flight paths
    marker_color = "rgb(217, 72, 72)"  # Warm red for markers
    text_color = "rgb(34, 40, 49)"  # Dark grey for text

    for flight in connected_set:
        start = airport_to_coords[flight[0]]
        end = airport_to_coords[flight[1]]
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
