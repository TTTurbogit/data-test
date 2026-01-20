import streamlit as st
import time

# --- 页面配置 ---
st.set_page_config(page_title="AdminPortal Login", page_icon="🔐", layout="centered")

# --- 玻璃拟态 (Glassmorphism) CSS 样式 ---
st.markdown("""
<style>
    /* 1. 全局背景：深邃的渐变色，突显玻璃效果 */
    .stApp {
        background-image: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        background-attachment: fixed;
        background-size: cover;
        font-family: 'Fira Sans', sans-serif;
    }

    /* 2. 隐藏 Streamlit 默认的 Header 和 Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. 登录卡片容器 */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.1);  /* 稍微加深白色透明度 */
        backdrop-filter: blur(25px);           /* 增加模糊度 */
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15); 
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        padding: 40px;
        margin-top: 50px;
    }

    /* 4. 标题样式 */
    h1 {
        color: #FFFFFF !important;
        text-align: center;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 10px !important;
    }
    
    .login-subtitle {
        color: rgba(255, 255, 255, 0.8) !important;
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }

    /* 5. 输入框样式重写 */
    div[data-baseweb="input"] {
        background-color: rgba(0, 0, 0, 0.2) !important; /* 背景改用深色半透明，增加对比 */
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* 聚焦时的边框 */
    div[data-baseweb="input"]:focus-within {
        border-color: #3B82F6 !important;
    }

    /* 输入框内的文字颜色 */
    input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important; /* 兼容部分浏览器 */
    }
    
    /* Placeholder 颜色 */
    input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Label 颜色：使用高亮的浅蓝/白，确保在深色背景下可见 */
    .stMarkdown label p {
        color: #60A5FA !important; 
        font-weight: 600 !important;
        font-size: 14px;
        margin-bottom: 8px;
    }

    /* 6. 按钮样式重写 */
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important;
        border: none !important;
        color: white !important;
        padding: 10px 24px !important;
        text-align: center !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-size: 16px !important;
        margin: 4px 2px !important;
        cursor: pointer !important;
        border-radius: 12px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        background: linear-gradient(90deg, #5b7cc7 0%, #283858 100%) !important;
    }

    /* 错误/成功消息样式 */
    .stAlert {
        background-color: rgba(255, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 0, 0, 0.2);
        color: white;
    }
    
</style>
""", unsafe_allow_html=True)

# --- 逻辑部分 ---

# 初始化 Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    # 模拟验证
    if st.session_state.username == "admin" and st.session_state.password == "password":
        st.session_state['logged_in'] = True
        st.success("登录成功！正在跳转...")
        time.sleep(1)
        st.rerun()
    else:
        st.error("用户名或密码错误 (试一下 admin / password)")

def logout():
    st.session_state['logged_in'] = False
    st.rerun()

# --- 界面渲染 ---

if not st.session_state['logged_in']:
    # --- 登录页视图 ---
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 使用 Form 容器来应用我们的 CSS 样式
        with st.form("login_form"):
            st.title("Admin Portal")
            st.markdown("<div class='login-subtitle'>请登录您的管理控制台</div>", unsafe_allow_html=True)
            
            st.text_input("用户名", key="username", placeholder="输入 admin")
            st.text_input("密码", type="password", key="password", placeholder="输入 password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("登 录")
            
            if submit:
                login()
                
else:
    # --- 登录后视图 (Dashboard) ---
    st.markdown("""
        <style>
            /* 登录后切换为专业且清爽的后台配色 */
            .stApp {
                background: #F8FAFC !important;
            }
            [data-testid="stHeader"] {visibility: visible;}
            
            /* 调整文字颜色回深色，确保可读性 */
            h1, h2, h3, p, span, label {
                color: #1E293B !important;
            }
            
            /* 侧边栏样式 */
            [data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0;
            }
            
            /* 指标卡片背景 */
            [data-testid="stMetricValue"] {
                color: #3B82F6 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.title("导航")
    st.sidebar.button("退出登录", on_click=logout)
    
    st.title(f"👋 欢迎回来, {st.session_state.username}")
    st.markdown("---")
    
    # 简单的卡片布局
    m1, m2, m3 = st.columns(3)
    m1.metric("今日活跃用户", "1,234", "+5%")
    m2.metric("总销售额", "¥ 45,231", "-2%")
    m3.metric("系统状态", "正常", "100%")
    
    st.info("💡 提示：这是一个玻璃拟态风格的登录演示。实际项目中请连接数据库进行验证。")
    
    # 这里可以整合您之前的绘图代码
    st.subheader("📊 快速概览")
    import pandas as pd
    import numpy as np
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

