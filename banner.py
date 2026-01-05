import pyfiglet # 导入这个新安装的库

def create_banner(text):
    # 使用 figlet 库将文字转换成艺术字
    # slant 是字体样式
    banner = pyfiglet.figlet_format(text, font="slant")
    print(banner)

# 让用户输入想显示的文字
my_text = "PYTHON PRO"
print(f"--- 正在为 {my_text} 生成艺术字 ---")

create_banner(my_text)
