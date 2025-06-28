
import numpy as np
import matplotlib.pyplot as plt

time = np.linspace(0, 1, 500)
pose_voltage = np.sin(2 * np.pi * 3 * time) + 0.1 * np.random.randn(500)
depth_voltage = np.cos(2 * np.pi * 3 * time) + 0.1 * np.random.randn(500)

threshold = 0.8
zero_shot_error = np.abs(pose_voltage - depth_voltage) > threshold

plt.figure(figsize=(10, 5))
plt.plot(time, pose_voltage, label='Pose Voltage', color='green')
plt.plot(time, depth_voltage, label='Depth Voltage', color='blue')
plt.fill_between(time, -1.5, 1.5, where=zero_shot_error, color='red', alpha=0.3, label='Zero-Shot Error')
plt.title('Zero-Shot Error Detection in HoloGram Circuit')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/HoloGram_Hardware_Circuit/code/zero_shot_error_output.jpg")
plt.show()
