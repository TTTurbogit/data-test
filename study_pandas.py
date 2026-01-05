import pandas as pd

print("=== Pandas 基础语法 ===")

# 1. 创建表格 (DataFrame)
# 通常我们用“字典”来创建，键是列名，值是数据列表
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [20, 25, 30, 22],
    "城市": ["北京", "上海", "北京", "深圳"],
    "工资": [8000, 12000, 20000, 9000]
}

df = pd.DataFrame(data)
print("--- 原始表格 ---")
print(df)

# 2. 查看数据
print("\n--- 查看基础信息 ---")
print(df.head(2))  # 只看前 2 行
print(df.columns)  # 查看列名
print(df.describe()) # 快速统计数字列 (平均值、最大最小等)

# 3. 取列 (像查字典一样)
print("\n--- 只看姓名列 ---")
names = df["姓名"] 
print(names)

# 4. 筛选行 (最重要的功能！)
print("\n--- 筛选工资大于 10000 的人 ---")
# 逻辑: df[ 条件 ]
rich_people = df[ df["工资"] > 10000 ]
print(rich_people)

print("\n--- 筛选住在北京的人 ---")
beijing_people = df[ df["城市"] == "北京" ]
print(beijing_people)

# 5. 排序
print("\n--- 按年龄从小到大排序 ---")
sorted_df = df.sort_values(by="年龄")
print(sorted_df)

# 6. 新增一列
df["年薪"] = df["工资"] * 12
print("\n--- 算完年薪后的表格 ---")
print(df)
