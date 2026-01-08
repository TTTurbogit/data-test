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

print("\n结论：通过给‘近期数据’加大权重，AI 成功摆脱了陈旧经验的束缚，更敏锐地捕捉到了新趋势。")
