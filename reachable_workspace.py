import matplotlib.pyplot as plt
import matplotlib.colors as mpc
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math





####
reachable_workspace_file = "ReachableWorkspaceSpherical_01_31_2024_14_31_02"
####




# JSON data
spherical_vector_list = []
with open(f"./ReachableWorkspaceData/{reachable_workspace_file}.txt") as f:
    for line in f:
        floats:list = [float(f) for f in line.strip('\n\r,').split(',')]
        spherical_vector_list.append([floats[1],floats[2],floats[3]])

n = len(spherical_vector_list)
# print(spherical_vector_list)

# Rad, polar, elevation
# Convert spherical coordinates to Cartesian coordinates
radius = np.array([vector[0] for vector in spherical_vector_list])
polar_angle = np.array([vector[1] for vector in spherical_vector_list])
elevation_angle = np.array([vector[2] for vector in spherical_vector_list])

# Convert spherical to Cartesian coordinates
x_s = radius * np.sin(elevation_angle) * np.cos(polar_angle)
y_s = radius * np.sin(elevation_angle) * np.sin(polar_angle)
z_s = radius * np.cos(elevation_angle)


fig_s = plt.figure()
ax_s = fig_s.add_subplot(111, projection='3d')
ax_s.scatter(x_s, y_s, z_s, c='b', marker='o')
ax_s.scatter([0], [0], [0], marker='D', color='red')


# Set axis limits
# ax_s.set_xlim(axis_limits)
# ax_s.set_ylim(axis_limits)
# ax_s.set_zlim(axis_limits)

# Set labels
ax_s.set_xlabel('X Axis')
ax_s.set_ylabel('Y Axis')
ax_s.set_zlabel('Z Axis')


# ====================================
# =========== HEAT MAP ===============
# ====================================

print(spherical_vector_list)
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
float_tolerance = 0.05
# Extract all points with this p

# fixed_p_spherical_bool_mask = [math.isclose(num, fixed_p, rel_tol=0.1) for num in polar_angle]
# fixed_p_spherical_bool_mask = np.array(fixed_p_spherical_bool_mask).reshape(len(fixed_p_spherical_bool_mask),3)
# tutorial_points = np.extract(fixed_p_spherical_bool_mask, spherical_vector_list)
tutorial_points = []
for point in spherical_vector_list:
    if math.isclose(point[1], fixed_p, rel_tol=0.05):
        tutorial_points.append(point)
print(spherical_vector_list)
# print(tutorial_points)

tutorial_plot = plt.figure().add_subplot(111)
radius_tut = np.array([vector[0] for vector in tutorial_points])
elevation_angle_tut = np.array([vector[2] for vector in tutorial_points])
tutorial_plot.scatter(radius_tut, elevation_angle_tut,  marker='o', color='black')
tutorial_plot.set_title(f"Elevation angle vs Radius for fixed polar angle {fixed_p} radians")
tutorial_plot.set_xlabel('Radius (m)')
tutorial_plot.set_ylabel('Elevation angle (radians)')



plt.show()
