import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy import Point

def generate_eight_figure_pattern(ip, tgt, radius=1):
    # ip and tgt are tuples (latitude, longitude)
    
    # Calculate the midpoint between IP and TGT
    mid_lat = (ip[0] + tgt[0]) / 2
    mid_lon = (ip[1] + tgt[1]) / 2
    midpoint = Point(mid_lat, mid_lon)
    
    # Calculate the azimuth (bearing) between IP and TGT
    def calculate_bearing(start, end):
        lat1 = np.radians(start[0])
        lat2 = np.radians(end[0])
        diff_lon = np.radians(end[1] - start[1])
        
        x = np.sin(diff_lon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(diff_lon))
        
        initial_bearing = np.degrees(np.arctan2(x, y))
        bearing = (initial_bearing + 360) % 360
        return bearing
    
    bearing = calculate_bearing(ip, tgt)
    
    # Generate semicircles
    angles1 = np.linspace(0, np.pi, 50)
    angles2 = np.linspace(0, -np.pi, 50)
    
    def generate_semicircle(center, angles, radius):
        return [(center.latitude + (radius / 111) * np.sin(angle), 
                 center.longitude + (radius / 111) * np.cos(angle)) for angle in angles]

    # Generate semicircles around midpoint
    semi1 = generate_semicircle(midpoint, angles1, radius)
    semi2 = generate_semicircle(midpoint, angles2, radius)
    
    # Rotate and translate to align with bearing
    def rotate_translate(point, origin, bearing):
        angle_rad = np.radians(bearing)
        lat_diff = point[0] - origin.latitude
        lon_diff = point[1] - origin.longitude
        
        new_lat = origin.latitude + lat_diff * np.cos(angle_rad) - lon_diff * np.sin(angle_rad)
        new_lon = origin.longitude + lat_diff * np.sin(angle_rad) + lon_diff * np.cos(angle_rad)
        
        return new_lat, new_lon
    
    semi1_rotated = [rotate_translate(point, midpoint, bearing) for point in semi1]
    semi2_rotated = [rotate_translate(point, midpoint, bearing) for point in semi2]
    
    # Combine semicircles to form figure-eight pattern
    figure_eight_pattern = semi1_rotated + semi2_rotated
    
    return figure_eight_pattern

def plot_eight_figure_pattern(pattern, ip, tgt):
    plt.figure(figsize=(8, 8))
    
    # Plot pattern
    pattern_lat, pattern_lon = zip(*pattern)
    
    plt.plot(pattern_lon, pattern_lat, 'k-', label="Eight Figure Pattern")
    
    # Plot IP and TGT
    plt.plot(ip[1], ip[0], 'ys', label="Initial Point")
    plt.plot(tgt[1], tgt[0], 'r^', label="Target")
    
    plt.legend()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Eight Figure Hold Pattern')
    plt.grid(True)
    plt.show()

# Example usage:
ip = (34.0, -117.0)  # Initial Point (latitude, longitude)
tgt = (34.2, -117.2)  # Target (latitude, longitude)
pattern = generate_eight_figure_pattern(ip, tgt)
plot_eight_figure_pattern(pattern, ip, tgt)
