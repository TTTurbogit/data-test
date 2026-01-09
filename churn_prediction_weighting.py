import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score

# 1. 构造与之前一致的数据
np.random.seed(42)
n_samples = 2500
df = pd.DataFrame({
    '月租费': np.random.normal(100, 20, n_samples),
    '流量': np.random.normal(10, 5, n_samples),
    '月份': np.random.choice(range(1, 10), n_samples)
})
df['是否流失'] = 0

# 1-6月：月租贵流失
mask1 = (df['月份'] <= 6) & (df['月租费'] > 110)
df.loc[mask1, '是否流失'] = np.random.choice([0, 1], size=mask1.sum(), p=[0.2, 0.8])

# 7-9月：流量少流失
mask2 = (df['月份'] > 6) & (df['流量'] < 5)
df.loc[mask2, '是否流失'] = np.random.choice([0, 1], size=mask2.sum(), p=[0.2, 0.8])

# 2. 准备数据
features = ['月租费', '流量']
train_df = df[df['月份'] <= 8].copy()
test_df = df[df['月份'] == 9].copy()

X_train = train_df[features]
y_train = train_df['是否流失']
X_test = test_df[features]
y_test = test_df['是否流失']

print("--- 实验：对比普通重训 vs 样本加权重训 ---")

# --- 方案 A: 普通全量重训 ---
model_normal = RandomForestClassifier(random_state=42)
model_normal.fit(X_train, y_train)
y_pred_a = model_normal.predict(X_test)
print(f"\n[方案 A: 普通重训] 9月召回率: {recall_score(y_test, y_pred_a):.2%}")

# --- 方案 B: 样本加权 (P6+ 技巧) ---
# 给 7-8 月的数据赋予更高的权重 (例如 5 倍)
# 创建权重向量，默认为 1
weights = np.ones(len(train_df))
# 将 7-8 月的数据权重设为 5
weights[train_df['月份'].isin([7, 8])] = 5

model_weighted = RandomForestClassifier(random_state=42)
# 在 fit 时传入 sample_weight
model_weighted.fit(X_train, y_train, sample_weight=weights)

y_pred_b = model_weighted.predict(X_test)
print(f"[方案 B: 样本加权] 9月召回率: {recall_score(y_test, y_pred_b):.2%}")

# --- 诊断环节：为什么加权反而没用？ ---
print("\n--- 诊断：AI 到底看重什么？(特征重要性) ---")
print("方案 A (普通):", dict(zip(features, model_normal.feature_importances_.round(2))))
print("方案 B (加权):", dict(zip(features, model_weighted.feature_importances_.round(2))))

# --- 方案 C: 滑动窗口 (Rolling Window) ---
# 既然旧数据在“捣乱”，告诉 AI 流量低没事，那我们干脆直接扔掉旧数据！
# 只用 7-8 月训练
print("\n--- 方案 C: 滑动窗口 (只用7-8月数据) ---")
train_df_recent = df[df['月份'].isin([7, 8])].copy()
X_train_recent = train_df_recent[features]
y_train_recent = train_df_recent['是否流失']

model_rolling = RandomForestClassifier(random_state=42)
model_rolling.fit(X_train_recent, y_train_recent)

y_pred_c = model_rolling.predict(X_test)
print(f"[方案 C: 滑动窗口] 9月召回率: {recall_score(y_test, y_pred_c):.2%}")

print("\n最终总结：")
print("1. 如果方案 B 的‘流量’重要性没显著提升，说明旧数据干扰太强。")
print("2. 方案 C 通常是解决‘规律彻底反转’的最好办法。")
