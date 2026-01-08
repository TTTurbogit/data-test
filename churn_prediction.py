import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score

# 设置随机种子，保证每次运行结果一致
np.random.seed(42)

print("--- 1. 构造‘概念漂移’的时间序列数据 ---")
# 我们生成 2000 条数据
n_samples = 2000
df = pd.DataFrame({
    '月租费': np.random.normal(100, 20, n_samples),
    '流量': np.random.normal(10, 5, n_samples),
    # 随机分配月份：1到8月
    '月份': np.random.choice(range(1, 9), n_samples)
})

# 初始化流失为 0
df['是否流失'] = 0

# --- 关键点：不同时间段，流失原因不同 ---

# 【阶段 A：1-6月】 嫌贵阶段
# 规则：只看月租。月租 > 110 的人大概率流失
mask_phase1 = (df['月份'] <= 6) & (df['月租费'] > 110)
df.loc[mask_phase1, '是否流失'] = np.random.choice([0, 1], size=mask_phase1.sum(), p=[0.2, 0.8])

# 【阶段 B：7-8月】 缺流量阶段 (环境变了！)
# 规则：只看流量。流量 < 5G 的人大概率流失 (月租无所谓了)
mask_phase2 = (df['月份'] > 6) & (df['流量'] < 5)
df.loc[mask_phase2, '是否流失'] = np.random.choice([0, 1], size=mask_phase2.sum(), p=[0.2, 0.8])

print(f"数据生成完毕。总行数: {len(df)}")
print(f"1-6月流失主因：月租贵。 7-8月流失主因：流量少。\n")

# ==========================================
# 实验 1：错误的验证方式 (随机切分)
# ==========================================
print("【实验 1：错误的随机切分 (Random Split)】")
print("模拟场景：把未来的数据混进训练集，AI '穿越'了...")

features = ['月租费', '流量']
X = df[features]
y = df['是否流失']

# 随机打乱切分 (80% 训练, 20% 测试)
# 这里的 X_test 里可能包含了 7、8 月的数据，X_train 里也可能包含
X_train_rand, X_test_rand, y_train_rand, y_test_rand = train_test_split(X, y, test_size=0.2, random_state=42)

model_rand = RandomForestClassifier(random_state=42)
model_rand.fit(X_train_rand, y_train_rand)

y_pred_rand = model_rand.predict(X_test_rand)
print(f"-> 测试集准确率: {accuracy_score(y_test_rand, y_pred_rand):.2%}")
print(f"-> 召回率 (Recall): {recall_score(y_test_rand, y_pred_rand):.2%}")
print("评价：分数很高！但这是作弊，因为模型在训练时偷看到了未来的规律。 সন")

# ==========================================
# 实验 2：正确的验证方式 (时间切分)
# ==========================================
print("\n【实验 2：正确的时间切分 (Time-Series Split)】")
print("模拟场景：严守时间线，用 1-6 月预测 7-8 月...")

# 训练集：1-6月
train_mask = df['月份'] <= 6
X_train_time = df.loc[train_mask, features]
y_train_time = df.loc[train_mask, '是否流失']

# 测试集：7-8月 (模拟未来上线)
test_mask = df['月份'] > 6
X_test_time = df.loc[test_mask, features]
y_test_time = df.loc[test_mask, '是否流失']

model_time = RandomForestClassifier(random_state=42)
model_time.fit(X_train_time, y_train_time)

# 预测未来
y_pred_time = model_time.predict(X_test_time)
print(f"-> 测试集准确率: {accuracy_score(y_test_time, y_pred_time):.2%}")
print(f"-> 召回率 (Recall): {recall_score(y_test_time, y_pred_time):.2%}")

print("\n------------------------------------------------")
print("🔴 真相揭晓：")
if recall_score(y_test_time, y_pred_time) < 0.4: # 调整判断标准
    print("模型彻底崩了！Recall 极低。")
    print("因为它只学过‘月租贵会导致流失’，")
    print("完全不懂7-8月新出现的‘流量少会导致流失’这个新规律。")
    print("这就是为什么一定要做‘时间外验证 (OOT)’！")
else:
    print("模型表现尚可。")

# ==========================================
# 实验 3：模型迭代 (Retraining) - 你的解决方案
# ==========================================
print("\n【实验 3：模型迭代 (Retraining)】")
print("模拟场景：到了9月，我们用 1-8 月的全量数据重训，预测 9 月...")

# 1. 生成 9 月份的数据 (规律和 7-8 月一样：流量少会导致流失)
df_sept = pd.DataFrame({
    '月租费': np.random.normal(100, 20, 500),
    '流量': np.random.normal(10, 5, 500),
    '月份': 9
})
df_sept['是否流失'] = 0
mask_sept = (df_sept['流量'] < 5) # 9月的规律
df_sept.loc[mask_sept, '是否流失'] = np.random.choice([0, 1], size=mask_sept.sum(), p=[0.2, 0.8])

# 2. 准备训练集 (1-8月)
# 也就是把之前的 df (1-8月) 全部用来训练
X_train_new = df[features]
y_train_new = df['是否流失']

# 3. 准备测试集 (9月)
X_test_new = df_sept[features]
y_test_new = df_sept['是否流失']

# 4. 重训模型
model_retrain = RandomForestClassifier(random_state=42)
model_retrain.fit(X_train_new, y_train_new)

# 5. 验证效果
y_pred_new = model_retrain.predict(X_test_new)

print(f"-> 9月测试集准确率: {accuracy_score(y_test_new, y_pred_new):.2%}")
print(f"-> 9月召回率 (Recall): {recall_score(y_test_new, y_pred_new):.2%}")
print("评价：起死回生！模型学会了新知识，又可以愉快地工作了。")