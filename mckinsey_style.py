import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

# --- 1. 准备数据 (模拟财报) ---
# 这是一个经典的 P&L (损益表) 数据结构
data = {
    '项目': ['总营收', '退货损失', '销售成本(COGS)', '物流成本', '营销费用', '行政支出', '净利润'],
    '金额': [1000, -50, -400, -250, -150, -100, 0] # 净利润先填0，后面算
}

df = pd.DataFrame(data)

# 计算净利润 (总营收 + 所有负数的开销)
net_profit = df['金额'].sum()
# 更新表格里的净利润
df.loc[df['项目'] == '净利润', '金额'] = net_profit

print("--- 财务数据预览 ---")
print(df)

# --- 2. 准备画瀑布图的数据 ---
# 瀑布图的核心逻辑：当前的柱子是“浮”在空中的，它的底部是前几个柱子的累加值
# 我们需要计算每一根柱子的“底部位置” (Bottom)
df['累计值'] = df['金额'].cumsum()
# 为了让柱子浮空，我们把“累计值”向后移一位作为下一根柱子的底部
df['底部'] = df['累计值'].shift(1).fillna(0)

# 特殊处理：第一个柱子(总营收)和最后一个柱子(净利润)应该是从0开始的
df.loc[df['项目'] == '总营收', '底部'] = 0
df.loc[df['项目'] == '净利润', '底部'] = 0

# --- 3. 咨询级可视化 (The "McKinsey" Look) ---
plt.figure(figsize=(12, 7))

# 定义颜色逻辑：
# - 增加(收入)用 绿色
# - 减少(成本)用 红色
# - 最终结果(净利润)用 蓝色
colors = []
for val in df['金额']:
    if val > 0:
        colors.append('#2E8B57') # 海藻绿 (稳重)
    else:
        colors.append('#C0392B') # 绯红 (警示)
colors[-1] = '#2980B9' # 最后一个柱子给蓝色

# 画柱状图
# 核心技巧：使用 'bottom' 参数让柱子浮起来
bars = plt.bar(
    df['项目'], 
    df['金额'], 
    bottom=df['底部'], 
    color=colors,
    edgecolor='white',
    width=0.6
)

# --- 4. 添加数据标签 (核心：让老板一眼看到数字) ---
for i, rect in enumerate(bars):
    height = rect.get_height()
    
    # 格式化数字：正数加'+'号
    label_text = f"{df.loc[i, '金额']:+.0f}"
    
    # 在柱子中间写字
    plt.text(
        rect.get_x() + rect.get_width()/2, 
        df.loc[i, '底部'] + height + (10 if height>0 else -20), # 位置微调
        label_text, 
        ha='center', 
        va='bottom', 
        fontsize=11, 
        fontweight='bold'
    )

# --- 5. 添加“连线” (Bridge) ---
# 咨询报告里通常会有虚线连接各个柱子，显示流动感
for i in range(len(df) - 1):
    y_start = df.loc[i, '累计值']
    # 画一条虚线到下一个柱子
    plt.plot(
        [i, i+1], 
        [y_start, y_start], 
        color='gray', 
        linestyle='--',
        linewidth=1
    )

# --- 6. 装饰图表 (Storytelling) ---
# 咨询风格：标题就是结论！不要写 "2024财务图表"，要写 Insight
plt.title(
    "洞察：物流成本过高(-250)是导致净利润仅剩 5% 的主要原因", 
    fontsize=16, 
    pad=30, 
    loc='left', # 标题靠左，显得专业
    fontweight='bold'
)

# 去掉多余的边框 (极简主义)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.ylabel("金额 (百万)")

plt.tight_layout()
plt.savefig("mckinsey_waterfall.png")
print("\n图表已生成：mckinsey_waterfall.png")
