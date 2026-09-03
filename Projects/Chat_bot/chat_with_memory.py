import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Không tìm thấy Open Router key trong .env")

# Choose model
MODEL = "inclusionai/ling-3.0-flash-fin:free"

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

print("Bot chị Ishimi đã sẵn sàng. Nhập 'exit' để thoát.\n")

# Chat
while True:
    user_input = input("Bạn: ")
    
    if user_input.lower() == "exit":
        print("Chị: Thôi, hôm nay đến đây tới đây nhé. Về ngủ sớm đi nhóc!")
        break
    
    # Add user's text to history
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
    chat_history.append({"role": "assistant", "content": ai_reply})
    
    # Print results
    print(f"Chị: {ai_reply}\n")