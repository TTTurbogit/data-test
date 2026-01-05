import pandas as pd
import numpy as np

# 1. 模拟数据准备
print("--- 1. 正在创建订单表和用户表 ---")
orders_data = {
    "订单号": [1001, 1002, 1003, 1004, 1005],
    "用户ID": [1, 2, 1, 3, 2],
    "消费金额": [250, 450, 150, 600, 300]
}
users_data = {
    "用户ID": [1, 2, 3, 4],
    "姓名": ["小明", "小红", "小刚", "小强"],
    "性别": ["男", "女", "男", "男"],
    "年龄": [25, 30, 25, 40]
}

df_orders = pd.DataFrame(orders_data)
df_users = pd.DataFrame(users_data)

# 2. 数据合并 (Merge) - 相当于 SQL 的 JOIN
# 我们通过“用户ID”把两张表合二为一
print("\n--- 2. 合并后的完整报表 ---")
df_combined = pd.merge(df_orders, df_users, on="用户ID", how="left")
print(df_combined)
df_combined["消费水平"] = df_combined["消费金额"].apply(lambda x: "高" if x > 300 else "中")
print("\n含消费水平的报表")
print(df_combined)

# 3. 分组聚合 (Groupby) - 深度分析
print("\n--- 3. 核心统计分析 ---")

# 统计不同性别的平均消费金额
gender_analysis = df_combined.groupby("性别")["消费金额"].mean()
print("不同性别的平均消费：")
print(gender_analysis)

# 统计不同年龄段的总消费金额
age_analysis = df_combined.groupby("年龄")["消费金额"].sum()
print("\n不同年龄的总消费：")
print(age_analysis)


people = df_combined.groupby("消费水平")["用户ID"].count()
print("\n不同消费水平的人群分布")
print(people)

# 4. 透视表 (Pivot Table) - 多维度交叉
# 比如我想看：不同性别在不同年龄下的平均消费
print("\n--- 4. 生成交叉透视表 ---")
pivot = df_combined.pivot_table(
    values="消费金额", 
    index="性别", 
    columns="年龄", 
    aggfunc="mean" # 统计方式：平均值
)
print(pivot)

# 5. 填补缺失值 (处理透视表产生的 NaN)
print("\n--- 5. 清洗透视表 (填补空值) ---")
pivot_clean = pivot.fillna(0)
print(pivot_clean)


