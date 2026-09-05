import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Không tìm thấy Open Router key trong .env")

# Choose model
MODEL = "inclusionai/ling-3.0-flash-fin:free"
LOG_FILE = "chat_log.json"

# System prompt
system_prompt = (
    "Em là một đàn chị tomboy tên là Ishimi Yokoyama, tóc mullet, giọng trầm, "
    "tính cách mạnh mẽ nhưng biết quan tâm. "
    "Hãy nói chuyện bằng giọng trêu chọc nhẹ nhàng nhưng trưởng thành. "
    "Khi nói chuyện, hãy nhớ những gì người dùng đã nói trước đó."
)

# Chat history
chat_history = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": "Dạ vâng, em hiểu rồi ạ."},
]

# Danh sách log (có stamp)
log_data = []

def save_log():
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(log_data, file, ensure_ascii=False, indent=2)
    print(f"\nĐã lưu log vào {LOG_FILE}")

print("Bot chị Ishimi đã sẵn sàng. Nhập 'exit' để thoát.\n")

# Chat
while True:
    user_input = input("Bạn: ")
    
    if user_input.lower() == "exit":
        save_log()
        print("Chị: Tạm biệt, mai gặp lại nha!")
        break
    
    # Add user's text to history
    user_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data.append({"role": "user", "content": user_input, "time": user_time})
    chat_history.append({"role": "user", "content": user_input})
    
    # Give all chat history to AI
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json= {
            "model": MODEL,
            "messages": chat_history,
            "temperature": 0.8
        }
    )
    
    if response.status_code == 200:
        # Take the reply
        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]
    else:
        ai_reply = f"Lỗi {response.status_code}: {response.text}"
    
    # Add chat's msg to history
    ai_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data.append({"role": "assistant", "content": ai_reply, "time": ai_time})
    chat_history.append({"role": "assistant", "content": ai_reply})
    
    # Print results
    print(f"Chị: {ai_reply}\n")