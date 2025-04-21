import numpy as np
import matplotlib.pyplot as plt
import csv 
from scipy.stats import norm  

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题

def vehicle_simulation(road_length, simulation_time, mean_headway=5, std_headway=1, min_speed=10, max_speed=15, seed=None):
    if seed is not None:
        np.random.seed(seed)  
    current_time = 0
    vehicles = []
    headways = [] 
    while current_time < simulation_time:
        # 随机生成符合正态分布的车头时距，保证为正数
        while True:
            headway = np.random.normal(mean_headway, std_headway)
            if headway > 0:
                break
        headways.append(headway)
        current_time += headway  
        if current_time < simulation_time:
            speed = np.random.uniform(min_speed, max_speed)
            travel_time = road_length / speed
            leave_time = current_time + travel_time
            vehicles.append((current_time, speed, leave_time))
    return vehicles, headways

road_length = 500
simulation_time = 3600
seed = 42  
result, headways = vehicle_simulation(road_length, simulation_time, seed=seed)

print("仿真结果：")
print("车辆编号\t进入时刻 (秒)\t速度 (米/秒)\t离开时刻 (秒)")
for i, (entry_time, speed, leave_time) in enumerate(result):
    print(f"{i + 1}\t\t{entry_time:.2f}\t\t{speed:.2f}\t\t{leave_time:.2f}")

print(f"车头时距数据基本统计信息：\n最小值: {np.min(headways)}\n最大值: {np.max(headways)}\n均值: {np.mean(headways)}\n标准差: {np.std(headways)}")

# 保存仿真结果到CSV文件
with open("out/1/simulation_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["车辆编号", "进入时刻 (秒)", "速度 (米/秒)", "离开时刻 (秒)", "停留时间"])
    for i, (entry_time, speed, leave_time) in enumerate(result):
        writer.writerow([i + 1, f"{entry_time:.2f}", f"{speed:.2f}", f"{leave_time:.2f}", f"{leave_time - entry_time:.2f}"])

with open("out/1/headways_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["车头时距 (秒)"])
    writer.writerows([[headway] for headway in headways])

plt.hist(headways, bins=30, density=True, alpha=0.7, color='skyblue', label='车头时距直方图')

mean = np.mean(headways)  # 计算车头时距的均值
std = np.std(headways)    # 计算车头时距的标准差
x = np.linspace(min(headways), max(headways), 1000)  # 在车头时距范围内生成点
pdf = norm.pdf(x, mean, std)  # 计算正态分布的概率密度函数

plt.plot(x, pdf, 'r-', label='标准正态分布曲线')

plt.title('车头时距的正态分布')
plt.xlabel('车头时距 (秒)')
plt.ylabel('概率密度')
plt.legend()
plt.grid(True)

plt.savefig('out/1/headway_distribution_with_normal_curve.png')
plt.show()

speeds = [vehicle[1] for vehicle in result]  # 提取所有车辆的速度
plt.hist(speeds, bins=20, color='orange', edgecolor='black', alpha=0.7, label='速度频率分布')

plt.title('车辆速度频率分布图')
plt.xlabel('速度 (米/秒)')
plt.ylabel('频率')
plt.legend()
plt.grid(True)

plt.savefig('out/1/speed_frequency_distribution.png')
plt.show()
