"""This modules provides functions for calculating projectile trajectories"""

import numpy as np

def calculate_initial_conditions(r, rho_proj, angle):
    """Calculate initial conditions of launch
    
    Args:
        r: projectile radius
        rho_proj: projectile density
        angle: launch angle
    returns:
        A: frontal area
        theta: launch angle in radians
        proj_mass: projectile mass
    """
    A = np.pi * r**2 # Calculate frontal area
    theta = np.radians(angle) # angle to radians
    proj_vol = 4/3 * np.pi * r**3 # projectile volume
    proj_mass = rho_proj * proj_vol # projectile mass
    return A, theta, proj_mass

def calculate_acceleration(proj_mass, rho_air, v0_x, v0_y, Cd, A):
    """Calculate projectile acceleration
    
    Args: 
        proj_mass: projectile mass
        rho_air: air density
        v0_x: initial x velocity
        v0_y: initial y velocity
        Cd: drag coefficient
        A: frontal area of projectile

    Returns:
        ax: x acceleration
        ay: y acceleration
    """
    g = 9.81 # m/s^2
    v_mag = np.sqrt(v0_x**2 + v0_y**2)
    F_drag = 0.5 * rho_air * v_mag**2 * Cd * A

    Fx = -F_drag * (v_mag / v0_x)
    Fy = -F_drag * (v_mag / v0_y)

    ax = Fx / proj_mass
    ay = (Fy / proj_mass) - g

    return ax, ay

def calculate_trajectory(proj_mass, v0, A, theta, dt = 0.001, x=0, y=0, rho_air=1.225, Cd=0.47):
    """Calculate projectile trajectory
    
    Args:
        proj_mass: projectile mass
        v0: initial velocity
        A: frontal area of projectile
        theta: launch angle in radians
        dt: time step
        x: initial x position
        y: initial y position
        rho_air: air density
        Cd: drag coefficient

    Returns:
        time: list of times
        x_positions: list of x positions
        y_positions: list of y positions
    """
    # Calculate velocity components
    v0_x = v0 * np.cos(theta)
    v0_y = v0 * np.sin(theta)
    
    x_positions = []
    y_positions = []
    t= 0
    while y >= 0:
        # Calculate drag
        ax, ay = calculate_acceleration(proj_mass, rho_air, v0_x, v0_y, Cd, A)

        # Update velocity
        v0_x = v0_x + ax * dt
        v0_y = v0_y + ay * dt

        # Update position
        x += v0_x * dt
        y += v0_y * dt
        t += dt
        x_positions.append(x)
        y_positions.append(y)

    print(f"Total flight time: {t} seconds")
    print(f"Total distance: {x} metres")
    return x_positions, y_positions