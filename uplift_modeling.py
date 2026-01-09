import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文 (Seaborn 也会用到 Matplotlib 的配置)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 
# 设置随机种子
np.random.seed(42)
n_samples = 3000

print("--- 1. 构造 Uplift 模拟数据 ---")
# 特征：月租费，网龄
df = pd.DataFrame({
    '月租费': np.random.normal(100, 20, n_samples),
    '网龄': np.random.randint(1, 72, n_samples),
    # 随机实验：50% 的人发了券 (Treated)，50% 的人没发 (Control)
    '发券': np.random.choice([0, 1], n_samples)
})

# 初始化留存标签 (0=流失, 1=留存)
# 注意：我们要模拟四种人！

# 【铁粉】(网龄长, 月租低): 发不发券都留存 (概率 0.9)
mask_loyal = (df['网龄'] > 48) & (df['月租费'] < 90)

# 【死敌】(网龄短, 月租巨高): 发不发券都走 (概率 0.1)
mask_lost = (df['网龄'] < 12) & (df['月租费'] > 130)

# 【羊毛党】(网龄中等, 月租中等): 发券就留(0.8)，不发就走(0.2)
# 这是我们最想抓的人！
mask_persuadable = (df['网龄'].between(12, 48)) & (df['月租费'].between(90, 130))

# 默认基础留存率
df['留存'] = np.random.choice([0, 1], n_samples, p=[0.5, 0.5])

# 填入特定人群的逻辑
# 1. 铁粉：不管发没发券，留存都高
df.loc[mask_loyal, '留存'] = np.random.choice([0, 1], mask_loyal.sum(), p=[0.1, 0.9])

# 2. 死敌：不管发没发券，留存都低
df.loc[mask_lost, '留存'] = np.random.choice([0, 1], mask_lost.sum(), p=[0.9, 0.1])

# 3. 羊毛党：对'发券'极其敏感！
# 这是一个交互项逻辑
# 如果是羊毛党 AND 发券=1 -> 留存率 0.9
mask_p_treat = mask_persuadable & (df['发券'] == 1)
df.loc[mask_p_treat, '留存'] = np.random.choice([0, 1], mask_p_treat.sum(), p=[0.1, 0.9])
# 如果是羊毛党 AND 发券=0 -> 留存率 0.2
mask_p_control = mask_persuadable & (df['发券'] == 0)
df.loc[mask_p_control, '留存'] = np.random.choice([0, 1], mask_p_control.sum(), p=[0.8, 0.2])

print(f"数据生成完毕。羊毛党人数占比: {mask_persuadable.mean():.1%}")

# --- 2. T-Learner (双模型法) ---
print("\n--- 2. 训练 Uplift 模型 (T-Learner) ---")

# 拆分数据
df_control = df[df['发券'] == 0]
df_treated = df[df['发券'] == 1]

features = ['月租费', '网龄']

# 模型 0：学习“自然状态”
model_control = RandomForestClassifier(n_estimators=100, random_state=42)
model_control.fit(df_control[features], df_control['留存'])

# 模型 1：学习“干预状态”
model_treated = RandomForestClassifier(n_estimators=100, random_state=42)
model_treated.fit(df_treated[features], df_treated['留存'])

print("模型训练完毕。")

# --- 3. 预测增益 (Uplift Score) ---
# 现在来了一批新用户，我们想知道给谁发券最划算？
print("\n--- 3. 预测每个人的 Uplift ---")
# 计算两种概率
prob_c = model_control.predict_proba(df[features])[:, 1] # 不发券的留存率
prob_t = model_treated.predict_proba(df[features])[:, 1] # 发券的留存率

# 核心公式：增益 = P(发) - P(不发)
uplift_score = prob_t - prob_c
df['Uplift'] = uplift_score

# --- 4. 结果验证 ---
# 我们看看被模型评分为“高增益”的人，是不是真的符合“羊毛党”特征(网龄12-48, 月租90-130)？
print("正在绘制 Uplift 分布图...")

plt.figure(figsize=(10, 6))
# 用颜色标记真实的“羊毛党”
sns.scatterplot(data=df, x='网龄', y='月租费', hue='Uplift', palette='RdBu_r', size='Uplift', sizes=(10, 100))
# 画个框，标出我们设定的真实羊毛党区域
plt.plot([12, 48, 48, 12, 12], [90, 90, 130, 130, 90], 'r--', lw=2, label='True Persuadables Area')

plt.title("Uplift 预测分布图 (红色代表高营销价值)")
plt.legend()
plt.savefig("uplift_result.png")
print("结果已保存为 'uplift_result.png'。请查看红色高分区域是否落在了虚线框内！")

# 挑几个高分用户看看
print("\n【营销建议名单】(Uplift Score Top 5):")
print(df.sort_values('Uplift', ascending=False)[['月租费', '网龄', 'Uplift']].head())
