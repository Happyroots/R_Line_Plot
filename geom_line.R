library(ggplot2)

library(showtext)

# 如果没有加载 showtext，可以这样添加和启用自定义字体
font_add("Times New Roman", regular = "times.ttf")  # 请确保系统中安装了Times New Roman
showtext_auto()

# 设置当前工作目录为需要处理的文件夹
setwd("D:\\Documents\\R\\simulatorDataProcess")  # 替换为你的文件夹路径

# 获取当前文件夹中的所有CSV文件
csv_files <- list.files(pattern = "\\.csv$", full.names = TRUE)

# 遍历每个CSV文件
for (csv_file in csv_files) {
    
  # 读取数据
  data <- read.csv(csv_file, header = TRUE, na.strings = c("NA"))
  head(data,10)  #head()函数，默认查看数据框前6行，这里我们定义查看前10行 


  # 绘制 COG 折线图
  p <- ggplot(
    data, aes(x = Time, y = COG, color = Type, shape = Type)) +
    geom_line(size = 1.5) +
    labs(
      x = expression(italic("Time") ~ "(minute)"),           # 添加时间单位
      y = expression(italic(phi) ~ "(degree)")  # 使用 expression 添加角度单位
    ) +
    geom_hline(aes(yintercept = 0), alpha = 0.65) +
    theme_minimal() +
    theme(
      text = element_text(size = 62, family = "serif"),  # 设置全局文本大小
      plot.margin = margin(t = 10, r = 10, b = 10, l = 10),
      panel.grid.major = element_line(color = "grey80", size = 0.2),
      panel.grid.minor = element_blank(),
      axis.text = element_text(size = 42),  # 设置坐标轴刻度字号

      # axis.title = element_text(size = 22, face = "bold"),  # 设置坐标轴标题字号
      axis.title.x = element_text(size = 72,  margin = margin(t = 15)),  # face = "bold", 设置 x 轴标题字号和上边距
      axis.title.y = element_text(size = 72,  margin = margin(r = 15)),  # 设置 y 轴标题字号和右边距

      legend.title = element_blank(),
      legend.text = element_text(size = 62),  # 设置图例文字大小
      legend.position = "bottom",
      legend.margin = margin(t = 10)  # 增加图例与图形的间距
    ) +
    # 设置 y 轴范围和刻度
    scale_y_continuous(
      limits = c(min(data$COG) - 10, max(data$COG) + 10),
      breaks = seq(floor(min(data$COG) / 10) * 10 - 10, ceiling(max(data$COG) / 10) * 10 + 10, 50)    
    )

  print(p)
  # 获取文件名（不带路径和扩展名）
  base_name <- tools::file_path_sans_ext(basename(csv_file))
  # 保存图像
  ggsave(paste0(base_name, "_cog_plot.png"), plot = p, width = 12, height = 6, dpi = 300)
  print(paste("Saved COG plot for", base_name))

  # 绘制 SOG 折线图
  p <- ggplot(
    data, aes(x = Time, y = SOG, color = Type, shape = Type)) +
    geom_line(size = 1.5) +
    labs(
      x = expression(italic("Time") ~ "(minute)"),           # 添加时间单位
      y = expression(italic("v") ~ "(kn)")   # 使用 expression 添加角度单位
    ) +
    geom_hline(aes(yintercept = 0), alpha = 0.65) +
    theme_minimal() +
    theme(
      text = element_text(size = 62, family = "serif"),  # 设置全局文本大小
      plot.margin = margin(t = 10, r = 10, b = 10, l = 10),
      panel.grid.major = element_line(color = "grey80", size = 0.2),
      panel.grid.minor = element_blank(),
      axis.text = element_text(size = 42),  # 设置坐标轴刻度字号

      # axis.title = element_text(size = 22, face = "bold"),  # 设置坐标轴标题字号
      axis.title.x = element_text(size = 72,  margin = margin(t = 15)),  # face = "bold", 设置 x 轴标题字号和上边距
      axis.title.y = element_text(size = 72,  margin = margin(r = 15)),  # 设置 y 轴标题字号和右边距

      legend.title = element_blank(),
      legend.text = element_text(size = 62),  # 设置图例文字大小
      legend.position = "bottom",
      legend.margin = margin(t = 10)  # 增加图例与图形的间距
    ) +
    # 设置 y 轴范围和刻度
    scale_y_continuous(
      limits = c(min(data$SOG) - 5, max(data$SOG) + 5),
      breaks = seq(floor(min(data$SOG) / 10) * 10 - 5, ceiling(max(data$SOG) / 10) * 10 + 5, 5)    
    )
  print(p)
  # 获取文件名（不带路径和扩展名）
  base_name <- tools::file_path_sans_ext(basename(csv_file))
  # 保存图像
  ggsave(paste0(base_name, "_sog_plot.png"), plot = p, width = 12, height = 6, dpi = 300)
  print(paste("Saved SOG plot for", base_name))


  # 绘制 Trajectory 折线图
  p <- ggplot(
    data, aes(x = Lat, y = Lon, color = Type, shape = Type)) +
    geom_line(size = 1.5) +
    labs(
      x = expression(italic("Latitude")),          
      y = expression( italic("Longitude")  ) 
    ) +
    geom_hline(aes(yintercept = 0), alpha = 0.65) +
    theme_minimal() +
    theme(
      text = element_text(size = 62, family = "serif"),  # 设置全局文本大小
      plot.margin = margin(t = 10, r = 10, b = 10, l = 10),
      panel.grid.major = element_line(color = "grey80", size = 0.2),
      panel.grid.minor = element_blank(),
      axis.text = element_text(size = 42),  # 设置坐标轴刻度字号

      # axis.title = element_text(size = 22, face = "bold"),  # 设置坐标轴标题字号
      axis.title.x = element_text(size = 72,  margin = margin(t = 15)),  # face = "bold", 设置 x 轴标题字号和上边距
      axis.title.y = element_text(size = 72,  margin = margin(r = 15)),  # 设置 y 轴标题字号和右边距

      legend.title = element_blank(),
      legend.text = element_text(size = 62),  # 设置图例文字大小
      legend.position = "bottom",
      legend.margin = margin(t = 10)  # 增加图例与图形的间距
    ) +
    
    scale_x_continuous(
      limits = c((min(data$Lat)) , (max(data$Lat ) ) ),
      breaks = seq(floor(min(data$Lat)) , ceiling(max(data$Lat) ), 0.05)    
    )+
    
    # 设置 y 轴范围和刻度
    scale_y_continuous(
      limits = c((min(data$Lon)) , (max(data$Lon ) ) ),
      breaks = seq(floor(min(data$Lon)) , ceiling(max(data$Lon) ), 0.05)    
    )
   print(p)
  # 获取文件名（不带路径和扩展名）
  base_name <- tools::file_path_sans_ext(basename(csv_file))
  # 保存图像
  ggsave(paste0(base_name, "_trjectory_plot.png"), plot = p, width = 12, height = 6, dpi = 300)
  print(paste("Saved Trajectory plot for", base_name))


}