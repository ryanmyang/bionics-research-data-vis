import matplotlib.pyplot as plt
import matplotlib.colors as mpc
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import math_helper





####
reachable_workspace_file = "ReachableWorkspaceSpherical_01_31_2024_23_50_21_Left"
####




# JSON data
spherical_vector_list = []
with open(f"./ReachableWorkspaceData/{reachable_workspace_file}.txt") as f:
    for line in f:
        if line[0] == 'U':
            break
        floats:list = [float(f) for f in line.strip('\n\r,').split(',')]
        spherical_vector_list.append([floats[1],floats[2],floats[3]])


n = len(spherical_vector_list)
# print(spherical_vector_list)

# Rad, polar, elevation
# Convert spherical coordinates to Cartesian coordinates
radius = np.array([vector[0] for vector in spherical_vector_list])
polar_angle = np.array([vector[1] for vector in spherical_vector_list])
elevation_angle = np.array([vector[2] for vector in spherical_vector_list])
polar_angle_deg = np.rad2deg(polar_angle)
elevation_angle_deg = np.rad2deg(elevation_angle)

# Convert spherical to Cartesian coordinates
x_s = radius * np.sin(elevation_angle) * np.cos(polar_angle)
y_s = radius * np.sin(elevation_angle) * np.sin(polar_angle)
z_s = radius * np.cos(elevation_angle)


fig_s = plt.figure()
ax_s = fig_s.add_subplot(111, projection='3d')
single_max_radius = np.max(radius)
ax_s.set_xlim(-single_max_radius, single_max_radius)
ax_s.set_ylim(-single_max_radius, single_max_radius)
ax_s.set_zlim(-single_max_radius, single_max_radius)

ax_s.scatter(x_s, y_s, z_s, c='b', marker='o')
ax_s.scatter([0], [0], [0], marker='D', color='red')

####
# Drawing the axes onto the 3D graph
####
# 1. Circle
# https://stackoverflow.com/questions/56870675/how-to-do-a-3d-circle-in-matplotlib
r = max(radius) # desired radius
n = 100 # number of points for the circle
points = r*np.exp(1j*np.linspace(0, 2*np.pi, n))
u,v = np.real(points), np.imag(points)
w = np.repeat(r, n)
ax_s.plot(u,v,w-0.7, color='black')
# 2. Polar Line for 0
polar_0 = math_helper.spherical_to_cartesian(r, 0, math.pi/2)
ax_s.plot([0,polar_0[0]],[0,polar_0[1]],[0,polar_0[2]], color='black')
ax_s.text(polar_0[0]+0.05,polar_0[1],polar_0[2], "θ=0", fontsize=13)
# 3. Elevation Line for 0
elevation_0 = math_helper.spherical_to_cartesian(r, 0, 0)
ax_s.plot([0,elevation_0[0]],[0,elevation_0[1]],[0,elevation_0[2]], color='black')
# ax_s.text(elevation_0[0],elevation_0[1]+0.05,elevation_0[2], "ϕ=0")
# 4. Elevation 45
elevation_45 = math_helper.spherical_to_cartesian(r,0, math.pi/8)
ax_s.plot([0,elevation_45[0]],[0,elevation_45[1]],[0,elevation_45[2]], color='black')
# ax_s.text(elevation_45[0]+0.025,elevation_45[1],elevation_45[2]+0.05, "ϕ=22.5")
# 5. Box at 90 polar
ax_s.plot([0,0,0,0,0],[0,single_max_radius,single_max_radius,0,0],[0,0,single_max_radius,single_max_radius,0], color='red',linestyle='-')




# Set axis limits
# ax_s.set_xlim(axis_limits)
# ax_s.set_ylim(axis_limits)
# ax_s.set_zlim(axis_limits)

# Set labels
ax_s.set_xlabel('X Axis')
ax_s.set_ylabel('Y Axis')
ax_s.set_zlabel('Z Axis')
ax_s.set_aspect('equal')


# ====================================
# =========== HEAT MAP ===============
# ====================================

# print(spherical_vector_list)
# Using polar_angle, elevation_angle, max_radius
fig_heatmap, ax_heatmap = plt.subplots()
ax_heatmap.set_facecolor("lightyellow")
min_val, max_val = 0.2,1.0
n = 10
orig_cmap = plt.cm.Greys
colors = orig_cmap(np.linspace(min_val, max_val, n))
mycmap = mpc.LinearSegmentedColormap.from_list("mycmap", colors)

# Find max radius per every polar angle and elevation angle
max_radius = np.array([np.max(radius[(polar_angle_deg == pa) & (elevation_angle_deg == ea)]) for pa, ea in zip(polar_angle_deg, elevation_angle_deg)])
# print(np.shape(max_radius))
# Remove duplicate points that come from matching p & e getting assigned same max radius
max_radius_points = np.unique(np.column_stack((polar_angle_deg, elevation_angle_deg, max_radius)), axis=0)
# print(np.shape(max_radius_points))
mrp_p = max_radius_points[:, 0].tolist()
mrp_e = max_radius_points[:, 1].tolist()
mrp_r = max_radius_points[:, 2].tolist()

ax_heatmap.plot([90,90], [0, 180], color='red',linestyle='-',zorder=0,linewidth=2)
scatter = ax_heatmap.scatter(mrp_p, mrp_e, c=mrp_r, cmap=mycmap, marker='s')

ax_heatmap.set_xlabel('Polar Angle (Degrees)')
ax_heatmap.set_ylabel('Elevation Angle (Degrees)')
ax_heatmap.set_title(f"Radius, Polar Angle, Elevation Angle")
cbar = plt.colorbar(scatter, label='Maximum Radius (m)')



# ====================================
# ============ HEAT MAP 2 ============
# ====================================
# fig_heatmap2, ax_heatmap2 = plt.subplots()

# # I need to define a grid of intervals to use for each theta and phi. 
#     # One way is to basically find the smallest difference between any theta and use that as my interval, and same for any phi, and use that as the interval
# min_polar_interval = min(math.fabs(d) for d in np.diff(np.unique(polar_angle_deg)))
# min_elevation_interval = min(math.fabs(d) for d in np.diff(np.unique(elevation_angle_deg)))
# print(min_polar_interval)
# print(min_elevation_interval)

# # Create a 2D histogram
# heatmap, xedges, yedges = np.histogram2d(mrp_p, mrp_e, bins=[np.arange(0, 360+min_polar_interval, min_polar_interval), np.arange(0, 180+min_elevation_interval, min_elevation_interval)], weights=mrp_r)

# # Plot the heatmap
# ax_heatmap2.imshow(heatmap.T, extent=[0, 360, 0, 180], origin='lower', cmap=mycmap,aspect='equal')
# ax_heatmap2.set_aspect('equal',adjustable='box')

# ax_heatmap2.set_xlabel('Polar Angle (degrees)')
# ax_heatmap2.set_ylabel('Elevation Angle (degrees)')
# ax_heatmap2.set_title('Heatmap of Max Radius')




# Then create a 2D array encompassing the entire dataset, defaulting all values to 0
# Then I need to grab each max_radiuspoint I have and find the c


# ====================================
# ========== TUTORIAL PLOT ===========
# ====================================

fixed_p = 90

# Extract all points with this p

# fixed_p_spherical_bool_mask = [math.isclose(num, fixed_p, rel_tol=0.1) for num in polar_angle]
# fixed_p_spherical_bool_mask = np.array(fixed_p_spherical_bool_mask).reshape(len(fixed_p_spherical_bool_mask),3)
# tutorial_points = np.extract(fixed_p_spherical_bool_mask, spherical_vector_list)
tutorial_points = max_radius_points[np.isclose(max_radius_points[:, 0], fixed_p)]


tutorial_plot = plt.figure().add_subplot(111)
tutorial_plot.scatter(tutorial_points[:, 2], tutorial_points[:, 1],  marker='o', color='black')
tutorial_plot.set_title(f"Elevation angle vs Max Radius for fixed polar angle {fixed_p} degrees")
tutorial_plot.set_xlabel('Radius (m)')
tutorial_plot.set_ylabel('Elevation angle (degrees)')



plt.show()
