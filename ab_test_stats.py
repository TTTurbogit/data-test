import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 模拟实验数据 (Conversion Rate 转化率)
# A 组 (旧版): 转化率约 10%
# B 组 (新版): 转化率约 12%
print("--- 正在模拟 A/B 测试数据 (样本量: 1000) ---")
np.random.seed(42)

# 生成 0 和 1 (1代表转化成功，0代表失败)
# size=1000 代表每组有 1000 个用户看到
group_a = np.random.binomial(1, 0.10, 1000)
group_b = np.random.binomial(1, 0.12, 1000)

print(f"A 组转化率: {group_a.mean():.2%}")
print(f"B 组转化率: {group_b.mean():.2%}")
print(f"表面上的提升: {group_b.mean() - group_a.mean():.2%}")

# --- 2. T 检验 (判断显著性) ---
# 我们使用 ttest_ind (独立样本 T 检验)
t_stat, p_value = stats.ttest_ind(group_a, group_b)

print("\n--- 统计检验结果 ---")
print(f"T 统计量: {t_stat:.4f}")
print(f"P 值 (P-value): {p_value:.4f}")

# --- 3. 做出商业决策 ---
alpha = 0.05 # 显著性水平阈值
if p_value < alpha:
    print("\n✅ 结论: 差异显著！(P < 0.05)")
    print("新版本确实提高了转化率，建议全量上线。")
else:
    print("\n❌ 结论: 差异不显著。")
    print("目前的提升可能是由随机波动造成的，不建议仅凭此数据更换版本。")

# --- 4. 可视化差异 ---
plt.figure(figsize=(8, 5))
plt.rcParams['font.sans-serif'] = ['SimHei']
df_plot = pd.DataFrame({
    'Group': ['A (蓝色按钮)']*1000 + ['B (红色按钮)']*1000,
    'Converted': np.concatenate([group_a, group_b])
})

sns.barplot(x='Group', y='Converted', data=df_plot, palette='coolwarm')
plt.title("A/B 测试转化率对比")
plt.ylabel("平均转化率")
plt.savefig("ab_test_result.png")
print("\n结果图表已保存为 'ab_test_result.png'")
