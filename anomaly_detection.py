import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

# 1. 模拟一年 DAU 数据
dates = pd.date_range('2024-01-01', periods=365)
# 基础值 + 周末效应 (每7天一个峰值)
base = 1000
weekly_seasonality = [200 if d.dayofweek >= 5 else 0 for d in dates]
# 加上随机噪声
noise = np.random.normal(0, 30, 365)

dau = base + np.array(weekly_seasonality) + noise

# 2. 埋入异常点 (比如第 100 天服务器崩溃，第 250 天大促)
dau[100] = 400  # 异常下跌
dau[250] = 2500 # 异常上涨

df = pd.DataFrame({'date': dates, 'dau': dau})

# --- 3. 异常检测算法 (3倍标准差原则) ---
# 计算 7 天移动平均值，平滑掉周期性影响
df['rolling_mean'] = df['dau'].rolling(window=7, center=True).mean()
# 计算移动标准差
df['rolling_std'] = df['dau'].rolling(window=7, center=True).std()

# 定义上下界
df['upper'] = df['rolling_mean'] + 3 * df['rolling_std']
df['lower'] = df['rolling_mean'] - 3 * df['rolling_std']

# 标记异常
df['is_anomaly'] = (df['dau'] > df['upper']) | (df['dau'] < df['lower'])

# 4. 可视化
plt.figure(figsize=(15, 7))
plt.plot(df['date'], df['dau'], label='实际 DAU', color='gray', alpha=0.5)
plt.plot(df['date'], df['rolling_mean'], label='7日移动平均 (基准)', color='blue')

# 突出显示异常点
anomalies = df[df['is_anomaly']]
plt.scatter(anomalies['date'], anomalies['dau'], color='red', label='检测到的异常', s=50)

plt.fill_between(df['date'], df['lower'], df['upper'], color='blue', alpha=0.1, label='正常波动区间 (3-Sigma)')

plt.title("DAU 异常检测告警系统")
plt.legend()
plt.savefig("anomaly_detection.png")
print("异常检测报告已生成: anomaly_detection.png")

print(f"\n系统共检测到 {len(anomalies)} 处异常。\n")
print(anomalies[['date', 'dau']].head())
