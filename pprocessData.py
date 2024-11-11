import csv
import math

# 读取CSV文件并处理数据
file_csv = 'toright1.csv'
filtered_data = []

time_first = -1.0
X_first = -1.0
Y_first = -1.0
slide_window_interval = 3  # 每隔3个点计算一次速度
time_to_diff = 0
window_size = 3  # 滑动窗口大小
data_window = []  # 存储速度以用于滑动窗口平均

with open(file_csv, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    previous_row = None
    SOG = 0  # 当前速度值
    speed_counter = 0  # 计数器，用于确定是否需要重新计算速度

    # rows = list(reader)  # 将所有行读取到列表中
    # n_rows = len(rows)
    # for i in range(n_rows):
    #     row = rows[i]
    for row in reader:
        time = float(row['Time'])
        X = float(row['X'])
        Y = float(row['Y'])

        if time_first < 0:
            time_first = time
            X_first = X
            Y_first = Y
        # 计算时间相对于初始时间的秒数
        time -= time_first
        X -= X_first
        Y -= Y_first
        # if(i == 0): #只执行一次
        data_window.append((X, Y, time))

        if speed_counter >= slide_window_interval:
            # 计算时间差（秒）
            time_diff_seconds = time - data_window[0][2]
            # 计算位移距离（米）
            distance = math.sqrt((X - data_window[0][0]) **2 + (Y - data_window[0][1]) **2)
            # 计算瞬时速度（米/秒）
            SOG = distance / time_diff_seconds
            # speed_counter = 0  # 重置计数器
            # time_to_diff = time
            # data_window.clear()
            # data_window.append((X, Y, time))
            # for i in range(3):
            del data_window[0]
        else:
            speed_counter += 1

        # 维护滑动窗口的大小
        if len(data_window) > window_size:
            data_window.pop(0)

        # 构建新行
        new_row = {
            'Time': time,
            'COG': row['COG'],
            'Lon': row['Lon'],
            'Lat': row['Lat'],
            'X': X,
            'Y': Y,
            'SOG': SOG,
            'Type': 'OS'
        }
        filtered_data.append(new_row)


# 如果需要保存到新的CSV文件
with open('filtered_'+file_csv, mode='w', newline='') as file:
    fieldnames = ['Time', 'COG', 'Lon', 'Lat', 'X', 'Y', 'SOG','Type']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered_data)
