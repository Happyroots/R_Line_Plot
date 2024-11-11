import os
import pandas as pd
import gps2xy

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    os_data = []
    ts_data = []
    timeStampFirst = -1.0
    X_OS_First = -1.0
    Y_OS_First = -1.0
    X_TS_First = -1.0
    Y_TS_First = -1.0

    for line in lines:
        if 'OS:1' in line:
            data = dict(item.split(':') for item in line.strip().split('\t'))
            time = int(data.get('Time', 0) )
            if(timeStampFirst < 0):
                timeStampFirst = time
            time -= timeStampFirst
            time_in_minutes = time / 1000000.0 / 60.0
            Lat = float(data.get('Lat', 0))
            Lon = float(data.get('Lon', 0))
            X, Y = gps2xy.WGS84ToWebMercator_Single(Lat, Lon)
            if(Lat == 0):
                continue
            if(X_TS_First < 0):
                X_OS_First = X_TS_First = X
                Y_OS_First = Y_TS_First = Y

            X -= X_OS_First
            Y -= Y_OS_First

            # Convert timestamp to UTC datetime
            # dt_seconds = datetime.datetime.fromtimestamp(time_in_seconds)

            os_data.append({
                'Type': 'OS',
                'Time': time_in_minutes,
                'SOG': float(data.get('SOG', 0)),
                'COG': float(data.get('COG', 0)),
                'Lat': float(data.get('Lat', 0)),
                'Lon': float(data.get('Lon', 0)),
                'X':float(X),
                'Y':float(Y)
            })
        elif 'TS:1' in line:
            data = dict(item.split(':') for item in line.strip().split('\t'))
            time = int(data.get('Time', 0) )
            time -= timeStampFirst
            time_in_minutes = time / 1000000.0 / 60.0
            Lat = float(data.get('Lat', 0))
            if(Lat == 0):
                continue

            Lon = float(data.get('Lon', 0))
            X, Y = gps2xy.WGS84ToWebMercator_Single(Lat, Lon)

            if(X_TS_First < 0):
                continue
            X -= X_OS_First
            Y -= Y_OS_First

            if(Lat == 0):
                continue
            ts_data.append({
                'Type': 'TS',
                'Time': time_in_minutes,
                'SOG': float(data.get('SOG', 0)),
                'COG': float(data.get('COG', 0)),
                'Lat': float(data.get('Lat', 0)),
                'Lon': float(data.get('Lon', 0)),
                'X':float(X),
                'Y':float(Y)

            })

    df_os = pd.DataFrame(os_data)
    df_ts = pd.DataFrame(ts_data)

    # 合并 OS 和 TS 数据
    combined_df = pd.concat([df_os, df_ts], ignore_index=True)

    return combined_df

def main(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            combined_df = process_file(file_path)
            
            # 构建输出文件名
            base_name = os.path.splitext(filename)[0]
            output_file = f"{base_name}_combined.csv"
            
            # 保存到 CSV 文件
            combined_df.to_csv(output_file, index=False)
            
            print(f"Processed {filename}: Combined data saved to {output_file}")

if __name__ == "__main__":
    folder_path = './'  # 替换为你的文件夹路径
    main(folder_path)