import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置页面
st.set_page_config(page_title="通用数据分析助手", page_icon="📂", layout="wide")

# 支持中文绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False 

st.title("📂 CSV 数据自助分析工具")
st.markdown("---")

# --- STEP 1: 文件上传区域 ---
with st.sidebar:
    st.header("1. 上传数据")
    # accept_multiple_files=False: 一次只处理一个文件
    uploaded_file = st.file_uploader("请拖入 CSV 文件", type=["csv"])
    
    st.info("提示：请确保 CSV 里至少包含数值类型的列，否则画不出图哦。")

# --- STEP 2: 判断是否有文件 ---
if uploaded_file is not None:
    # A. 读取用户上传的文件
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"成功加载文件！包含 {df.shape[0]} 行，{df.shape[1]} 列数据。")
        
        # B. 数据预览区
        with st.expander("点击预览原始数据", expanded=True):
            st.dataframe(df.head(50)) # 只展示前50行，防止浏览器卡顿
            
        st.markdown("---")
        
        # C. 交互式绘图区
        st.header("2. 探索性分析")
        
        # 布局：左边选 X 轴，右边选 Y 轴
        col1, col2, col3 = st.columns(3)
        
        # 获取所有列名
        columns = df.columns.tolist()
        
        with col1:
            x_axis = st.selectbox("选择 X 轴 (分类/时间)", columns, index=0)
        with col2:
            # 智能一点：默认选最后一个列作为 Y 轴
            y_axis = st.selectbox("选择 Y 轴 (数值)", columns, index=len(columns)-1)
        with col3:
            chart_type = st.radio("图表类型", ["柱状图 (Bar)", "折线图 (Line)", "散点图 (Scatter)"])

        # D. 开始画图
        st.subheader(f"📊 {x_axis} vs {y_axis}")
        
        # 创建画布
        fig, ax = plt.subplots(figsize=(10, 5))
        
        if chart_type == "柱状图 (Bar)":
            sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax, palette="viridis")
        elif chart_type == "折线图 (Line)":
            sns.lineplot(x=x_axis, y=y_axis, data=df, ax=ax, marker="o")
        else:
            sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax, s=100, color="purple")
            
        # 优化坐标轴标签（防止重叠）
        plt.xticks(rotation=45)
        
        # 在 Streamlit 中展示 Matplotlib 的图
        st.pyplot(fig)
        
        # E. 基础统计
        st.markdown("### 📈 核心统计指标")
        # 只计算数值列
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if not numeric_df.empty:
            st.write(numeric_df.describe())
        else:
            st.warning("表格里好像没有数字，没法做统计分析...")

    except Exception as e:
        st.error(f"解析文件失败，请检查格式是否正确。错误信息: {e}")

else:
    # 如果没上传文件，显示这个
    st.markdown("""
    ### 👋 欢迎使用！
    还没有数据？您可以：
    1. 下载这份 [测试数据 (Titanic)](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv)
    2. 将它拖到左侧的上传框中。
    3. 立刻开始分析！
    """)