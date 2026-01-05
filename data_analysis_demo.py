import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# --- 1. 制造模拟数据 (加上“脏数据”) ---
print("--- 正在生成包含缺失值的模拟数据... ---")

products = ["手机", "笔记本", "耳机", "鼠标", "键盘"]
dates = pd.date_range(start="2025-01-01", periods=100)

data = {
    "日期": dates,
    "产品": [random.choice(products) for _ in range(100)],
    "单价": [random.randint(50, 5000) for _ in range(100)],
    "销量": [random.choice([1, 2, 5, np.nan]) for _ in range(100)] # 故意放入 np.nan (缺失值)
}

df = pd.DataFrame(data)

# --- 2. 数据清洗 (Data Cleaning) ---
print("\n--- 发现脏数据！ ---")
# 检查有多少个空值
print(f"当前销量列中的空值数量: {df['销量'].isnull().sum()}")

# 策略：用销量的“平均值”来填补这些空值
mean_sales = df["销量"].mean()
print(f"计算得出的平均销量为: {mean_sales:.2f}，准备填补...")

# 填补空值
df["销量"] = df["销量"].fillna(mean_sales)

# 现在可以安全地计算总价了
df["总价"] = df["单价"] * df["销量"]

print(f"清洗后的空值数量: {df['销量'].isnull().sum()}")
print("前 5 条清洗后的数据：")
print(df.head())

# --- 2. 数据分析 (Data Analysis) ---
print("\n--- 开始分析 ---")

# 问题 1: 总销售额是多少？
total_sales = df["总价"].sum()
print(f"1. 历史总销售额: {total_sales} 元")

# 问题 2: 哪个产品卖得最好（按总销售额）？
# groupby: 分组统计，类似 SQL 或 Excel 透视表
product_performance = df.groupby("产品")["总价"].sum().sort_values(ascending=False)

print("\n2. 各产品销售额排行：")
print(product_performance)

best_product = product_performance.index[0]
print(f"\n🏆 冠军产品是: {best_product}")

# --- 3. 数据可视化 (Data Visualization) ---
# 为了支持中文显示，通常需要设置字体（不同系统字体路径不同，这里为了简单演示可能显示框框，主要看流程）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial'] # 尝试设置中文字体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

print("\n--- 正在生成图表... ---")
try:
    # 画一个柱状图
    plt.figure(figsize=(10, 6))
    product_performance.plot(kind='bar', color='skyblue')
    
    plt.title("各产品销售总额分析")
    plt.xlabel("产品名称")
    plt.ylabel("销售总额 (元)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 保存图片
    plt.savefig("sales_report.png")
    print("图表已保存为 'sales_report.png'，请在文件夹中查看！")
except Exception as e:
    print(f"画图时出了一点小意外: {e}")

# 保存处理后的表格
df.to_csv("sales_data.csv", index=False, encoding="utf-8-sig")
print("详细数据已导出为 'sales_data.csv'")
