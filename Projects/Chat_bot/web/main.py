import os
import requests
import uvicorn
import json
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Load API_KEY
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Select Model
MODEL = "inclusionai/ling-3.0-flash-fin:free"

app = FastAPI(title="Ishimi Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates (HTML)
templates = Jinja2Templates(directory="templates")

SYSTEM_PROMPT = (
    "Em là một đàn chị tomboy tên là Ishimi Yokoyama hiện là học sinh năm hai tại trường, tóc mullet, giọng trầm, "
    "tính cách mạnh mẽ nhưng biết quan tâm. "
    "Có 1 cậu đàn em học năm nhất mới vào trường tên là Izumi Kurose. "
    "Cả hai người đã thân với nhau qua các giờ nghỉ trưa của trường và qua phòng y tế - nơi mà cả 2 thường dọn dẹp giúp cô y tế trong trường. "
    "Hôm nay vào giờ nghỉ trưa thì thấy Izumi đi với 1 cô gái khác trong giờ nghỉ trưa nên lần đầu tiên cảm thấy khó chịu - ghen, "
    "đợi đến khi học sinh ra về, Izumi đến phòng y tế và thấy Ishimi ngồi đó với khuôn mặt khá căng thẳng. "
    "Hãy nói chuyện bằng giọng trêu chọc nhẹ nhàng nhưng trưởng thành và có phần chiếm hữu. "
)

# File lưu log
LOG_FILE = "../chat_log.json"


def load_log():
    global log_data
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f) or []
    return []


def save_log():
    with open(LOG_FILE, 'w', encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
        
log_data = load_log()
# Lịch sử chat
chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]
for item in log_data:
    chat_history.append({"role": item["role"], "content": item["content"]})

# Định nghĩa body request
class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history")
async def history():
    return JSONResponse(content=log_data)

@app.post("/chat")
async def chat(req: ChatRequest):
    global log_data
    
    user_message = req.message.strip()
    if not user_message:
        return {"reply": "Nhóc chưa nhập gì cả."}

    # Thêm tin nhắn người dùng
    chat_history.append({"role": "user", "content": user_message})

    # Gọi OpenRouter
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": chat_history,
            "temperature": 0.8
        }
    )

    if response.status_code == 200:
        ai_reply = response.json()["choices"][0]["message"]["content"]
    else:
        ai_reply = f"Lỗi {response.status_code}: {response.text}"

    # Lưu lịch sử
    chat_history.append({"role": "assistant", "content": ai_reply})
    
    # Lưu log có timestamp
    log_data.append({
        "role": "user",
        "content": user_message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    log_data.append({
        "role": "assistant",
        "content": ai_reply,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    save_log()

    return {"reply": ai_reply}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)