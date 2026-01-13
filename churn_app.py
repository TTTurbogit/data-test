import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import time
import platform
import matplotlib.font_manager as fm

# --- 0. 全局配置与字体适配 ---
st.set_page_config(page_title="电信 AI 智能营销中台", layout="wide")

# 解决中文乱码 (Windows/Linux 自动适配)
system_name = platform.system()
if system_name == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif system_name == "Linux":
    # 暴力搜寻法找中文字体
    try:
        font_files = fm.findSystemFonts(fontpaths=['/usr/share/fonts'])
        for file in font_files:
            if 'CJK' in file and ('SC' in file or 'Sim' in file or 'Noto' in file):
                fm.fontManager.addfont(file)
                plt.rcParams['font.sans-serif'] = [fm.FontProperties(fname=file).get_name()]
                break
    except:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans'] # 兜底
plt.rcParams['axes.unicode_minus'] = False 

# --- 1. 数据加载与模型训练核心 ---
@st.cache_resource
def init_system():
    # A. 读取真实数据
    try:
        df = pd.read_csv('telco_churn.csv')
    except:
        st.error("请先运行 real_world_churn.py 下载数据集！")
        return None, None, None, None

    # B. 清洗
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # C. 特征定义 (Top 7 核心业务特征)
    features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract', 'InternetService', 'OnlineSecurity', 'TechSupport']
    
    # D. 训练风险模型 (Churn Model)
    X = pd.get_dummies(df[features])
    model_cols = X.columns # 记录列顺序
    y = df['Churn']
    
    model_churn = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model_churn.fit(X, y)
    
    # E. 训练增益模型 (Uplift T-Learner)
    # 定义干预：Contract != Month-to-month (即：长约视为干预)
    df_control = df[df['Contract'] == 'Month-to-month'] # 对照组
    df_treated = df[df['Contract'] != 'Month-to-month'] # 实验组
    
    # 训练两个模型 (只用数值特征简化 T-Learner 可视化，防止维度爆炸)
    uplift_feats = ['tenure', 'MonthlyCharges', 'TotalCharges'] 
    
    m_control = RandomForestClassifier(n_estimators=100, random_state=42)
    m_control.fit(df_control[uplift_feats], df_control['Churn'])
    
    m_treated = RandomForestClassifier(n_estimators=100, random_state=42)
    m_treated.fit(df_treated[uplift_feats], df_treated['Churn'])
    
    # 预先计算全量数据的 Uplift 用于画图
    df['Uplift_Score'] = m_control.predict_proba(df[uplift_feats])[:,1] - m_treated.predict_proba(df[uplift_feats])[:,1]
    
    return df, model_churn, model_cols, (m_control, m_treated)

df_raw, model_churn, model_cols, uplift_models = init_system()
m_control, m_treated = uplift_models

if df_raw is None:
    st.stop()

st.title("🚀 电信客户全生命周期管理中台")
st.markdown("**集成模块：** ⚠️ 流失风险预测 | 🎯 营销增益分析 (Uplift) | 👁️ 全局数据洞察")

# --- 2. 侧边栏：统一特征录入 ---
st.sidebar.header("👤 当前客户画像")

# 数值特征
tenure = st.sidebar.slider("网龄 (月)", 0, 72, 24)
monthly_charges = st.sidebar.slider("月租费 ($)", 18, 120, 85)
total_charges = tenure * monthly_charges # 自动计算

st.sidebar.markdown("---")
# 类别特征
contract = st.sidebar.selectbox("合约类型", ['Month-to-month', 'One year', 'Two year'])
internet = st.sidebar.selectbox("互联网类型", ['Fiber optic', 'DSL', 'No'])
security = st.sidebar.selectbox("网络安全服务", ['No', 'Yes', 'No internet service'])
tech_support = st.sidebar.selectbox("技术支持服务", ['No', 'Yes', 'No internet service'])

# 构造输入数据 DataFrame
input_base = pd.DataFrame({
    'tenure': [tenure], 'MonthlyCharges': [monthly_charges], 'TotalCharges': [total_charges],
    'Contract': [contract], 'InternetService': [internet], 
    'OnlineSecurity': [security], 'TechSupport': [tech_support]
})

# --- 3. 主界面 Tabs ---
tab1, tab2 = st.tabs(["⚠️ 风险预测 (Risk)", "💰 增益分析 (Uplift)"])

# ========== TAB 1: 风险预测 ==========
with tab1:
    col_kpi, col_viz = st.columns([1, 2])
    
    # 1.1 实时预测
    input_encoded = pd.get_dummies(input_base).reindex(columns=model_cols, fill_value=0)
    prob_churn = model_churn.predict_proba(input_encoded)[0][1]
    
    with col_kpi:
        st.subheader("流失风险评估")
        st.metric("流失概率", f"{prob_churn:.1%}")
        
        if prob_churn > 0.7:
            st.error("🔴 极高风险")
            st.write("建议：立即启动人工关怀流程。")
        elif prob_churn > 0.4:
            st.warning("⚠️ 中等风险")
            st.write("建议：关注其流量使用情况。")
        else:
            st.success("🟢 健康状态")
            st.write("建议：维持现状。")

    with col_viz:
        st.subheader("📊 数据分布诊断")
        # 1.2 月租费分布对比图 (修复图例错乱问题)
        fig, ax = plt.subplots(figsize=(8, 3.5))
        
        # 关闭 seaborn 自带图例，改用手动构建
        sns.histplot(df_raw, x='MonthlyCharges', hue='Churn', kde=True, 
                     palette={0:'gray', 1:'red'}, element="step", ax=ax, legend=False)
        
        # 画当前用户的线
        ax.axvline(monthly_charges, color='blue', linestyle='--', linewidth=2)
        
        # --- 手动构建精准图例 ---
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        
        legend_elements = [
            Line2D([0], [0], color='blue', linestyle='--', lw=2, label='当前用户 (You)'),
            Patch(facecolor='red', alpha=1, label='历史流失 (Churn)'),
            Patch(facecolor='gray', alpha=1, label='历史留存 (Retain)')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right')
        ax.set_title("月租费与历史流失人群对比")
        st.pyplot(fig)
    
    st.markdown("---")
    # 1.3 开发者模式 (One-Hot 向量展示)
    with st.expander("🔍 开发者模式：查看 One-Hot 特征向量"):
        st.write("模型实际接收到的稀疏矩阵向量：")
        st.dataframe(input_encoded.style.highlight_max(axis=1))

# ========== TAB 2: Uplift 增益分析 ==========
with tab2:
    st.subheader("📈 营销干预增益分析 (Causal Inference)")
    
    # 2.1 计算 Uplift
    # 我们对比：保持现状(Control) vs 转化为长约(Treated)
    # 注意：这里我们只用数值特征进 T-Learner，方便展示
    input_uplift = pd.DataFrame({'tenure':[tenure], 'MonthlyCharges':[monthly_charges], 'TotalCharges':[total_charges]})
    
    p_control = m_control.predict_proba(input_uplift)[0][1] # 不干预(Month-to-month)的流失率
    p_treated = m_treated.predict_proba(input_uplift)[0][1] # 干预后(Two-year)的流失率
    uplift_val = p_control - p_treated
    
    # 2.2 增益可视化 (KPI)
    c1, c2, c3 = st.columns(3)
    c1.metric("自然流失率 (基线)", f"{p_control:.1%}", help="如果不做任何干预，用户流失的概率")
    c2.metric("干预后流失率", f"{p_treated:.1%}", help="如果成功引导签长约，用户流失的概率")
    c3.metric("营销增益 (Uplift)", f"{uplift_val:.1%}", delta_color="normal", help="干预带来的风险降低幅度")

    # 2.3 干预效果对比图
    st.markdown("#### 干预效果模拟")
    fig_bar, ax_bar = plt.subplots(figsize=(6, 2))
    bars = ax_bar.barh(['不干预', '推销长约'], [p_control, p_treated], color=['gray', '#2ecc71'])
    ax_bar.set_xlim(0, 1)
    ax_bar.set_xlabel("流失概率")
    ax_bar.bar_label(bars, fmt='%.1f%%')
    st.pyplot(fig_bar)

    st.markdown("---")
    
    # 2.4 全局 Uplift 分布图 (P7级大杀器)
    st.subheader("🗺️ 全局营销价值定位 (Uplift Distribution)")
    st.caption("下图展示了全量用户的营销价值分布。红色越深代表‘挽留价值’越高。五角星 ★ 代表当前用户位置。")
    
    fig_up, ax_up = plt.subplots(figsize=(10, 5))
    # 画背景：全量用户的散点图
    sc = ax_up.scatter(df_raw['tenure'], df_raw['MonthlyCharges'], 
                       c=df_raw['Uplift_Score'], cmap='RdBu_r', 
                       alpha=0.6, s=15, label='历史用户')
    
    # 画当前用户：五角星
    ax_up.scatter([tenure], [monthly_charges], color='gold', s=300, marker='*', edgecolors='black', label='当前用户')
    
    plt.colorbar(sc, label='营销增益 (Uplift Score)')
    ax_up.set_xlabel("网龄 (Tenure)")
    ax_up.set_ylabel("月租费 (Monthly Charges)")
    ax_up.set_title("谁值得被挽留？(Uplift 画像定位)")
    ax_up.legend()
    
    st.pyplot(fig_up)
    
    # 2.5 策略建议
    if uplift_val > 0.3:
        st.success(f"💎 **高潜用户**：该用户位于 Uplift 红色高值区！挽留成功率极高，建议提供 **30% 折扣换取年费合约**。")
    elif uplift_val > 0.1:
        st.warning(f"⚖️ **摇摆用户**：有一定挽留价值，建议发送关怀短信。")
    else:
        st.info(f"💤 **低效用户**：干预效果不明显（可能是铁粉或死敌），建议节省预算。")

st.sidebar.markdown("---")
st.sidebar.caption("Powered by XGBoost & T-Learner")
