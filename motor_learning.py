import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from enum import Enum
import re

class plane(Enum):
    XY = 0
    YZ = 1
    XZ = 2

class motor_learning:
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
                print(words)
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
            print("done")
            print("TIMES: " + str(self.times))
            print(f"POSITIONS: {self.positions}")
            print(f"TARGET SET TIMES: {self.target_set_times}")
            print(f"SPEED SET TIMES: {self.speed_set_times}")


    def process_first_line(self, line: str):
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
            self.plane = plane[match.group(5)]
            self.game_radius = float(match.group(6))
    
            
    def process_last_line(self, words: list[str]):
        pass
        
    def plot_2d(self):
        num_ticks = 10
        x = 0
        y = 2
        if self.plane == plane.XY:
            x = 0
            y = 2
        x_arr = np.array([i[x] for i in self.positions])
        y_arr = np.array([i[y] for i in self.positions])
        print(x_arr)
        print(y_arr)
        x_ticks = np.linspace(x_arr.min(), x_arr.max(), num_ticks, endpoint=True)
        plt.xticks(x_ticks)

        plt.plot(x_arr, y_arr, marker='o', linestyle='-', label='Positions')
        plt.show()


if __name__ == "__main__":
    ml = motor_learning("MotorLearning_01_24_2024_09_49_44_Left_XZ_normal.txt")
    ml.plot_2d()
    