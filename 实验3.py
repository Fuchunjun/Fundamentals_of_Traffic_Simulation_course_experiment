import numpy as np
import csv
import matplotlib.pyplot as plt

# 设置随机种子
np.random.seed(42)

# 仿真参数
num_vehicles = 100  # 车辆数量
mean_headway = 8  # 负指数分布参数
max_service_time = 10  # 最大服务时间
min_service_time = 5  # 最小服务时间

# 初始化变量
arrival_times = []
inter_arrival_times = []
service_times = []
waiting_times = []
leave_times = []

# 生成随机数
current_time = 0
for _ in range(num_vehicles):
    # 生成符合负指数分布的车头时距
    inter_arrival = round(np.random.exponential(mean_headway), 2)
    inter_arrival_times.append(inter_arrival)
    current_time += inter_arrival
    arrival_times.append(round(current_time,2))

    service_time = round(np.random.uniform(min_service_time, max_service_time),2)
    service_times.append(service_time)

# 计算等待时间和离开时间
last_leave_time = 0
for i in range(num_vehicles):
    if arrival_times[i] < last_leave_time:
        waiting_times.append(round(last_leave_time - arrival_times[i],2))
        leave_times.append(round(last_leave_time + service_times[i],2))
    else:
        waiting_times.append(0)
        leave_times.append(round(arrival_times[i] + service_times[i],2))
    last_leave_time = leave_times[i]

# 计算平均服务时间和平均等待时间
average_service_time = np.mean(service_times)
average_waiting_time = np.mean(waiting_times)

# 输出结果到CSV文件
with open('out/3/traffic_simulation_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['车辆编号', '到达时刻', '等待时间', '服务时间', '离开时间'])
    for i in range(num_vehicles):
        writer.writerow([i + 1, arrival_times[i], waiting_times[i], service_times[i], leave_times[i]])
    writer.writerow(['队列平均服务时间', '', '', '', average_service_time])
    writer.writerow(['队列平均等待时间', '', '', '', average_waiting_time])
    # 计算平均车头时距
    average_headway = np.mean(inter_arrival_times)
    writer.writerow(['队列平均车头时距', '', '', '', average_headway])

# 设置中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决符号显示问题

# 绘制车头时距频率分布图
plt.figure()
plt.grid(True)
plt.hist(inter_arrival_times, bins=30,alpha = 0.7,color='skyblue', edgecolor='black')
plt.title('车头时距频率分布图')
plt.xlabel('车头时距')
plt.ylabel('频率')
# 计算标准负指数分布的概率密度函数
x = np.linspace(0, max(inter_arrival_times), 1000)
y = (1/mean_headway) * np.exp(-x/mean_headway)
# 叠加标准负指数分布图像
plt.plot(x, y * len(inter_arrival_times) * (max(inter_arrival_times) - min(inter_arrival_times)) / 20, 'r-', label='负指数分布')
plt.legend()
plt.savefig('out/3/inter_arrival_times_distribution.png', dpi = 500)

# 绘制服务时长频率分布图
plt.figure()
plt.grid(True)
plt.hist(service_times, bins=20, alpha = 0.7,color='skyblue',edgecolor='black')
plt.title('服务时长频率分布图')
plt.xlabel('服务时长')
plt.ylabel('频率')
plt.savefig('out/3/service_times_distribution.png',dpi = 500)
print('结束')