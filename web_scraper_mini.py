import requests # 导入这个超能力模块

print("--- 正在连接百度... ---")

# 发送一个网络请求
try:
    # 模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = "https://www.google.com"
    response = requests.get(url, headers=headers)
    
    # 设置编码，防止中文乱码
    response.encoding = 'utf-8'

    if response.status_code == 200:
        print("连接成功！")
        
        # 获取网页的全部源代码 (HTML)
        html_content = response.text
        with open("web_save.txt", "w", encoding="utf-8") as f:
            f.writelines(html_content) # 一次性写入多行
            print("写入完成！")
            # print("\n--- 网页预览 (前100个字符) ---")
        # print(html_content)
        
        # 简单的“提取标题”技巧
        # 寻找 <title> 标签的位置
    #     if '<span class="text" itemprop="text">' in html_content:
    #         start = html_content.find('<span class="text" itemprop="text">') + len('<span class="text" itemprop="text">')
    #         end = html_content.find("</span>")
    #         title = html_content[start:end]
    #         print(f"\n提取出的网页标题是: {title}")
        
    # else:
    #     print(f"连接失败，状态码: {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"网络好像断了哦")
finally:
    print(f"爬取任务结束")

