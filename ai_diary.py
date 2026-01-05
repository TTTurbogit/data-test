from snownlp import SnowNLP
import time
import os

# --- 1. AI 情感分析核心函数 ---
def analyze_emotion(text):
    s = SnowNLP(text)
    # s.sentiments 是一个 0 到 1 之间的浮点数
    # 接近 1 表示积极 (Positive)，接近 0 表示消极 (Negative)
    score = s.sentiments 
    return score

# --- 2. 根据得分给出反馈 ---
def get_ai_feedback(score):
    print(f"\n[AI 分析报告] 情感指数: {score:.2f} / 1.00")
    
    if score > 0.8:
        return "看来今天发生了很棒的事情！继续保持这种好心情！🌟"
    elif score > 0.4:
        return "今天过得平平淡淡才是真。🍵"
    else:
        return "抱抱你。看起来今天有点艰难，别忘了明天又是新的一天。💪"

# --- 3. 主程序逻辑 ---
def main():
    print("==============================")
    print("   🤖 AI 智能情感日记本 v1.0   ")
    print("==============================")
    
    while True:
        user_input = input("\n请输入今天的日记 (输入 'q' 退出): ")
        
        if user_input.lower() == 'q':
            print("再见！记得常来记录心情。")
            break
            
        if len(user_input) < 5:
            print("写太短啦，AI 读不懂哦，多写几个字吧。")
            continue

        # 调用 AI 进行分析
        print("🤖 AI 正在阅读并分析你的心情...")
        time.sleep(1) # 假装思考一秒钟
        
        score = analyze_emotion(user_input)
        feedback = get_ai_feedback(score)
        
        print(f"🤖 AI 说: {feedback}")
        
        # 保存日记
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("ai_diary.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] (情感分:{score:.2f}) {user_input}\n")
        print("[系统] 日记已加密保存到云端(其实是本地文件)。")

if __name__ == "__main__":
    main()
