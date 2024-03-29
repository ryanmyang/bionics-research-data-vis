import json
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

# JSON data
with open('./old/11_30_00_30_touched_sphere_coords_left.json') as cartesian_json_file:
    cartesian_data = json.load(cartesian_json_file)

# Extract vectorList from the data
cartesian_vector_list = cartesian_data['vectorList']

# Separate x, y, and z coordinates
x = np.array([vector['x'] for vector in cartesian_vector_list])
y = np.array([vector['y'] for vector in cartesian_vector_list])
z = np.array([vector['z'] for vector in cartesian_vector_list])

# Define overall size and step size
overall_size = 0.8
step_size = 0.1

# Adjust axis limits
axis_limits = (-overall_size, overall_size)

# Load JSON data
with open('./old/11_30_00_30_touched_sphere_polar_left.json') as spherical_json_file:
    spherical_data = json.load(spherical_json_file)

# Extract vectorList from the data
spherical_vector_list = spherical_data['vectorList']

# Convert spherical coordinates to Cartesian coordinates
radius = np.array([vector['x'] for vector in spherical_vector_list])
polar_angle = np.array([vector['y'] for vector in spherical_vector_list])
elevation_angle = np.array([vector['z'] for vector in spherical_vector_list])

# Convert spherical to Cartesian coordinates
x_s = radius * np.sin(elevation_angle) * np.cos(polar_angle)
y_s = radius * np.sin(elevation_angle) * np.sin(polar_angle)
z_s = radius * np.cos(elevation_angle)


# Create 3D scatter plot
fig_c = plt.figure()

ax = fig_c.add_subplot(111, projection='3d')
ax.scatter(x, z, y, marker='o',color='blue')
ax.scatter([0], [0], [0], marker='D', color='red')

# Set axis limits
ax.set_xlim(axis_limits)
ax.set_ylim(axis_limits)
ax.set_zlim(axis_limits)

# Set labels
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

fig_s = plt.figure()
ax_s = fig_s.add_subplot(111, projection='3d')
ax_s.scatter(x_s, y_s, z_s, c='b', marker='o')
ax_s.scatter([0], [0], [0], marker='D', color='red')


# Set axis limits
ax_s.set_xlim(axis_limits)
ax_s.set_ylim(axis_limits)
ax_s.set_zlim(axis_limits)

# Set labels
ax_s.set_xlabel('X Axis')
ax_s.set_ylabel('Y Axis')
ax_s.set_zlabel('Z Axis')


# ====================================
# =========== HEAT MAP ===============
# ====================================

# Using polar_angle, elevation_angle, max_radius
fig_heatmap, ax_heatmap = plt.subplots()
ax_heatmap.set_facecolor("lightyellow")
min_val, max_val = 0.2,1.0
n = 10
orig_cmap = plt.cm.Greys
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = mpc.LinearSegmentedColormap.from_list("mycmap", colors)

# Find max radius per every polar angle and elevation angle
max_radius = np.array([np.max(radius[(polar_angle == pa) & (elevation_angle == ea)]) for pa, ea in zip(polar_angle, elevation_angle)])
scatter = ax_heatmap.scatter(polar_angle, elevation_angle, c=max_radius, cmap=cmap, marker='.')


ax_heatmap.set_xlabel('Polar Angle')
ax_heatmap.set_ylabel('Elevation Angle')
cbar = plt.colorbar(scatter, label='Maximum Radius')

# ====================================
# ========== TUTORIAL PLOT ===========
# ====================================

fixed_p = 1.57
# Extract all points with this p

fixed_p_spherical_bool_mask = [math.isclose(num, fixed_p, rel_tol=0.1) for num in polar_angle]
tutorial_points = np.extract(fixed_p_spherical_bool_mask, spherical_vector_list)

print(tutorial_points)

tutorial_plot = plt.figure().add_subplot(111)
radius_tut = np.array([vector['x'] for vector in tutorial_points])
elevation_angle_tut = np.array([vector['z'] for vector in tutorial_points])
tutorial_plot.scatter(radius_tut, elevation_angle_tut,  marker='o', color='black')
tutorial_plot.set_title(f"Elevation angle vs Radius for fixed polar angle {fixed_p} radians")
tutorial_plot.set_xlabel('Radius (m)')
tutorial_plot.set_ylabel('Elevation angle (radians)')



plt.show()
