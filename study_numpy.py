import numpy as np

print("=== NumPy 基础语法 ===")

# 1. 创建数组 (Array)
# 普通列表
my_list = [1, 2, 3, 4, 5]
# NumPy 数组 (看起来差不多，但功能强大得多)
arr = np.array(my_list)
print(f"原本的列表: {my_list}")
print(f"NumPy 数组: {arr}")

# 2. 为什么要用它？看看数学运算
# 如果是列表: my_list * 2 会变成 [1, 2, ..., 1, 2, ...] (复制了一份)
# 如果是数组:
print(f"数组每个数乘 2: {arr * 2}")      # 结果: [2 4 6 8 10]
print(f"数组每个数加 10: {arr + 10}")    # 结果: [11 12 13 14 15]
print(f"数组之间相加: {arr + arr}")      # 结果: [2 4 6 8 10]

# 3. 统计功能
print(f"平均值 (mean): {np.mean(arr)}")
print(f"最大值 (max): {np.max(arr)}")
print(f"求和 (sum): {np.sum(arr)}")

# 4. 生成数据
# 生成 0 到 10 (不含) 的整数
zeros = np.zeros(5) # 全是 0
ones = np.ones(3)   # 全是 1
range_arr = np.arange(0, 10, 2) # 从0开始，步长为2 -> [0 2 4 6 8]

print(f"自动生成的序列: {range_arr}")

# 5. 二维数组 (矩阵) - 就像 Excel 的表格
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
print("这是一个 2行3列 的矩阵:")
print(matrix)
print(f"矩阵形状 (Shape): {matrix.shape}") # (2, 3)
