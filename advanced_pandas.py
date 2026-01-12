import pandas as pd
import numpy as np

# 1. 模拟面试中的原始数据
raw_orders = [
    {'user_id': 1, 'amount': 100, 'category': '电子'},
    {'user_id': 2, 'amount': -50, 'category': '图书'},  # 异常值：负数
    {'user_id': 1, 'amount': None, 'category': '电子'}, # 异常值：缺失
    {'user_id': 3, 'amount': 200, 'category': '家居'},
    {'user_id': 2, 'amount': 150, 'category': '图书'},
    {'user_id': 4, 'amount': 300, 'category': '电子'},
]

print("--- 原始数据 ---")
df = pd.DataFrame(raw_orders)
print(df)

# --- 2. 数据清洗 (重点记忆这些 API) ---

# 【坑点 1】填充空值：要指定列，且 fillna 是方法
df['amount'] = df['amount'].fillna(0)

# 【坑点 2】过滤数据：使用布尔索引
df = df[df['amount'] >= 0]

print("\n--- 清洗后的数据 ---")
print(df)

# --- 3. 指标计算 (P6 必备聚合技巧) ---

# 【坑点 3】不要写两次 groupby，直接用 .agg 一次性算出所有指标
# nunique() 是去重计数的关键
result = df.groupby('category').agg(
    total_amount=('amount', 'sum'),      # 销售总额
    unique_users=('user_id', 'nunique')  # 独立用户数
)

# 计算人均消费
result['avg_per_user'] = result['total_amount'] / result['unique_users']

# 找出人均消费最高的分类
# idxmax() 返回的是索引(也就是分类名)
top_cat = result['avg_per_user'].idxmax()

print("\n--- 最终统计结果 ---")
print(result)
print(f"\n🏆 人均消费最高的品类是: {top_cat}")

# --- 给你的额外挑战 ---
# 试着在下面添加一行代码，按照 'total_amount' 从高到低排序
# 提示：result.sort_values(...)
sort = result.sort_values('total_amount',ascending=False)
print(f"按照 'total_amount' 从高到低排序是 {sort}")