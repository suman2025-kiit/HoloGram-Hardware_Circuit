import matplotlib.pyplot as plt
import numpy as np

depth_voltage = np.sin(np.linspace(0, 10, 100))
pose_voltage = np.sin(np.linspace(0, 10, 100) + 0.3)
zero_shot_error = np.abs(depth_voltage - pose_voltage)

plt.figure(figsize=(8, 5))
plt.plot(depth_voltage, label='Depth Voltage', color='cyan')
plt.plot(pose_voltage, label='Pose Voltage', color='green')
plt.plot(zero_shot_error, label='Zero-Shot Error', color='red')
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.title("HoloGram Circuit Simulation Output")
plt.legend()
plt.grid(True)
plt.savefig("outputs/zero_shot_error_plot.jpeg", dpi=300)
plt.show()