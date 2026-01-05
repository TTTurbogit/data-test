# --- 1. 写入模式 ('w' - Write) ---
# 注意：'w' 模式非常霸道，如果文件已存在，它会清空旧内容重新写！
print("--- 正在创建日记文件... ---")

diary_content = [
    "2025-12-24: 开始学习 Python 文件操作.\n",
    "2025-12-24: 天气不错，北京很冷.\n"
]

# with open(文件名, 模式, 编码) as 变量名:
with open("my_diary.txt", "w", encoding="utf-8") as f:
    f.writelines(diary_content) # 一次性写入多行
    print("写入完成！")

# --- 2. 追加模式 ('a' - Append) ---
# 'a' 模式很温柔，它会在文件末尾接着写，不删除旧内容。
print("\n--- 正在追加新记录... ---")

new_record = "2025-12-25: 祝大家圣诞快乐！\n"

with open("my_diary.txt", "a", encoding="utf-8") as f:
    f.write(new_record)
    print("追加完成！")

# --- 3. 读取模式 ('r' - Read) ---
# 读取刚才写进去的内容
print("\n--- 读取文件内容 ---")

try:
    with open("my_diary.txt", "r", encoding="utf-8") as f:
        content = f.read() # 读取全部内容
        print("日记本内容如下：")
        print("----------------")
        print(content)
        print("----------------")
except FileNotFoundError:
    print("错误：找不到文件！")

task = input("请输入要做的事: ")
with open("todo.txt", "a", encoding="utf-8") as f:
    f.write(task)
    print("追加完成！\n")

try:
    with open("todo.txt", "r", encoding="utf-8") as f:
        content = f.read() # 读取全部内容
        print("----------------")
        print(content)
        print("----------------")
        print("已保存")
except FileNotFoundError:
    print("错误：找不到文件！")
