import numpy as np
import matplotlib.pyplot as plt

def compute_semicircle(center, track_width_deg_lon, theta, vec_ip_tgt_norm):
    """
    Compute the coordinates of a semicircle given center, track width, angle, and normalization vector.
    
    Parameters:
    center (tuple): Center of the semicircle (latitude, longitude).
    track_width_deg_lon (float): Width of the track in degrees of longitude.
    theta (array): Array of angles to define the semicircle.
    vec_ip_tgt_norm (array): Normalized vector pointing from IP to TGT.
    
    Returns:
    array: Transformed coordinates of the semicircle.
    """
    # Create the semicircle points
    semicircle = np.array([
        center[0] + (track_width_deg_lon / 2) * np.cos(theta),
        center[1] + (track_width_deg_lon / 2) * np.sin(theta)
    ]).T
    
    # Transformation matrix based on the IP-TGT vector
    transformation_matrix = np.array([
        [vec_ip_tgt_norm[0], vec_ip_tgt_norm[1]],
        [-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]]
    ])
    
    # Apply the transformation
    semicircle_transformed = (semicircle - center) @ transformation_matrix + center
    
    return semicircle_transformed

def calculate_midpoint(ip, tgt, distance_deg_lon):
    """
    Calculate the midpoint between the IP and TGT, optionally shifting it behind the IP.
    
    Parameters:
    ip (tuple): Initial Point (latitude, longitude).
    tgt (tuple): Target Point (latitude, longitude).
    distance_deg_lon (float): Distance to place the midpoint behind the IP in degrees of longitude.
    
    Returns:
    array: Coordinates of the midpoint.
    """
    # Normalized direction vector from TGT to IP (opposite direction)
    direction_vector = np.array([-tgt[0] + ip[0], -tgt[1] + ip[1]]) / np.linalg.norm(np.array([-tgt[0] + ip[0], -tgt[1] + ip[1]]))
    
    # Calculate the midpoint
    midpoint = np.array([ip[0], ip[1]]) + distance_deg_lon * direction_vector
    
    return midpoint

def generate_hold_pattern(ip, tgt, speed, time_minutes, track_width, distance_to_ip, hold_type):
    """
    Generates a holding pattern based on the initial point (IP), target (TGT),
    aircraft speed, time in minutes, and pattern type.
    
    Parameters:
    ip (tuple): Initial Point coordinates (latitude, longitude).
    tgt (tuple): Target Point coordinates (latitude, longitude).
    speed (float): Aircraft speed in knots (nautical miles per hour).
    time_minutes (float): Time in minutes for the leg length calculation.
    track_width (float): Width of the track in nautical miles.
    distance_to_ip (float): Distance of the pattern to IP in nautical miles.
    hold_type (str): Type of holding pattern, either "eight-figure" or "racetrack".
    
    Returns:
    dict: A dictionary containing the pattern points (straight legs and semicircles).
    """
    # Convert time from minutes to hours
    time_hours = time_minutes / 60.0
    
    # Calculate leg length in degrees of latitude
    leg_length_deg_lat = (speed * time_hours) / 60.0
    
    # Track width in degrees of longitude
    track_width_deg_lon = track_width / 60.0
    
    # Distance to midpoint in degrees of longitude
    distance_deg_lon = distance_to_ip / 60.0
    
    # Calculate the normalized vector from IP to TGT
    vec_ip_tgt = np.array([tgt[0] - ip[0], tgt[1] - ip[1]])
    vec_ip_tgt_norm = vec_ip_tgt / np.linalg.norm(vec_ip_tgt)
    
    # Calculate the midpoint
    midpoint = calculate_midpoint(ip, tgt, distance_deg_lon)
    
    # Calculate the centers of the semicircles
    perp_vec = np.array([-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]])
    center_1 = midpoint + (leg_length_deg_lat / 2) * perp_vec
    center_2 = midpoint - (leg_length_deg_lat / 2) * perp_vec
    
    # Define angles for the semicircles
    theta = np.linspace(0, np.pi, 100)
    
    # Compute the semicircles
    semicircle_1 = compute_semicircle(center_1, track_width_deg_lon, theta, vec_ip_tgt_norm)
    semicircle_2 = compute_semicircle(center_2, track_width_deg_lon, theta + np.pi, vec_ip_tgt_norm)
    
    # Determine the straight legs based on the hold type
    if hold_type == "racetrack":
        start_leg_1, end_leg_1 = semicircle_1[-1], semicircle_2[0]
        start_leg_2, end_leg_2 = semicircle_2[-1], semicircle_1[0]
    elif hold_type == "eight-figure":
        start_leg_1, end_leg_1 = semicircle_1[-1], semicircle_2[-1]
        start_leg_2, end_leg_2 = semicircle_2[0], semicircle_1[0]
    
    # Combine points into the hold pattern
    hold_track_points = {
        'leg_1': [start_leg_1, end_leg_1],
        'semicircle_1': semicircle_1,
        'leg_2': [start_leg_2, end_leg_2],
        'semicircle_2': semicircle_2
    }
    
    return hold_track_points

def plot_hold_pattern(hold_track_points, ip, tgt):
    """
    Plot the generated holding pattern.
    
    Parameters:
    hold_track_points (dict): Dictionary containing the points of the pattern.
    ip (tuple): Initial Point (latitude, longitude).
    tgt (tuple): Target Point (latitude, longitude).
    """
    plt.figure(figsize=(8, 8))
    
    # Plot the legs
    leg_1 = hold_track_points['leg_1']
    plt.plot([leg_1[0][0], leg_1[1][0]], [leg_1[0][1], leg_1[1][1]], 'b-')
    
    leg_2 = hold_track_points['leg_2']
    plt.plot([leg_2[0][0], leg_2[1][0]], [leg_2[0][1], leg_2[1][1]], 'b-')
    
    # Plot the semicircles
    semicircle_1 = hold_track_points['semicircle_1']
    plt.plot(semicircle_1[:, 0], semicircle_1[:, 1], 'r-')
    
    semicircle_2 = hold_track_points['semicircle_2']
    plt.plot(semicircle_2[:, 0], semicircle_2[:, 1], 'r-')
    
    # Plot the IP and TGT
    plt.plot(ip[0], ip[1], 'ys', label='Initial Point (IP)')
    plt.plot(tgt[0], tgt[1], 'r^', label='Target (TGT)')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.axis('equal')
    plt.title('Holding Pattern')
    plt.legend()
    plt.show()

# Example usage
ip = (-108, 7.3)  # Initial Point (latitude, longitude)
tgt = (-108.5, 7.38)  # Target Point (latitude, longitude)
speed = 180  # Aircraft speed in knots
time_minutes = 2  # Time in minutes for the leg length
track_width = 1.5  # Width of the pattern in nautical miles
distance_to_ip = 2  # Distance of the pattern to IP in nautical miles
# hold_type = "eight-figure"  # Either "eight-figure" or "racetrack"
hold_type = "racetrack"  # Either "eight-figure" or "racetrack"

# Generate and plot the hold pattern
hold_pattern = generate_hold_pattern(ip, tgt, speed, time_minutes, track_width, distance_to_ip, hold_type)
plot_hold_pattern(hold_pattern, ip, tgt)
