import networkx as nx
import gmaps
import folium
from IPython.display import display

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps.configure(api_key='YOUR_API_KEY')

# Step 1: Data Collection (Simulated Data)
G = nx.Graph()
G.add_edge("Bangalore", "Mysore", weight=150)  # Example weight (distance) between Bangalore and Mysore

# Step 2: Route Planning Algorithm
def optimize_route(graph, source, destination):
    optimized_route = nx.shortest_path(graph, source=source, target=destination, weight='weight')
    return optimized_route

# Step 3: User Input
source_location = input("Enter the source location: ")
destination_location = input("Enter the destination location: ")

# Validate user input
if source_location not in G.nodes or destination_location not in G.nodes:
    print("Invalid source or destination location. Please enter valid locations.")
else:
    # Step 4: Generate Optimized Route
    optimized_route = optimize_route(G, source_location, destination_location)
    print("Optimized Route:", optimized_route)

    # Step 5: Map Visualization (Using gmaps and folium)
    # Create a gmaps figure centered around Bangalore
    gmaps_fig = gmaps.figure(center=(12.9716, 77.5946), zoom_level=7)

    # Extract the latitude and longitude of each location in the optimized route
    route_coordinates = [(12.9716, 77.5946), (12.2958, 76.6394)]  # Replace with actual coordinates

    # Draw the route on the gmaps map
    route_layer = gmaps.directions_layer(route_coordinates[0], route_coordinates[-1],
                                         waypoints=route_coordinates[1:-1], travel_mode='DRIVING')
    gmaps_fig.add_layer(route_layer)

    # Display the gmaps map
    display(gmaps_fig)

    # Create a folium map for comparison
    folium_map = folium.Map(location=(12.9716, 77.5946), zoom_start=7)
    folium.PolyLine(locations=route_coordinates, color='blue').add_to(folium_map)

    # Save the folium map as an HTML file
    folium_map_path = "optimized_route_folium.html"
    folium_map.save(folium_map_path)

    # Display file path for user convenience
    print(f"Folium Map saved to: {folium_map_path}")

