import tkinter as tk
from tkinter import ttk
import requests
import gmaps
import webbrowser
import time

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps.configure(api_key='AIzaSyBP6tQtER1QZgDpzTN19W6JLvyvQE8p_ds')

# OpenStreetMap API endpoint for route calculation
OSM_API_ENDPOINT = "http://router.project-osrm.org/route/v1/driving/"

class RouteOptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Optimization Tool")

        self.source_label = ttk.Label(root, text="Source Location:")
        self.source_entry = ttk.Entry(root)

        self.destination_label = ttk.Label(root, text="Destination Location:")
        self.destination_entry = ttk.Entry(root)

        self.calculate_button = ttk.Button(root, text="Calculate Route", command=self.calculate_route)

        self.map_frame = ttk.Frame(root)
        self.map_frame.grid(row=5, column=0, columnspan=3)

        self.source_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_entry.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.destination_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.destination_entry.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.calculate_button.grid(row=4, column=0, pady=10)

    def calculate_route(self):
        source_location = self.source_entry.get()
        destination_location = self.destination_entry.get()

        if source_location and destination_location:
            # Extract coordinates from location strings
            source_coords = self.extract_coordinates(source_location)
            destination_coords = self.extract_coordinates(destination_location)

            if source_coords and destination_coords:
                route_coordinates = self.get_route(source_coords, destination_coords)

                if route_coordinates:
                    self.display_route_on_map(route_coordinates)
                else:
                    print("Error calculating route. Please check your input.")
            else:
                print("Invalid coordinates. Please enter valid coordinates.")
        else:
            print("Please enter both source and destination locations.")

    def extract_coordinates(self, location):
        try:
            coords = [float(coord) for coord in location.split(',')]
            return coords
        except ValueError:
            print(f"Invalid coordinates: {location}")
            return []

    def get_route(self, source, destination):
        source_coords = self.get_coordinates(source)
        destination_coords = self.get_coordinates(destination)

        if source_coords and destination_coords:
            url = f"{OSM_API_ENDPOINT}{source_coords[1]},{source_coords[0]};{destination_coords[1]},{destination_coords[0]}?overview=false"
            response = requests.get(url)
            data = response.json()

            print("OSM API Response:", data)  # Print the entire response for debugging

            if 'routes' in data and data['routes']:
                # Use the first route as an example; modify as needed based on your requirements
                route = data['routes'][0]

                # Extract coordinates from the 'legs' section of the route
                route_coordinates = [
                    [step['location'][1], step['location'][0]] for leg in route['legs'] if 'steps' in leg
                    for step in leg['steps']
                ]

                return route_coordinates
            else:
                return []
        else:
            return []

    def get_coordinates(location):
        if isinstance(location, list):
            return location

        try:
            coords = [float(coord.strip()) for coord in location.split(',')]
            if len(coords) == 2:
                return coords
            else:
                print(f"Invalid coordinates: {location}")
                return []
        except ValueError:
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={location}")
            data = response.json()
            print("Nominatim API Response:", data)

            if data and len(data) > 0:
                lat = data[0].get('lat')
                lon = data[0].get('lon')

                if lat and lon:
                    return [float(lat), float(lon)]
                else:
                    print(f"Geocoding failed for location: {location}")
                    return []
            else:
                print(f"Geocoding failed for location: {location}")
                return []

    def display_route_on_map(self, route_coordinates):
        gmaps_fig = gmaps.figure(center=(route_coordinates[0][1], route_coordinates[0][0]), zoom_level=14)
        route_layer = gmaps.directions_layer(route_coordinates[0], route_coordinates[-1],
                                             waypoints=route_coordinates[1:-1], travel_mode='DRIVING')
        gmaps_fig.add_layer(route_layer)

        # Display the gmaps map
        webbrowser.open(gmaps_fig.url)

if __name__ == "__main__":
    root = tk.Tk()
    app = RouteOptimizationApp(root)
    root.mainloop()
