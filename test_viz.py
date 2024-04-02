
import plotly.graph_objects as go
import data_classes

def viusualize_new_graph(graph: data_classes.Graph):
    airport_to_coords = {}
    connected_set = set()
    for vertex in graph.all_verticies():
        if vertex.airport_code not in airport_to_coords:
            airport_to_coords[vertex.airport_code] = vertex.cordinates
        for neighbor in vertex.neighbors():
            if (vertex.airport_code, neighbor) not in connected_set or (neighbor, vertex.airport_code) not in connected_set:
                connected_set.add((vertex.airport_code, neighbor))

    graph_figure = go.Figure()

    for flight in connected_set:
        start = airport_to_coords[flight[0]]
        end = airport_to_coords[flight[1]]
        graph_figure.add_trace(go.Scattergeo(
            lon = [start[1], end[1]],
            lat = [start[0], end[0]],
            mode='lines',
            line=dict(width=2, color='blue'),

        ))
    for airport in airport_to_coords:
        graph_figure.add_trace(go.Scattergeo(
            lon = [airport_to_coords[airport][1]],
            lat = [airport_to_coords[airport][0]],
            mode='markers',
            marker=dict(size=5, color='red')

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
