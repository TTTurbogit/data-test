import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import PartialDependenceDisplay

# 1. 构造数据 (依然使用我们验证过的 7-8 月逻辑)
np.random.seed(42)
n_samples = 1000
df = pd.DataFrame({
    '月租费': np.random.normal(100, 20, n_samples),
    '流量': np.random.normal(10, 5, n_samples),
})

# 模拟一个复杂的非线性规律：
# - 月租 < 100: 大家都能忍，流失率低
# - 月租 > 100: 流失率线性上升
# - 月租 > 130: 到了忍耐极限！流失率直接爆炸
df['流失概率'] = 0.1 # 基础概率
df.loc[df['月租费'] > 100, '流失概率'] += (df['月租费'] - 100) * 0.01
df.loc[df['月租费'] > 130, '流失概率'] += 0.5 # 愤怒值爆表

# 生成最终 0/1 标签
df['是否流失'] = df.apply(lambda row: np.random.choice([0, 1], p=[1-min(row['流失概率'], 0.99), min(row['流失概率'], 0.99)]), axis=1)

X = df[['月租费', '流量']]
y = df['是否流失']

# 2. 训练模型
print("正在训练模型...")
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# 3. P6 级可视化：偏依赖图 (PDP)
# 这张图会告诉你：随着月租费的增加，流失风险到底是缓慢上升，还是突然爆炸？
print("正在生成偏依赖图 (Partial Dependence Plot)...")

fig, ax = plt.subplots(figsize=(12, 6))
# 绘制 '月租费' 和 '流量' 的 PDP
PartialDependenceDisplay.from_estimator(model, X, features=['月租费', '流量'], ax=ax)

plt.suptitle("P6 级洞察：特征与流失风险的非线性关系", fontsize=16)
plt.savefig("churn_pdp.png")
print("\n图表已保存为 'churn_pdp.png'。")
print("请打开这张图，看看 AI 眼中的‘月租费’红线到底在哪里！")
