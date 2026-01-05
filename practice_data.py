# --- 1. 字典基础 (Dictionary Basics) ---
# 字典是用花括号 {} 包裹的，里面是 "键: 值" 对
hero = {
    "name": "spy",        # 键 "name" 对应 值 "钢铁侠"
    "power": 85,            # 键 "power" 对应 值 85
    "weapons": ["掌心炮", "激光"] # 值也可以是一个列表！
}

# 访问字典里的数据：使用方括号 ["键名"]
print(f"英雄: {hero['name']}")
print(f"初始战斗力: {hero['power']}")
print(f"主武器: {hero['weapons'][0]}")

# --- 2. 修改与新增 ---
print("\n--- 正在升级装甲... ---")

# 修改现有的值
hero['power'] = 99 

# 新增一个全新的键值对
hero['location'] = "斯塔克大厦"
hero['color'] = "Black"

print(f"升级后战斗力: {hero['power']}")
print(f"当前位置: {hero['location']}")

# --- 3. 列表与字典的组合 (实战常见结构) ---
# 现实世界的数据通常很复杂，比如“所有玩家的列表”
players = [
    {"id": 101, "name": "Alice", "score": 500},
    {"id": 102, "name": "Bob",   "score": 300},
    {"id": 103, "name": "Charlie", "score": 850},
    {"id": 104, "name": "David", "score": 600}
]

print("\n--- 玩家排行榜 ---")
for p in players:
    # 这里的 p 每次循环都是一个字典
    print(f"ID: {p['id']} - {p['name']} 	得分: {p['score']}")
