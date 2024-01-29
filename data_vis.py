import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# JSON data
with open('11_30_00_30_touched_sphere_coords_left.json') as cartesian_json_file:
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

# Create 3D scatter plot



# Load JSON data
with open('11_30_00_30_touched_sphere_polar_left.json') as spherical_json_file:
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
ax.scatter(x, z, y, c='b', marker='o')

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
# ax_s.scatter(0, 0, 0, c='r', marker='o')  # Center point
# ax_s.scatter(radius * np.sin(elevation_angle) * np.cos(polar_angle),
#              radius * np.sin(elevation_angle) * np.sin(polar_angle),
#              radius * np.cos(elevation_angle),
#              c='r', marker='o')  # Spherical axes

# Set axis limits
ax_s.set_xlim(axis_limits)
ax_s.set_ylim(axis_limits)
ax_s.set_zlim(axis_limits)

# Set labels
ax_s.set_xlabel('X Axis')
ax_s.set_ylabel('Y Axis')
ax_s.set_zlabel('Z Axis')
# Calculate maximum radius for each combination of polar and elevation angles
max_radius = np.array([np.max(radius[(polar_angle == pa) & (elevation_angle == ea)]) for pa, ea in zip(polar_angle, elevation_angle)])

# Create 2D heatmap
fig_heatmap, ax_heatmap = plt.subplots()

# Scatter plot with color representing maximum radius
scatter = ax_heatmap.scatter(polar_angle, elevation_angle, c=max_radius, cmap='viridis', marker='o')

# Set labels and colorbar
ax_heatmap.set_xlabel('Polar Angle')
ax_heatmap.set_ylabel('Elevation Angle')
cbar = plt.colorbar(scatter, label='Maximum Radius')

plt.show()

plt.show()
