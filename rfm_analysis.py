import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

# --- 1. 模拟 1 万条订单数据 (Raw Data) ---
print("--- 正在生成模拟交易数据... ---")
np.random.seed(42)
n_orders = 10000

# 模拟 1000 个用户
user_ids = np.random.randint(1000, 2000, n_orders)
# 模拟最近一年的日期
dates = pd.date_range(start='2024-01-01', end='2024-12-31')
order_dates = np.random.choice(dates, n_orders)
# 模拟金额 (大部分是小额，少数大额)
amounts = np.random.exponential(scale=200, size=n_orders) + 10 

df = pd.DataFrame({
    'user_id': user_ids,
    'order_date': order_dates,
    'amount': amounts
})

print(f"原始数据预览:\n{df.head()}")

# --- 2. 数据清洗与 ETL ---
# 把日期转成 datetime 对象 (这是必须的步骤)
df['order_date'] = pd.to_datetime(df['order_date'])

# 假设今天是 2025年1月1日 (观察点)
NOW = pd.to_datetime('2025-01-01')

# --- 3. 计算 R, F, M 值 (核心聚合) ---
# 这里的 groupby 是数据分析师的基本功
rfm = df.groupby('user_id').agg({
    'order_date': lambda x: (NOW - x.max()).days, # R: 今天 - 最近一次购买日期 = 几天没来了
    'user_id': 'count',                           # F: 订单数量
    'amount': 'sum'                               # M: 总金额
}).rename(columns={
    'order_date': 'R_days',
    'user_id': 'F_count',
    'amount': 'M_sum'
})

print("\n--- RFM 指标计算完成 ---")
print(rfm.head())

# --- 4. 评分打分 (Scoring) ---
# 我们把 R, F, M 分别切成 5 份 (1-5分)
# R: 越小越好 (分越高) -> 这里的 label 需要反过来，5,4,3,2,1
rfm['R_score'] = pd.qcut(rfm['R_days'], 5, labels=[5, 4, 3, 2, 1])
# F: 越大越好
rfm['F_score'] = pd.qcut(rfm['F_count'], 5, labels=[1, 2, 3, 4, 5])
# M: 越大越好
rfm['M_score'] = pd.qcut(rfm['M_sum'], 5, labels=[1, 2, 3, 4, 5])

# 为了简单，我们把得分拼接起来，比如 "534"
# 但更通用的做法是看是否大于“平均值”
# 我们定义：如果分数 > 平均分，就是 "高"，否则是 "低"

def rfm_segment(row):
    # 这里的 3 是中位数分界线
    r_level = '高' if row['R_score'] >= 3 else '低'
    f_level = '高' if row['F_score'] >= 3 else '低'
    m_level = '高' if row['M_score'] >= 3 else '低'
    
    # 经典分类规则
    if r_level == '高' and f_level == '高' and m_level == '高':
        return '重要价值客户'
    elif r_level == '高' and f_level == '低' and m_level == '高':
        return '重要发展客户'
    elif r_level == '低' and f_level == '高' and m_level == '高':
        return '重要保持客户'
    elif r_level == '低' and f_level == '低' and m_level == '高':
        return '重要挽留客户'
    elif r_level == '高' and f_level == '高' and m_level == '低':
        return '一般价值客户'
    else:
        return '一般挽留客户' # 简化版，没写全8类

# 将 score 列转为整数以便比较
rfm['R_score'] = rfm['R_score'].astype(int)
rfm['F_score'] = rfm['F_score'].astype(int)
rfm['M_score'] = rfm['M_score'].astype(int)

rfm['用户标签'] = rfm.apply(rfm_segment, axis=1)

print("\n--- 用户分层结果 ---")
print(rfm['用户标签'].value_counts())

# --- 5. 可视化分析报告 ---
plt.figure(figsize=(10, 6))
# 绘制不同用户群体的数量对比
sns.countplot(y='用户标签', data=rfm, order=rfm['用户标签'].value_counts().index, palette='viridis')
plt.title("用户价值分层统计 (RFM模型)")
plt.xlabel("用户人数")
plt.tight_layout()
plt.savefig("rfm_result.png")
print("\n图表已保存为 rfm_result.png")

# --- 6. 输出给运营部门的名单 ---
# 筛选出需要“挽留”的大客户
vip_churn = rfm[rfm['用户标签'] == '重要挽留客户']
vip_churn.to_csv("vip_churn_list.csv")
print(f"已生成 'vip_churn_list.csv'，共包含 {len(vip_churn)} 名需挽留的土豪用户。")
