import tkinter as tk
from tkinter import ttk
import requests
import webbrowser
from geopy.geocoders import Nominatim

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
            source_coords = self.get_coordinates(source_location)
            destination_coords = self.get_coordinates(destination_location)

            if source_coords and destination_coords:
                # You can use the coordinates for your desired purpose
                print("Source Coordinates:", source_coords)
                print("Destination Coordinates:", destination_coords)
                route_coordinates = self.get_route(source_coords, destination_coords)
                if route_coordinates:
                    print("Route Coordinates:", route_coordinates)
                    # Add your code to display the route on the map or perform other operations
                else:
                    print("Error calculating route. Please check your input.")
            else:
                print("Invalid coordinates. Please enter valid coordinates.")
        else:
            print("Please enter both source and destination locations.")

    def get_coordinates(self, location):
        geolocator = Nominatim(user_agent="route_optimizer")
        try:
            location_info = geolocator.geocode(location)
            if location_info:
                return [location_info.latitude, location_info.longitude]
            else:
                print(f"Geocoding failed for location: {location}")
                return []
        except Exception as e:
            print(f"Error during geocoding: {e}")
            return []

    def get_route(self, source_coords, destination_coords):
        # Add your code to fetch the route using source and destination coordinates
        # Return the route coordinates
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = RouteOptimizationApp(root)
    root.mainloop()
