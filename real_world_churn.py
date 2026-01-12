import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 设置中文 (Seaborn 也会用到 Matplotlib 的配置)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

# 1. 加载真实数据
print("--- 1. 正在读取真实 IBM 电信数据集 ---")
df = pd.read_csv('telco_churn.csv')
print(f"原始数据形状: {df.shape}")

# 2. 硬核清洗 (P6 必修课)
print("\n--- 2. 正在进行数据清洗 ---")

# A. 处理 TotalCharges 的空格问题 (这是该数据集著名的坑)
# errors='coerce' 会把无法转成数字的空格变成 NaN
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# B. 处理缺失值 (由于只有11行缺失，我们直接删除)
df.dropna(inplace=True)

# C. 转换标签: Churn (Yes/No) -> 1/0
df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

# D. 剔除对预测无用的 ID 列
df.drop('customerID', axis=1, inplace=True)

# 3. 特征工程 (One-Hot Encoding)
print("--- 3. 正在进行特征工程 (One-Hot 编码) ---")
# 自动把所有文字分类列变成数字列
df_final = pd.get_dummies(df)

# 4. 训练模型
print("--- 4. 正在训练模型 ---")
X = df_final.drop('Churn', axis=1)
y = df_final['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 使用 class_weight 处理不平衡 (因为流失率只有 26%)
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 5. 评估
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n--- 5. 真实模型评估报告 ---")
print(f"ROC-AUC 分数: {roc_auc_score(y_test, y_prob):.4f}")
print("\n详细指标:")
print(classification_report(y_test, y_pred))

# 6. 特征重要性分析 (真实业务逻辑)
print("\n--- 6. 真实业务洞察: 哪些因素决定了用户流失？ ---")
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("Top 10 核心特征:")
print(importances.head(10))

# 可视化重要性
plt.figure(figsize=(10, 6))
importances.head(15).plot(kind='barh', color='teal').invert_yaxis()
plt.title("真实电信用户流失特征权重 (IBM Dataset)")
plt.tight_layout()
plt.savefig("real_churn_importance.png")
print("\n分析图表已保存为 'real_churn_importance.png'")
