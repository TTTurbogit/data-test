import pandas as pd
import numpy as np
import plotly.graph_objects as go # 漏斗图用 plotly 画最漂亮

# 1. 模拟用户行为日志
print("--- 正在生成模拟行为日志... ---")
steps = ['1_首页', '2_搜索', '3_详情页', '4_购物车', '5_下单']
data = {
    'step': steps,
    'users': [10000, 7500, 4000, 1200, 800] # 每一环节剩余的人数
}
df = pd.DataFrame(data)

# 2. 计算转化率 (Conversion Rate)
# 总体转化率 = 当前环节 / 第一环节
df['总体转化率'] = df['users'] / df['users'][0]
# 环节转化率 = 当前环节 / 上一环节
df['环节转化率'] = df['users'].pct_change().add(1).fillna(1)

print("\n--- 漏斗转化报告 ---")
print(df)

# 3. 找出“最痛点”
# 我们看哪一步的“环节转化率”最低（即流失最狠）
# 排除第一行
worst_step_idx = df['环节转化率'][1:].idxmin()
worst_step = df.loc[worst_step_idx, 'step']
drop_rate = 1 - df.loc[worst_step_idx, '环节转化率']

print(f"\n⚠️ 预警：流失最严重的环节是 '{worst_step}'，流失率高达 {drop_rate:.1%}")

# 4. 绘制可视化漏斗图 (使用 Plotly，这种图在汇报中非常高级)
fig = go.Figure(go.Funnel(
    y = df['step'],
    x = df['users'],
    textinfo = "value+percent initial+percent previous" # 显示数值、总体占比、环比占比
))

fig.update_layout(title_text="电商平台全链路转化漏斗")
# 注意：plotly 通常在浏览器打开，这里我们保存为 html
fig.write_html("funnel_report.html")
print("\n漏斗图报告已生成: funnel_report.html (请用浏览器打开查看)")
