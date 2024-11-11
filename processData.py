import csv
from datetime import datetime, timedelta
import gps2xy
import math
# 定义时间格式
time_format = "%Y-%m-%d %H:%M:%S:%f"

# 指定时间范围
start_time = datetime.strptime("2024-11-06 02:41:00:804", time_format)
end_time = start_time + timedelta(minutes=1, seconds=30)
# 定义经纬度的有效范围
valid_longitude_range = (-180.0, 180.0)
valid_latitude_range = (-90.0, 90.0)

# 定义距离阈值（单位：米）
distance_threshold = 30  # 例如，1000米

# 定义一个函数来计算两点之间的Haversine距离
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球半径，单位：米
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# 读取CSV文件并处理数据
file_csv = '2024-11-06--04_32_04-LandTerminal.csv'
filtered_data = []
X_first = -1.0
Y_first = -1.0
prev_lat = None
prev_lon = None

with open(file_csv, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # 解析时间

        time_str = row['Time']
        time_obj = datetime.strptime(time_str, time_format)


        # 检查时间是否在指定范围内
        # if start_time <= time_obj <= end_time:
        # 解析经纬度
        try:
            lat = float(row['longitude'])
            lon = float(row['latitude'])
        except ValueError:
            continue  # 跳过无效的经纬度
        # 检查与前一个点的距离
        if prev_lat is not None and prev_lon is not None:
            distance = haversine_distance(prev_lat, prev_lon, lat, lon)
            if distance > distance_threshold:
                continue  # 跳过距离过远的点
        X, Y = gps2xy.WGS84ToWebMercator_Single(lat, lon)
        if(X_first < 0):
            X_first = X
            Y_first = Y
            time_first = time_obj
        X -= X_first
        Y -= Y_first
        # 计算时间相对于初始时间的秒数
        time_diff_seconds = (time_obj - time_first).total_seconds()
        # 构建新行
        new_row = {
            'Time': time_diff_seconds,
            'COG': row['heading'],
            'Lon': lon,
            'Lat': lat,
            'X': X,
            'Y': Y,
            'Type': 'OS'
        }
        filtered_data.append(new_row)
        # 更新前一个点的经纬度
        prev_lat = lat
        prev_lon = lon


# 如果需要保存到新的CSV文件
with open('filtered'+file_csv, mode='w', newline='') as file:
    fieldnames = ['Time', 'COG', 'Lon', 'Lat', 'X', 'Y', 'Type']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered_data)
