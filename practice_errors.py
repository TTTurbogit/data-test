def safe_divide():
    try:
        # 1. 尝试执行可能会出错的代码
        num1 = float(input("请输入被除数: "))
        num2 = float(input("请输入除数: "))
        
        result = num1 / num2
        print(f"结果是: {result}")

    except ValueError:
        # 2. 如果用户输入的不是数字
        print("错误：请输入有效的数字！")

    except ZeroDivisionError:
        # 3. 如果除数是 0
        print("错误：除数不能为 0！")

    except Exception as e:
        # 4. 其他任何未知的错误
        print(f"发生了意外错误: {e}")

    finally:
        # 5. 无论是否报错，最后都会执行（通常用于清理工作）
        print("--- 计算结束 ---")

# 运行测试
safe_divide()
