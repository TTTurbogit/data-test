import numpy as np
from scipy import stats
import statsmodels.stats.api as sms

print("--- A/B 测试结果分析 (P7 级统计学) ---")

# 1. 实验数据输入
# 场景：B 组使用了你的 AI 模型进行干预
n_a = 10000  # A组总人数
churn_a = 1050 # A组流失人数

n_b = 10000  # B组总人数
churn_b = 980  # B组流失人数

# 计算流失率
rate_a = churn_a / n_a
rate_b = churn_b / n_b

print(f"A组 (对照组) 流失率: {rate_a:.2%}")
print(f"B组 (实验组) 流失率: {rate_b:.2%}")
print(f"相对降低 (Lift): {(rate_b - rate_a) / rate_a:.2%}")

# 2. 核心挑战：这 0.7% 的差距是真实的吗？
# 我们使用 "双比例 Z 检验" (Two-proportions Z-test)
# 零假设 (H0): A 和 B 没区别，这 0.7% 纯属瞎猫碰死耗子。
# 备择假设 (H1): B 真的比 A 好。

print("\n--- 正在进行假设检验 (Z-Test) ---")
# 构造数据数组：[流失人数A, 流失人数B], [总人数A, 总人数B]
count = np.array([churn_a, churn_b])
nobs = np.array([n_a, n_b])

# 计算 Z 统计量和 P 值
# stat, pval = sms.proportions_ztest(count, nobs, alternative='larger') 
# 注意：我们要证明 A > B (流失率)，所以 alternative 是 'larger' 
# 或者证明 A != B，用 'two-sided'。这里为了简单，我们通常看 A 是否显著高于 B (即 B 显著低于 A)。
# 严谨起见，通常用 two-sided，然后看方向。我们这里用 two-sided 看看。
stat, pval = sms.proportions_ztest(count, nobs, alternative='two-sided')

print(f"P-value (P值): {pval:.4f}")

# 3. 结果解读 (面试话术)
alpha = 0.05 # 显著性水平通常设为 5%
print("\n--- 📝 结论判定 ---")
if pval < alpha:
    print("✅ 结果显著 (Significant)！")
    print(f"P值 ({pval:.4f}) 小于 0.05。")
    print("我们可以有 95% 的把握说：你的模型真的有效，不是运气。")
    print("老板，可以全量上线了！")
else:
    print("❌ 结果不显著 (Not Significant)。")
    print(f"P值 ({pval:.4f}) 大于 0.05。")
    print("虽然 B 组低了 0.7%，但这很可能是随机波动。")
    print("建议：继续观察，或者扩大样本量再测。")

# 4. 进阶：置信区间 (Confidence Interval)
# 老板不仅想知道“有没有效”，还想知道“到底能降多少？”
# 我们计算 (Rate_A - Rate_B) 的 95% 置信区间
# conf = sms.proportion_effectsize(rate_a, rate_b)
# print(f"\n---  效应量：{conf:.2f} ---")
# 这里手动算一下近似区间
se_diff = np.sqrt(rate_a*(1-rate_a)/n_a + rate_b*(1-rate_b)/n_b)
diff = rate_a - rate_b
ci_low = diff - 1.96 * se_diff
ci_high = diff + 1.96 * se_diff

print(f"\n--- 📊 95% 置信区间 ---")

print(f"我们有 95% 的信心认为，AI 模型能让流失率降低: [{ci_low:.2%} 到 {ci_high:.2%}]")



# 5. P7 级反击：事前样本量估算 (Power Analysis)

print("\n--- 5. 假如结果不显著，我们该怎么办？(Power Analysis) ---")

print("计算：为了检测出这 0.7% 的微弱优势，我们到底需要多少样本？")



# 设定目标

effect_size = sms.proportion_effectsize(0.105, 0.098) # 把流失率差异转化为效应量

power = 0.8  # 我们希望有 80% 的概率能检测出来 (行业标准)

alpha = 0.05 # 显著性水平



required_n = sms.NormalIndPower().solve_power(

    effect_size=effect_size, 

    power=power, 

    alpha=alpha, 

    ratio=1

)



print(f"需要样本量 (每组): {int(required_n)}")

print(f"当前样本量 (10,000) {'充足' if 10000 > required_n else '不足'}。")

if 10000 < required_n:

    print("💡 建议：实验不要停！请再跑一段时间，累积更多用户后再看。")
