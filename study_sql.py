import sqlite3
import pandas as pd

# 1. 连接到数据库 (如果文件不存在，会自动创建)
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

print("--- 1. 创建表并插入数据 ---")
# 使用 SQL 语句创建一个学生表
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    score REAL
)
''')

# 插入一些假数据
# 注意：SQL 插入通常用元组
student_list = [
    (1, "张三", 20, 58.5),
    (2, "李四", 22, 92.0),
    (3, "王五", 19, 75.0),
    (4, "赵六", 21, 95.5)
]

cursor.executemany("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)", student_list)
conn.commit() # 必须要 commit，数据才会真正写入硬盘
print("数据已存入 SQLite 数据库。")

# --- 2. 使用 SQL 进行查询 (核心！) ---
print("\n--- 2. 执行 SQL 查询 ---")

# 需求：查询年龄大于 20 岁的学生，且按分数从高到低排序
# 这里的语句就是标准 SQL
query = "SELECT name, score FROM students WHERE age >= 20 ORDER BY score DESC"

cursor.execute(query)
results = cursor.fetchall()

print("查询结果 (年龄>=20, 分数倒序):")
for row in results:
    print(f"姓名: {row[0]}, 分数: {row[1]}")


query2 = "SELECT name, score FROM students WHERE score < 60 AND name LIKE '%张%'  ORDER BY score DESC"
cursor.execute(query2)
results2 = cursor.fetchall()

print("查询结果 (名字里带‘张’字，且分数不及格):")
for row in results2:
    print(f"姓名: {row[0]}, 分数: {row[1]}")
# --- 3. 终极技巧：SQL + Pandas (职场最常用) ---
# 数据分析师通常直接把 SQL 查询的结果变成 DataFrame
print("\n--- 3. 将 SQL 结果转化为 Pandas DataFrame ---")
df_from_sql = pd.read_sql_query("SELECT * FROM students", conn)
print(df_from_sql)

# 记得关闭连接
conn.close()
