# --- 1. 变量 (Variables) ---
# 就像给数据贴标签
name = "lee"  # 字符串 (String)
level = 1              # 整数 (Integer)
is_happy = True        # 布尔值 (Boolean)

print(f"你好，{name}！欢迎来到第 {level} 关。")

# --- 2. 列表 (Lists) ---
# 就像一个购物清单，或者一排储物柜
tools = ["编辑器", "解释器", "咖啡","键盘"]
print(f"我们要准备的第一个工具是: {tools[0]}") # 计算机从0开始数数！

# --- 3. 循环 (Loops) ---
# 只有机器才喜欢重复工作，让人来做太累了
print("\n--- 开始检查工具 ---")
for tool in tools:
    print(f"检查: {tool} ... 准备就绪")

# --- 4. 条件判断 (If/Else) ---
# 让程序学会做决定
score = 50

print("\n--- 考试结果 ---")
if score >= 60:
    print("恭喜，测试通过！(Result: Pass)")
else:
    print("还需要再练习一下。(Result: Fail)")

# --- 5. 函数 (Functions) ---
# 把一段常用的代码打包起来，随时调用
def calculate_area(width, height):
    area = width * height
    return area

# 调用函数
w = 5
h = 10
result = calculate_area(w, h)
print(f"\n一个 {w}x{h} 的矩形面积是: {result}")
