import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans # 导入 K-Means 算法
from sklearn.datasets import make_blobs # 用来生成一团团的数据

# 为了显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

print("--- 1. 生成模拟客户数据 ---")
# make_blobs 专门用来生成“几堆”数据
# n_samples=200: 生成200个客户
# centers=5: 我们预设生成5个群体 (比如：低收低消、高收高消...)
# cluster_std=1.0: 数据分散程度 (越小越紧凑)
X, y_true = make_blobs(n_samples=200, centers=5, cluster_std=1.0, random_state=42)
print(f"{X}\n")
print(f"{y_true}")
# 把数据变成 DataFrame 方便看
df = pd.DataFrame(X, columns=["年收入 (k$)", "消费评分 (1-100)"])
print("前5个客户的数据：")
print(df.head())

print("\n--- 2. AI 开始自动聚类 (Training) ---")
# 我们告诉 AI：请试着把这些人分成 5 组 (n_clusters=5)
kmeans = KMeans(n_clusters=5, random_state=42)

# 核心代码就这一行！AI 自动学习数据的特征
# fit_predict: 训练并直接预测每个人的类别 (0, 1, 2, 3, 4)
y_kmeans = kmeans.fit_predict(X)

# 把预测结果加回表格
df["AI分类结果"] = y_kmeans
print("\n分类完成！前5个客户被分到了这些组：")
print(df.head())

print("\n--- 3. 可视化结果 ---")
plt.figure(figsize=(10, 6))

# 画散点图
# c=y_kmeans: 根据分类结果给不同颜色
# cmap='viridis': 颜色盘
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis', alpha=0.7)

# 画出每个群体的“中心点” (红色的 X)
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, marker='x', label="群体中心")

plt.title("AI 客户分群结果 (K-Means)")
plt.xlabel("年收入 (k$)")
plt.ylabel("消费评分 (1-100)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)

plt.savefig("customer_clusters.png")
print("聚类图表已保存为 'customer_clusters.png'")

print("\n--- 进阶：寻找最佳分类数 (手肘法) ---")
wcss = []
 # 试着分 1 到 10 类
for i in range(1, 11):
     kmeans = KMeans(n_clusters=i, random_state=42)
     kmeans.fit(X)
     wcss.append(kmeans.inertia_) # inertia_ 就是误差平方和

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('手肘法寻找最佳 K 值')
plt.xlabel('分类数量 (K)')
plt.ylabel('误差 (WCSS)')
plt.grid()
plt.savefig("elbow_method.png")
print("手肘图已保存为 'elbow_method.png'")
