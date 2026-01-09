import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time
import matplotlib.pyplot as plt

# --- 1. 页面配置 ---
st.set_page_config(page_title="电信用户流失预警系统", layout="wide")

st.title("🔮 电信用户流失预测系统 (P6+ 诊断版)")
st.markdown("---")

# --- 2. 幕后模型 (逻辑加固) ---
@st.cache_resource
def train_model():
    # 模拟数据
    np.random.seed(42)
    n = 2000 # 增加数据量
    df = pd.DataFrame({
        '月租费': np.random.normal(100, 20, n),
        '流量': np.random.normal(10, 5, n),
        '网龄': np.random.randint(1, 72, n),
        '有合约': np.random.choice([0, 1], n)
    })
    
    # 规则加固：确保单调性
    df['流失概率'] = 0.1 # 基础概率
    df.loc[(df['有合约'] == 0) & (df['月租费'] > 120), '流失概率'] = 0.6
    df.loc[(df['有合约'] == 0) & (df['月租费'] > 160), '流失概率'] = 0.9
    
    # 生成标签
    df['流失'] = df['流失概率'].apply(lambda p: np.random.choice([0, 1], p=[1-p, p]))
    
    X = df[['月租费', '流量', '网龄', '有合约']]
    y = df['流失']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, df # 返回 df 用于画图

model, train_df = train_model()

# --- 3. 侧边栏 ---
st.sidebar.header("📝 输入用户特征")
monthly_fee = st.sidebar.slider("月租费 (元)", 50, 200, 100)
data_usage = st.sidebar.slider("每月流量 (GB)", 0, 50, 10)
tenure = st.sidebar.slider("网龄 (月)", 1, 120, 24)
contract = st.sidebar.radio("是否有合约?", ["无合约", "有合约"])
contract_val = 1 if contract == "有合约" else 0

# --- 4. 预测逻辑 ---
if st.button("🚀 开始预测", type="primary"):
    with st.spinner('AI 正在分析...'):
        time.sleep(0.5)
        
        input_data = pd.DataFrame([[monthly_fee, data_usage, tenure, contract_val]], 
                                  columns=['月租费', '流量', '网龄', '有合约'])
        
        prob = model.predict_proba(input_data)[0][1]
        
        # --- 5. 结果展示 ---
        st.subheader("分析结果")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.metric(label="当前用户流失概率", value=f"{prob:.1%}")
            if prob > 0.7:
                st.error("🔴 高风险警告！")
            elif prob > 0.4:
                st.warning("⚠️ 中等风险。")
            else:
                st.success("🟢 优质客户。")

        with col2:
            # 可视化数据分布
            fig, ax = plt.subplots(figsize=(6, 2))
            ax.hist(train_df['月租费'], bins=50, alpha=0.6, color='skyblue', label='训练集分布')
            ax.axvline(monthly_fee, color='red', linestyle='--', label='当前用户')
            ax.set_title("月租费分布诊断图")
            ax.legend()
            st.pyplot(fig)
            st.caption("红线代表您当前输入的值。如果红线处于数据稀疏区，模型预测可能不准。")
            
st.markdown("---")
# --- 底部：模型解释 ---
with st.expander("📊 查看模型内部逻辑 (Feature Importance)"):
    importances = pd.DataFrame({
        'feature': ['月租费', '流量', '网龄', '有合约'],
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    st.bar_chart(importances.set_index('feature'))