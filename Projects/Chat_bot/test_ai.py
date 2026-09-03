import os
import requests
from dotenv import load_dotenv

# LOAD API key from .env file
#TODO: Ko bao giờ được gián API key trực tiếp vào code, phải qua file .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Chưa tìm thấy OPENROUTER_API_KEY trong file .env")

# Choose AI model
MODEL = "inclusionai/ling-3.0-flash-fin:free"

# Prompt system
system_prompt = (
    "Em là một đàn chị tomboy, tóc mullet, giọng trầm, "
    "tính cách mạnh mẽ nhưng biết quan tâm người khác. "
    "Hãy nói chuyện bằng giọng trêu chọc nhẹ nhàng nhưng trưởng thành."
)

user_message = "Chào chị, hôm nay em mới đi học về, ngày hôm nay của chị thế nào?"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.8
    }
)

if response.status_code == 200:
    data = response.json()
    reply = data["choices"][0]["message"]["content"]
    print("AI trả lời:")
    print(reply)
else:
    print(f"Lỗi: {response.status_code}")
    print(response.text)