import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from enum import Enum
import re
import math
from math_helper import normalize_vectors, pnt2line, distance


# ====================================
# ======== Filename at Bottom ========
# ====================================




class plane(Enum):
    XY = "Frontal"
    YZ = "Sagittal"
    XZ = "Horizontal"


class motor_learning:
    targets = np.array([[0.0,1.0], [1.0,1.0], [1.0, 0.0], [1.0, -1.0], [0.0,-1.0], [-1.0, -1.0], [-1.0, 0.0], [-1.0, 1.0]])
    def __init__(self, filename: str) -> None:
        with open(f"./MotorLearningData/{filename}") as f:
            first_line = f.readline()
            self.arm = None
            self.shoulder_pos = []
            self.plane: plane = None
            self.game_radius = 0

            
            # Array of tuples
            self.times = []
            self.positions = []
            self.target_set_times = []
            self.speed_set_times = []
            
    
            # Process the first line differently
            self.process_first_line(first_line)
            # Process the remaining lines, including last line
            last_target = -1
            for line in f:
                words = line.split(',')
                # print(words)
                # Last line check
                if words[0][0] == 't':
                    self.process_last_line(words)
                    break
                # Normal line processing:
                time: float = float(words[0])
                target: int = int(words[1])
                speed: str = words[2]
                pos: list[str] = [float(words[3]),float(words[4]),float(words[5])]
                # a) Add time
                self.times.append(time)
                self.positions.append(pos)
                # b) Check target is the same set time
                if (self.target_set_times[-1][0] if self.target_set_times else -1) != target:
                    # If diff, record that and change
                    self.target_set_times.append([target, time])
                last_speed = (self.speed_set_times[-1][0] if self.speed_set_times else "eee")
                if  last_speed != speed:
                    # If diff, record that and change
                    self.speed_set_times.append([speed, time])
            
        target_set_times_times_only = [couple[1] for couple in self.target_set_times]
        # print(f"TSTTO: {target_set_times_times_only}")
        splitIndices = [np.searchsorted(self.times, t) for t in target_set_times_times_only]
        
        self.target_time_index_array = np.column_stack((self.target_set_times, splitIndices))
        
        self.targets = normalize_vectors(motor_learning.targets, self.game_radius)
        # print(f"TARGETS: {self.targets}")    

        self.x = 0
        self.y = 2
        self.x_adjust = 1
        self.y_adjust = 1
        match self.plane:
            case plane.XZ:
                self.x = 0
                self.y = 2
                self.x_adjust = -1
                self.y_adjust = -1
            case plane.XY:
                self.x = 0
                self.y = 1
                self.x_adjust = -1
                self.y_adjust = -1
            case plane.YZ:
                if self.arm == 'Right':
                    self.x = 2
                    self.y = 1
                    self.x_adjust = 1
                    self.y_adjust = -1
                if self.arm == 'Left':
                    self.x = 2
                    self.y = 1
                    self.x_adjust = -1
                    self.y_adjust = -1
        
        self.fig = plt.figure(figsize=(10, 6), dpi=80)


    def process_first_line(self, line: str):
        # print("Process first line")
        pattern = r"(\w+),ShoulderPos:\(([-\d.]+), ([-\d.]+), ([-\d.]+)\),Plane:(\w+),Radius:([\d.]+)"
        # Use re.match to find matches in the string
        match = re.match(pattern, line)

        if match:
            # Extract information from the match groups
            self.arm = match.group(1)
            x_pos = float(match.group(2))
            y_pos = float(match.group(3))
            z_pos = float(match.group(4))
            self.shoulder_pos = np.array([x_pos, y_pos, z_pos])
            # print("PLANE")
            # print(match.group(5))
            self.plane = plane[match.group(5)]
            self.game_radius = float(match.group(6))
        else:
            print("Failed to read first line")
            quit()
    
            
    def process_last_line(self, words: list[str]):
        pass

    def calculate_average_velocity(self) -> int:
        # 1. Store all the differences
        position_diffs = np.diff(self.positions, axis=0)
        # 2. Find all the distances by norming each vector
        euclidean_distances = np.linalg.norm(position_diffs, axis=1)
        # 3. Sum to get the distance, and divide by time diff in secs
        time_diff = self.times[-1] - self.times[0]
        return sum(euclidean_distances)/time_diff
    
    def calculate_max_velocity(self) -> int:
        # 1. Store all the differences
        position_diffs = np.diff(self.positions, axis=0)
        # 2. Find all the distances by norming each vector
        euclidean_distances = np.linalg.norm(position_diffs, axis=1)
        # 3. Find all time diffs
        time_diffs = np.diff(self.times)
        all_instant_velocities = euclidean_distances/time_diffs
        return max(all_instant_velocities)

        
    def plot_2d(self) -> None:
        # Adjust 2D portions and flipping based on plane used for data collection
        
        # Initialize Plot 
        ax = self.fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        ax.margins(x=0.1,y=0.1)
        ax.set_title(f"Position of arm for each target\n{self.arm} arm, {self.plane.value} plane, {self.speed_set_times[0][0]} speed", fontsize=10)

        # Plot targets
        for i in range(len(self.targets)):
            ax.plot([0, self.targets[i][0]], [0,self.targets[i][1]], marker='o', linestyle='-', color='black')
            ax.annotate(str(i+1), (self.targets[i][0],self.targets[i][1]), textcoords='offset points', xytext= (-3,-4) + (self.targets[i])*30)

        # Split positions into target sections based on target times
        split_indices = [int(i[2]) for i in self.target_time_index_array]
        split_indices.remove(0)
        split_positions = np.split(self.positions, split_indices)

        # print("SPLIT INDICES")
        # print(split_indices)
        # print(len(self.positions))
        # print("SPLIT POSITIONS")
        # print(len(split_positions))
        # print(split_positions)
        RMSD_caption = "RMSD per target"
        # Plot all positions by iterating through the split positions
        for i in range(len(self.target_set_times)):
            curr_target = self.target_set_times[i][0]
            x_arr = np.array([(p[self.x] * self.x_adjust) for p in split_positions[i]])
            y_arr = np.array([(p[self.y] * self.y_adjust) for p in split_positions[i]])
            ax.plot(x_arr, y_arr, marker='.', linestyle='-', label=curr_target)

            # print("Target" + str(curr_target))
            # print(list(self.targets[curr_target-1]) +[0])

            # Calculate distances
            target_distances = []
            for j in range(len(x_arr)):
                distance = pnt2line([x_arr[j],y_arr[j],0], [0,0,0], list(self.targets[curr_target-1]) +[0])[0]
                target_distances.append(distance)
            # print(f"target distances : {target_distances}")

            distances_squared = [(d ** 2) for d in target_distances]
            # print(f"Distances squared: {distances_squared}")
            # print(f"Max in distance square sum: {max(distances_squared)}")
            distance_square_sum = sum(distances_squared)
            # print(f"Distance square sum: {distance_square_sum}")
            # print(f"Split positions size for target: {len(split_positions[i])}")
            rmsd = math.sqrt(distance_square_sum/len(target_distances))
            RMSD_caption += f"\nTarget {curr_target}: {'{:.3f}'.format(rmsd)}"
            # print(f"The RMSD for target {curr_target} is {rmsd}")
            
        ax.text(-0.45, 0, RMSD_caption, wrap=True, horizontalalignment='right', fontsize=8)
        ax.legend(bbox_to_anchor=(1.2, 1))
        plt.show()
             


if __name__ == "__main__":
    ml = motor_learning("MotorLearning_01_31_2024_17_41_34_Left_XZ_fast.txt")
    print(f"AVERAGE VELOCITY: {ml.calculate_average_velocity()}")
    print(f"MAX VELOCITY: {ml.calculate_max_velocity()}")
    
    ml.plot_2d()
