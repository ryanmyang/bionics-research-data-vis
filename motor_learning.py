import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from enum import Enum
import re

class plane(Enum):
    XY = "Frontal"
    YZ = "YZ"
    XZ = "Horizontal"

def normalize_vectors(vectors, radius):
    # Calculate the current magnitudes (lengths) of each vector
    magnitudes = np.linalg.norm(vectors, axis=1)

    # Normalize vectors to the specified radius
    normalized_vectors = vectors * (radius / magnitudes)[:, np.newaxis]

    return normalized_vectors

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
            print(self.arm)
            print(self.shoulder_pos)
            print(self.plane)
            print(self.game_radius)

            # Process the remaining lines, including last line
            last_target = -1
            for line in f:
                words = line.split(',')
                # print(words)
                # Last line check
                if len(words) < 6:
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
            
            # print(np.shape(self.times))
            # print(np.shape(self.target_set_times))
            target_set_times_times_only = [couple[1] for couple in self.target_set_times]
            # print(f"TSTTO: {target_set_times_times_only}")
            splitIndices = [np.searchsorted(self.times, t) for t in target_set_times_times_only]
            # print("SPLIT TIMES")
            # print([self.times[t] for t in splitIndices])
            # print(splitIndices)
            self.target_time_index_array = np.column_stack((self.target_set_times, splitIndices))
            # print()
            # print("target, time, index")
            # print(str(target_time_index))

            # print("done")
            # print("TIMES: " + str(self.times))
            # print(f"POSITIONS: {self.positions}")
            # print(f"TARGET SET TIMES: {self.target_set_times}")
            # print(f"SPEED SET TIMES: {self.speed_set_times}")
            self.targets = normalize_vectors(motor_learning.targets, self.game_radius)
            # print(f"TARGETS: {self.targets}")
            self.fig = plt.figure()


    def process_first_line(self, line: str):
        print("Process first line")
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
            print("PLANE")
            print(match.group(5))
            self.plane = plane[match.group(5)]
            self.game_radius = float(match.group(6))
        else:
            print("Failed to read first line")
            quit()
    
            
    def process_last_line(self, words: list[str]):
        pass
        
    def plot_2d(self):
        

        # num_ticks = 10
        x = 0
        y = 2
        x_adjust = 1
        y_adjust = 1
        match self.plane:
            case plane.XZ:
                x = 0
                y = 2
                x_adjust = -1
                y_adjust = -1
            case plane.XY:
                x = 0
                y = 1
                x_adjust = -1
                y_adjust = -1
            case plane.YZ:
                if self.arm == 'Right':
                    x = 2
                    y = 1
                    x_adjust = 1
                    y_adjust = -1
                if self.arm == 'Left':
                    x = 2
                    y = 1
                    x_adjust = -1
                    y_adjust = -1

        
        # print(x_arr)
        # print(y_arr)
        
        ax = self.fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')

        for i in range(len(self.targets)):
            ax.plot([0, self.targets[i][0]], [0,self.targets[i][1]], marker='o', linestyle='-', color='black')
            ax.annotate(str(i+1), (self.targets[i][0],self.targets[i][1]), textcoords='offset points', xytext= (-3,-4) + (self.targets[i])*30)
        ax.margins(x=0.1,y=0.1)

        split_indices = [int(i[2]) for i in self.target_time_index_array]
        split_indices.remove(0)
        split_positions = np.split(self.positions, split_indices)
        print("SPLIT INDICES")
        print(split_indices)
        print(len(self.positions))

        print("SPLIT POSITIONS")
        print(len(split_positions))

        print(split_positions)
        for i in range(len(self.target_set_times)):
            x_arr = np.array([(p[x] * x_adjust) for p in split_positions[i]])
            y_arr = np.array([(p[y] * y_adjust) for p in split_positions[i]])
            ax.plot(x_arr, y_arr, marker='.', linestyle='-', label=self.target_set_times[i][0])
        ax.legend(bbox_to_anchor=(1.2, 1))
        ax.set_title("", y=1.05, fontsize=18)
        ax.set_title(f"Position of arm for each target\n{self.arm} arm, {self.plane.value} plane", fontsize=10)     



        


if __name__ == "__main__":
    ml = motor_learning("MotorLearning_01_29_2024_19_21_21_Left_YZ_normal.txt")
    ml.plot_2d()
    plt.show()
    