import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import chardet


# 设置中文 (Seaborn 也会用到 Matplotlib 的配置)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

with open('beijing_air.csv', 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']
    df = pd.read_csv("beijing_air.csv", encoding=encoding)
    df["污染等级"] = df["AQI"].apply(lambda x: "优" if x<=50 else("良" if x<=100 else "污染") )
    level = df.groupby("污染等级").count()
    print("\nlevel")
    print(level)

    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x="污染等级",order=['优', '良', '污染'])

plt.title("污染等级柱状图")
plt.savefig("level.png")
print("\n柱状图已保存为 'level.png'")
plt.show()