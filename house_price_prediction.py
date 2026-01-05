import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # 导入线性回归模型
from sklearn.model_selection import train_test_split # 导入拆分工具

# 为了显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

# 1. 准备数据
# 假设面积是 50~200 平米，价格 = 面积 * 3 + 一些随机波动 (单位: 万元)
np.random.seed(42)
area = np.random.randint(50, 200, 100).reshape(-1, 1) # 100个面积数据
price = area * 3 + np.random.normal(0, 30, (100, 1)) # 价格，加上一点杂音

# 2. 拆分数据集 (机器学习的精髓！)
# 我们把数据分成“训练集”和“测试集”
# 训练集 (80%): 用来给 AI 学习
# 测试集 (20%): 留着用来考考 AI，看它学得好不好
X_train, X_test, y_train, y_test = train_test_split(area, price, test_size=0.2, random_state=42)

print(f"训练数据量: {len(X_train)}, 测试数据量: {len(X_test)}")

# 3. 创建并训练模型
model = LinearRegression()
model.fit(X_train, y_train) # 这里的 fit 就是“学习”的过程

# 4. 预测未来
new_area = [[160]] # 我们想预测 160 平米的房子
predicted_price = model.predict(new_area)
print(f"\nAI 预测：160 平米的房子大约价值: {predicted_price[0][0]:.2f} 万元")

# 5. 可视化：看看那条“趋势线”
plt.figure(figsize=(10, 6))
plt.scatter(area, price, color='blue', alpha=0.5, label='真实数据')
plt.plot(area, model.predict(area), color='red', linewidth=2, label='AI 学习到的规律线')

plt.title("面积与房价的关系 (线性回归)")
plt.xlabel("面积 (平米)")
plt.ylabel("价格 (万元)")
plt.legend()
plt.grid(True)
plt.savefig("house_prediction.png")
print("\n预测图表已保存为 'house_prediction.png'")

from sklearn.metrics import r2_score

# 用测试集来考试
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print(f"AI 的考试成绩 (R² Score): {score:.4f}")
