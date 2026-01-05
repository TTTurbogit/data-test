import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文 (Seaborn 也会用到 Matplotlib 的配置)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

# 1. 使用 Seaborn 自带的“泰坦尼克号”数据集
# 如果网络不好可能加载慢，这里我们手动造一点数据，稳妥起见
print("--- 正在准备数据... ---")

# 模拟一个学生的各科成绩表
data = {
    "数学": np.random.randint(60, 100, 50),
    "物理": np.random.randint(60, 100, 50),
    "英语": np.random.randint(50, 95, 50),
    "语文": np.random.randint(70, 90, 50),
    "体育": np.random.randint(80, 100, 50)
}
df = pd.DataFrame(data)

# 2. 计算“相关性系数” (Correlation)
# 1.0 代表完全正相关 (数学好的人物理也好)
# 0.0 代表没关系
# -1.0 代表完全负相关
corr = df.corr()

print("相关性矩阵预览：")
print(corr)

# 3. 画热力图 (Heatmap)
plt.figure(figsize=(8, 6))

sns.heatmap(
    corr, 
    annot=True,     # 在格子里显示具体数字
    cmap='coolwarm', # 颜色盘：冷暖色 (蓝色低，红色高)
    linewidths=0.5, # 格子之间的白线宽度
    fmt=".2f"       # 数字保留两位小数
)

plt.title("各科目成绩相关性热力图")
plt.savefig("score_heatmap.png")
print("\n热力图已保存为 'score_heatmap.png'")

# 4. 额外赠送：带有回归线的散点图 (lmplot)
# 看看数学和物理是不是真的有关系？
print("\n--- 正在绘制回归散点图... ---")
sns.lmplot(x="数学", y="物理", data=df)
plt.title("数学 vs 物理 (带回归线)")
plt.savefig("math_physics_regression.png")
print("回归散点图已保存为 'math_physics_regression.png'")
