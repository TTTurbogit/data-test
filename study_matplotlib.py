import matplotlib.pyplot as plt
import numpy as np

# 为了显示中文 (Windows系统通用设置)
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

print("=== Matplotlib 基础语法 ===")
print("正在生成图表，请留意弹出的窗口或保存的文件...")

# 准备数据 (用 NumPy 生成)
x = np.linspace(0, 10, 100) # 从0到10，切成100份
y1 = np.sin(x)              # 正弦波
y2 = np.cos(x)              # 余弦波

# 1. 创建画布
plt.figure(figsize=(10, 6)) # 宽10，高6

# 2. 画图
# plot(x轴数据, y轴数据, label="图例名", color="颜色")
plt.plot(x, y1, label="正弦波 (Sin)", color="blue", linewidth=2)
plt.plot(x, y2, label="余弦波 (Cos)", color="red", linestyle="--") # 虚线

# 3. 装饰图表
plt.title("数学函数图像展示") # 标题
plt.xlabel("X 轴")           # X轴标签
plt.ylabel("Y 轴")           # Y轴标签
plt.legend()                # 显示图例 (就是那个告诉你是哪条线的框框)
plt.grid(True)              # 显示网格

# 4. 保存或显示
plt.savefig("math_plot.png")
print("图表已保存为 math_plot.png")

# 如果是在交互式环境，可以用 plt.show() 弹出窗口
plt.show()
