import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决符号显示问题
# GHR跟驰模型参数
c = 0.5  # 灵敏度参数
m = 1  # 速度指数
l = 1  # 间距指数

# 随机生成初始参数
np.random.seed()
initial_distance = round(np.random.uniform(10, 50), 2) # 初始间距(米)
front_initial_speed = round(np.random.uniform(10, 20),2)  # 前车初始速度(米/秒)
rear_initial_speed = round(np.random.uniform(10, 20), 2)  # 后车初始速度(米/秒)
front_acceleration = round(np.random.uniform(0.5, 2),2)  # 前车加速度(米/秒²)
reaction_time = round(np.random.uniform(0.5, 2),2 )  # 后车反应时间(秒)

# 仿真参数
simulation_time = 10  # 总仿真时间(秒)
dt = 0.01  # 时间步长(秒)
steps = int(simulation_time / dt)

# 初始化数组
front_position = []
rear_position = []
front_speed = []
rear_speed = []
rear_acceleration = []

# 设置初始条件
front_position.append(0)
rear_position.append(-initial_distance)
front_speed.append(front_initial_speed)
rear_speed.append(rear_initial_speed)
rear_acceleration.append(0)  

print("初始参数:")
print(f"前车初始速度: {front_initial_speed:.2f} 米/秒")
print(f"后车初始速度: {rear_initial_speed:.2f} 米/秒")
print(f"初始间距: {initial_distance:.2f} 米")
print(f"前车加速度: {front_acceleration:.2f} 米/秒²")
print(f"后车反应时间: {reaction_time:.2f} 秒")
print(f"时间 0.00 秒，后车位置 {rear_position[-1]:.2f}, 前车位置 {front_position[-1]:.2f}, 后车速度 {rear_speed[-1]:.2f}, 前车速度 {front_speed[-1]:.2f},前车加速度{front_acceleration:.2f},后车加速度 {rear_acceleration[-1]:.2f}")

# 仿真循环
for i in range(1, steps+1):
    # 后车运动加速度计算 (GHR模型)
    if i > int(reaction_time / dt):  # 考虑反应时间
        distance = front_position[i-1] - rear_position[i-1]
        speed_diff = front_speed[i-1] - rear_speed[i-1]
        # GHR模型计算后车加速度
        rear_acceleration.append(c * (rear_speed[i-1]**m) * (speed_diff) / (distance**l))
    else:
        rear_acceleration.append(0)
    #前车运动
    front_speed.append(front_speed[i-1] + front_acceleration * dt)
    front_position.append(front_position[i-1] + front_speed[i-1] * dt+0.5*front_acceleration*(dt**2))
    #后车运动
    rear_speed.append(rear_speed[i-1] + rear_acceleration[i-1] * dt)
    rear_position.append(rear_position[i-1] + rear_speed[i-1] * dt+0.5*rear_acceleration[i-1]*(dt**2))
    # 碰撞判断
    if rear_position[i] > front_position[i]:
        print(f"碰撞发生在时间 {i * dt:.2f} 秒，后车位置 {rear_position[i]:.2f} 米")
        break  # 碰撞发生，停止仿真
    print(f"时间 {i * dt:.2f} 秒,后车位置 {rear_position[i]:.2f},前车位置 {front_position[i]:.2f},后车速度 {rear_speed[i]:.2f},前车速度 {front_speed[i]:.2f},前车加速度{front_acceleration:.2f},后车加速度 {rear_acceleration[i]:.2f},两车间距{front_position[i]-rear_position[i]:.2f}")

# 输出结果
print("初始参数:")
print(f"前车初始速度: {front_initial_speed:.2f} 米/秒")
print(f"后车初始速度: {rear_initial_speed:.2f} 米/秒")
print(f"初始间距: {initial_distance:.2f} 米")
print(f"前车加速度: {front_acceleration:.2f} 米/秒²")
print(f"后车反应时间: {reaction_time:.2f} 秒")
print(f"最后时刻后车加速度: {rear_acceleration[-1]:.2f} 米/秒^2")
print(f"最后时刻前车位置: {front_position[-1]:.2f} 米")
print(f"最后时刻后车位置: {rear_position[-1]:.2f} 米")

# 绘制结果
plt.figure(figsize=(14, 10))
plt.suptitle('GHR跟驰模型仿真结果', fontsize=16, y=1.02)

# 位置图
plt.subplot(3, 1, 1)
time_points = np.arange(0, len(front_position)*dt, dt)
plt.plot(time_points[:len(front_position)], front_position, label='前车', linewidth=2)
plt.plot(time_points[:len(rear_position)], rear_position, label='后车', linewidth=2)
plt.ylabel('位置 (米)', fontsize=12)
plt.title('车辆位置随时间变化', fontsize=14, pad=20)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# 添加参数文本框
param_text = f'初始参数:\n前车速度: {front_initial_speed:.2f} m/s\n后车速度: {rear_initial_speed:.2f} m/s\n初始间距: {initial_distance:.2f} m\n前车加速度: {front_acceleration:.2f} m/s^2\n反应时间: {reaction_time:.2f} s'
plt.text(0.02, 0.98, param_text, transform=plt.gca().transAxes,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=10)

# 速度图
plt.subplot(3, 1, 2)
plt.plot(time_points[:len(front_speed)], front_speed, label='前车', linewidth=2)
plt.plot(time_points[:len(rear_speed)], rear_speed, label='后车', linewidth=2)
plt.ylabel('速度 (米/秒)', fontsize=12)
plt.title('车辆速度随时间变化', fontsize=14, pad=20)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# 添加模型参数文本框
model_text = f'GHR模型参数:\n灵敏度: {c}\n速度指数: {m}\n间距指数: {l}'
plt.text(0.02, 0.98, model_text, transform=plt.gca().transAxes,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=10)

# 加速度图
plt.subplot(3, 1, 3)
plt.plot(time_points[:len(rear_acceleration)], rear_acceleration, linewidth=2)
plt.xlabel('时间 (秒)', fontsize=12)
plt.ylabel('加速度 (米/秒^2)', fontsize=12)
plt.title('后车加速度随时间变化', fontsize=14, pad=20)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.tight_layout()
plt.savefig('out/2/car_following_simulation.png', dpi=500 , bbox_inches='tight')
plt.show()

# 保存仿真结果到CSV文件
import csv
with open("out/2/simulation_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["时间 (秒)", "前车位置 (米)", "后车位置 (米)", "前车速度 (米/秒)", "后车速度 (米/秒)", "后车加速度 (米/秒²)","两车间距"])
    for i in range(len(front_position)):
        writer.writerow([
            f"{i * dt:.2f}",
            f"{front_position[i]:.2f}",
            f"{rear_position[i]:.2f}",
            f"{front_speed[i]:.2f}",
            f"{rear_speed[i]:.2f}",
            f"{rear_acceleration[i]:.2f}" if i < len(rear_acceleration) else "0.00",
            f"{front_position[i] - rear_position[i]:.2f}"
        ])