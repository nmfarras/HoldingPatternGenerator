import numpy as np
import matplotlib.pyplot as plt

def generate_racetrack(ip, tgt, speed, time_minutes, track_width):
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
    
    # Calculate the vector from IP to TGT
    vec_ip_tgt = np.array([tgt[0] - ip[0], tgt[1] - ip[1]])
    vec_ip_tgt_norm = vec_ip_tgt / np.linalg.norm(vec_ip_tgt)
    
    # Perpendicular vector to IP-TGT (rotate by 90 degrees)
    perp_vec = np.array([-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]])
    
    # Calculate the center points of the semicircles
    center_1 = np.array(tgt) + perp_vec * track_width / 2
    center_2 = np.array(tgt) - perp_vec * track_width / 2
    
    # Calculate the points for the straight legs
    # start_leg_1 = center_1 + vec_ip_tgt_norm * leg_length / 2
    # end_leg_1 = center_2 + vec_ip_tgt_norm * leg_length / 2
    
    # start_leg_2 = center_1 - vec_ip_tgt_norm * leg_length / 2
    # end_leg_2 = center_2 - vec_ip_tgt_norm * leg_length / 2
    
    # Calculate the points for the semicircles
    theta = np.linspace(0, np.pi, 100)
    
    semicircle_1 = np.array([center_1[0] + (track_width / 2) * np.cos(theta),
                             center_1[1] + (track_width / 2) * np.sin(theta)]).T
    semicircle_1 = (semicircle_1 - center_1) @ np.array([[vec_ip_tgt_norm[0], vec_ip_tgt_norm[1]],
                                                         [-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]]]) + center_1
    
    semicircle_2 = np.array([center_2[0] + (track_width / 2) * np.cos(theta + np.pi),
                             center_2[1] + (track_width / 2) * np.sin(theta + np.pi)]).T
    semicircle_2 = (semicircle_2 - center_2) @ np.array([[vec_ip_tgt_norm[0], vec_ip_tgt_norm[1]],
                                                         [-vec_ip_tgt_norm[1], vec_ip_tgt_norm[0]]]) + center_2
    
    
    # Calculate the points for the straight legs
    start_leg_1 = semicircle_1[-1]
    end_leg_1 = semicircle_2[0]
    
    start_leg_2 =semicircle_2[-1]
    end_leg_2 =semicircle_1[0]
    
    # Combine points into the racetrack
    racetrack_points = {
        'leg_1': [start_leg_1, end_leg_1],
        'semicircle_1': semicircle_1,
        'leg_2': [start_leg_2, end_leg_2],
        'semicircle_2': semicircle_2
    }
    
    return racetrack_points

def plot_racetrack(racetrack_points):
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
track_width = 1.5  # Width of the racetrack

racetrack = generate_racetrack(ip, tgt, speed, time_minutes, track_width)
plot_racetrack(racetrack)
