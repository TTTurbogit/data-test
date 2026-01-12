import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import time
import platform
import matplotlib.font_manager as fm

# --- 0. 解决中文乱码 (Windows/Linux 自动适配) ---
system_name = platform.system()
if system_name == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif system_name == "Linux":
    # 尝试加载云端安装的 Noto 字体
    try:
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']
    except:
        pass
plt.rcParams['axes.unicode_minus'] = False 

# --- 1. 页面配置 ---
st.set_page_config(page_title="IBM 电信客户流失预警中台", layout="wide")

st.title("📡 客户流失预警中台 (基于 IBM 真实数据)")
st.markdown("---")

# --- 2. 核心引擎：读取真实数据并训练 ---
@st.cache_resource
def load_and_train():
    # A. 读取真实数据
    try:
        df = pd.read_csv('telco_churn.csv')
    except FileNotFoundError:
        st.error("找不到 'telco_churn.csv'，请先运行上一步的下载脚本！")
        return None, None, None

    # B. 硬核清洗
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

    # C. 特征选择 (只选业务最关心的 Top 特征，方便前端输入)
    # 我们把 Contract, InternetService 等分类变量转为 One-Hot
    selected_features = [
        'tenure', 'MonthlyCharges', 'TotalCharges', 
        'Contract', 'InternetService', 'OnlineSecurity', 'TechSupport'
    ]
    
    X_raw = df[selected_features]
    y = df['Churn']
    
    # One-Hot 编码 (记录下列名，确保预测时一致)
    X = pd.get_dummies(X_raw)
    model_columns = X.columns
    
    # D. 训练模型 (使用真实数据!)
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X, y)
    
    return model, model_columns, df

model, model_columns, df_raw = load_and_train()

if model is None:
    st.stop()

# --- 3. 侧边栏：真实业务场景输入 ---
st.sidebar.header("📝 客户画像录入")

# 数值型特征
tenure = st.sidebar.slider("网龄 (月)", 0, 72, 24, help="用户入网时长")
monthly_charges = st.sidebar.slider("月租费 (元)", 18, 120, 70, help="用户每月的套餐费用")
# 自动计算总费用 (TotalCharges) 以简化输入
total_charges = tenure * monthly_charges 

st.sidebar.markdown("---")
st.sidebar.subheader("业务办理情况")

# 类别型特征 (根据数据集里的真实选项)
contract = st.sidebar.selectbox("合约类型", ['Month-to-month', 'One year', 'Two year'])
internet_service = st.sidebar.selectbox("互联网接入类型", ['DSL', 'Fiber optic', 'No'])
online_security = st.sidebar.selectbox("是否开通网络安全", ['Yes', 'No', 'No internet service'])
tech_support = st.sidebar.selectbox("是否开通技术支持", ['Yes', 'No', 'No internet service'])

# --- 4. 预测逻辑 ---
if st.button("🚀 发起风险评估", type="primary"):
    with st.spinner('正在比对 7000+ 条真实历史记录...'):
        time.sleep(0.5)
        
        # A. 构造原始输入
        input_data = pd.DataFrame({
            'tenure': [tenure],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges],
            'Contract': [contract],
            'InternetService': [internet_service],
            'OnlineSecurity': [online_security],
            'TechSupport': [tech_support]
        })
        
        # B. 对齐特征 (One-Hot)
        # 关键步骤：必须和训练时的列完全一致，缺少的列补0
        input_encoded = pd.get_dummies(input_data)
        input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
        
        # C. 预测
        prob = model.predict_proba(input_encoded)[0][1]
        
        # --- 5. 结果展示 ---
        st.subheader("📊 评估报告")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric(label="流失概率", value=f"{prob:.1%}")
            
            if prob > 0.7:
                st.error("🔴 极高风险 (High Risk)")
                st.write("**主要原因推测：**")
                if contract == 'Month-to-month':
                    st.write("- **按月付费**：粘性极低，随时可走。")
                if internet_service == 'Fiber optic':
                    st.write("- **光纤用户**：通常对价格/质量更挑剔。")
                if tenure < 12:
                    st.write("- **新用户**：磨合期容易流失。")
                    
            elif prob > 0.3:
                st.warning("⚠️ 中等风险 (Medium Risk)")
            else:
                st.success("🟢 健康状态 (Low Risk)")

        with col2:
            # D. 真实分布对比图
            fig, ax = plt.subplots(figsize=(8, 4))
            # 画两个分布：所有人的月费 vs 流失人群的月费
            ax.hist(df_raw['MonthlyCharges'], bins=30, alpha=0.3, color='gray', label='全体用户')
            ax.hist(df_raw[df_raw['Churn']==1]['MonthlyCharges'], bins=30, alpha=0.5, color='red', label='历史流失用户')
            
            # 标出当前用户
            ax.axvline(monthly_charges, color='blue', linestyle='--', linewidth=2, label='当前用户')
            
            ax.set_title("月租费分布对比 (红色为高发流失区)")
            ax.set_xlabel("月租费 ($)")
            ax.legend()
            st.pyplot(fig)
            st.caption("注：红色区域越高，代表该价格段的历史流失人数越多。")

st.markdown("---")
with st.expander("🔍 开发者模式：查看 One-Hot 编码后的特征向量"):
    # 为了演示给面试官看，展示一下后台实际处理的数据格式
    input_data_demo = pd.DataFrame({
            'tenure': [tenure],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges],
            'Contract': [contract],
            'InternetService': [internet_service],
            'OnlineSecurity': [online_security],
            'TechSupport': [tech_support]
        })
    input_demo_encoded = pd.get_dummies(input_data_demo).reindex(columns=model_columns, fill_value=0)
    st.dataframe(input_demo_encoded)
