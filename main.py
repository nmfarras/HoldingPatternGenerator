import numpy as np
import matplotlib.pyplot as plt

def compute_semicircle(center, track_width_deg_lon, theta, vec_ip_tgt_norm):
    """Compute the coordinates of a semicircle given center, track width, angle, and normalization vector."""
    # Create the semicircle points
    semicircle = np.array([
        center[0] + (track_width_deg_lon / 2) * np.cos(theta),
        center[1] + (track_width_deg_lon / 2) * np.sin(theta)
    ]).T
    
    # Define the transformation matrix
    transformation_matrix = np.array([
        [vec_ip_tgt_norm[0], vec_ip_tgt_norm[1]],
        [-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]]
    ])
    
    # Apply the transformation
    semicircle_transformed = (semicircle - center) @ transformation_matrix + center
    
    return semicircle_transformed

def generate_racetrack(ip, tgt, speed, time_minutes, track_width, distance):
    """
    Generates a racetrack pattern based on the initial point (IP), target (TGT),
    aircraft speed, and time in minutes.
    
    Parameters:
    ip (tuple): Initial point coordinates (x, y).
    tgt (tuple): Target point coordinates (x, y).
    speed (float): Aircraft speed in knots (nautical miles per hour).
    time_minutes (float): Time in minutes for the leg length calculation.
    track_width (float): Width of the racetrack.
    
    Returns:
    dict: A dictionary containing the racetrack points (straight legs and semicircles).
    """
    # Convert time from minutes to hours
    time_hours = time_minutes / 60.0
    
    # Calculate leg length (distance covered in the given time)
    leg_length = speed * time_hours  # in nautical miles
    
    leg_length_deg_lat = leg_length/60
    
    track_width_deg_lon = track_width / 60.0
    
    distance_deg_lon = distance / 60.0
    
    # Calculate the vector from IP to TGT
    vec_ip_tgt = np.array([tgt[0] - ip[0], tgt[1] - ip[1]])
    vec_ip_tgt_norm = vec_ip_tgt / np.linalg.norm(vec_ip_tgt)
    
    # Perpendicular vector to IP-TGT (rotate by 90 degrees)
    perp_vec = np.array([-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]])
    
    # Calculate the midpoint between start_leg_1 and end_leg_1
    ## Between IP and TGT
    # midpoint = (np.array(ip) + np.array(tgt)) / 2
    
    ## Behind IP
    # Calculate the normalized direction vector in the opposite direction
    midpoint_placement_direction = np.array([-tgt[0] + ip[0], -tgt[1] + ip[1]]) / np.linalg.norm(np.array([-tgt[0] + ip[0], -tgt[1] + ip[1]]))
    midpoint = np.array([ip[0],ip[1]]) + distance_deg_lon * midpoint_placement_direction
    
    # Adjust the centers to ensure the distance between them is leg_length
    center_1 = midpoint + (leg_length_deg_lat / 2) * perp_vec
    center_2 = midpoint - (leg_length_deg_lat / 2) * perp_vec
    
    theta = np.linspace(0, np.pi, 100)
    
    ## This function doesn't required function compute_semicircle()
    # semicircle_1 = np.array([center_1[0] + (track_width_deg_lon / 2) * np.cos(theta),
                             # center_1[1] + (track_width_deg_lon / 2) * np.sin(theta)]).T
    # semicircle_1 = (semicircle_1 - center_1) @ np.array([[vec_ip_tgt_norm[0], vec_ip_tgt_norm[1]],
                                                         # [-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]]]) + center_1
    
    # semicircle_2 = np.array([center_2[0] + (track_width_deg_lon / 2) * np.cos(theta + np.pi),
                             # center_2[1] + (track_width_deg_lon / 2) * np.sin(theta + np.pi)]).T
    # semicircle_2 = (semicircle_2 - center_2) @ np.array([[vec_ip_tgt_norm[0], vec_ip_tgt_norm[1]],
                                                         # [-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]]]) + center_2
    
    # Compute semicircle_1
    semicircle_1 = compute_semicircle(center_1, track_width_deg_lon, theta, vec_ip_tgt_norm)

    # Compute semicircle_2
    semicircle_2 = compute_semicircle(center_2, track_width_deg_lon, theta + np.pi, vec_ip_tgt_norm)

    # Calculate the points for the straight legs
    start_leg_1 = semicircle_1[-1]
    end_leg_1 = semicircle_2[0]
    
    start_leg_2 = semicircle_2[-1]
    end_leg_2 = semicircle_1[0]
    
    # Combine points into the racetrack
    racetrack_points = {
        'leg_1': [start_leg_1, end_leg_1],
        'semicircle_1': semicircle_1,
        'leg_2': [start_leg_2, end_leg_2],
        'semicircle_2': semicircle_2
    }
    
    return racetrack_points

def plot_racetrack(racetrack_points, ip, tgt):
    plt.figure(figsize=(8, 8))
    
    # Plot straight legs
    leg_1 = racetrack_points['leg_1']
    plt.plot([leg_1[0][0], leg_1[1][0]], [leg_1[0][1], leg_1[1][1]], 'b-')
    
    leg_2 = racetrack_points['leg_2']
    plt.plot([leg_2[0][0], leg_2[1][0]], [leg_2[0][1], leg_2[1][1]], 'b-')
    
    # Plot semicircles
    semicircle_1 = racetrack_points['semicircle_1']
    plt.plot(semicircle_1[:, 0], semicircle_1[:, 1], 'r-')
    
    semicircle_2 = racetrack_points['semicircle_2']
    plt.plot(semicircle_2[:, 0], semicircle_2[:, 1], 'r-')
    
    plt.plot(ip[0], ip[1], 'y*')
    plt.plot(tgt[0], tgt[1], 'k*')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.axis('equal')
    plt.title('Racetrack Pattern')
    plt.show()

# Example usage
ip = (-108, 7.3)  # Initial point
tgt = (-108.5, 7.38)  # Target point
speed = 180  # Aircraft speed in knots
time_minutes = 2  # Time in minutes for the leg length
track_width = 1.5  # Width of the racetrack in nautical miles
distance = 2  # Distance of the racetrack to IP in nautical miles

racetrack = generate_racetrack(ip, tgt, speed, time_minutes, track_width, distance)
plot_racetrack(racetrack, ip, tgt)
