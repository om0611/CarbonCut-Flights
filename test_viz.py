
import plotly.graph_objects as go

# Manually defined "airports" with latitude and longitude
airports = {
    'JFK': {'name': 'John F. Kennedy International Airport', 'lat': 40.6413, 'lon': -73.7781},
    'LAX': {'name': 'Los Angeles International Airport', 'lat': 33.9416, 'lon': -118.4085},
    'LHR': {'name': 'London Heathrow Airport', 'lat': 51.4700, 'lon': -0.4543},
    'CDG': {'name': 'Charles de Gaulle Airport', 'lat': 49.0097, 'lon': 2.5479},
}

# Manually defined "flights" between airports
flights = [
    ('JFK', 'LAX'),
    ('JFK', 'LHR'),
    ('LHR', 'CDG'),
    ('CDG', 'JFK'),  # Demonstrates a round trip
]

fig = go.Figure()

# Add lines for each flight path
for flight in flights:
    start = airports[flight[0]]
    end = airports[flight[1]]

    fig.add_trace(go.Scattergeo(
        lon=[start['lon'], end['lon']],
        lat=[start['lat'], end['lat']],
        mode='lines',
        line=dict(width=2, color='blue'),
    ))

# Add points for each airport
for airport in airports.values():
    fig.add_trace(go.Scattergeo(
        lon=[airport['lon']],
        lat=[airport['lat']],
        mode='markers',
        marker=dict(size=5, color='red'),
        name=airport['name']
    ))

fig.update_layout(
    title_text='Example Flight Paths',
    showlegend=True,
    geo=dict(
        projection_type="orthographic",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)",
    ),
)

fig.show()

import plotly.graph_objects as go
import numpy as np


def great_circle_points(lon1, lat1, lon2, lat2, num_points=100, curve_height=0):
    """
    Generate points for a great circle path, adding a curve height to visualize multiple edges.
    """
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Interpolate points
    lon_arr = np.linspace(lon1, lon2, num_points)
    lat_arr = np.linspace(lat1, lat2, num_points)

    # Adjust the curve height based on the distance between points
    f = np.sin(np.linspace(0, np.pi, num_points)) * curve_height
    lat_arr = np.arcsin(np.sin(lat_arr) * np.cos(f) + np.cos(lat_arr) * np.sin(f) * np.cos(lon_arr - lon1))

    # Convert back to degrees
    lon_arr, lat_arr = map(np.degrees, [lon_arr, lat_arr])
    return lon_arr, lat_arr


# Example usage with multiple flights between JFK and LAX
airports = {
    'JFK': {'name': 'John F. Kennedy International Airport', 'lat': 40.6413, 'lon': -73.7781},
    'LAX': {'name': 'Los Angeles International Airport', 'lat': 33.9416, 'lon': -118.4085},
}

flights = [
    ('JFK', 'LAX', 0.1),  # Tuple format (start, end, curve_height)
    ('JFK', 'LAX', 0.15),
    # Add as many as needed, adjusting curve_height for visibility
]

fig = go.Figure()

# Plot each flight path with a unique curve
for flight in flights:
    start = airports[flight[0]]
    end = airports[flight[1]]
    curve_height = flight[2]  # Control the height of the curve

    lon_arr, lat_arr = great_circle_points(start['lon'], start['lat'], end['lon'], end['lat'],
                                           curve_height=curve_height)
    fig.add_trace(go.Scattergeo(
        lon=lon_arr,
        lat=lat_arr,
        mode='lines',
        line=dict(width=2, color='blue'),
    ))

# Add markers for airports
for airport in airports.values():
    fig.add_trace(go.Scattergeo(
        lon=[airport['lon']],
        lat=[airport['lat']],
        mode='markers',
        marker=dict(size=5, color='red'),
        name=airport['name']
    ))

fig.update_layout(
    title_text='Multiple Flight Paths Between JFK and LAX',
    showlegend=False,
    geo=dict(
        projection_type="orthographic",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)",
    ),
)

fig.show()
