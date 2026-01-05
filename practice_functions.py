# --- 1. 定义一个简单的计算函数 ---
# price 和 discount 是“参数”（输入）
def calculate_price(price, discount):
    final_price = price * discount
    return final_price # return 是“返回值”（输出）

# --- 2. 带默认参数的函数 ---
# 如果不传 discount_rate，它就默认是 1.0 (不打折)
def format_user_msg(name, role="普通会员"):
    return f"用户: {name} (等级: {role})"

# --- 3. 结合逻辑的函数 ---
def check_stock(amount):
    if amount > 0:
        return "库存充足"
    else:
        return "暂时缺货"

def get_grade(score):
    if score >= 90:
        return "优秀"
    if score >= 60:
        return "及格"
    else:
        return "不及格"
# --- 开始调用 (使用) 这些函数 ---

# 调用 1: 计算打折
p1 = 100
d1 = 0.8
result = calculate_price(p1, d1)
print(f"原价 {p1} 的商品，8折后价格为: {result}")

# 调用 2: 格式化信息
print(format_user_msg("lee", "高级VIP"))
print(format_user_msg("张三")) # 不传第二个参数，会使用默认值

# 调用 3: 检查库存
apple_stock = 10
print(f"苹果状态: {check_stock(apple_stock)}")
print(f"西瓜状态: {check_stock(0)}")

print(get_grade(85))