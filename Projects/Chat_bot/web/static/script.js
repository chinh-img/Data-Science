const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function addMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("msg", role);

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = text;

    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function loadHistory() {
    try {
        const response = await fetch("http://127.0.0.1:8000/history");
        const history = await response.json();

        history.forEach(item => {
            addMessage(item.role, item.content);
        });
    } catch (error) {
        console.error("Không tải được lịch sử:", error);
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage("user", message);
    userInput.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        addMessage("assistant", data.reply);
    } catch (error) {
        addMessage("assistant", "Lỗi kết nối tới server.");
    }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

// Gọi khi mở trang
loadHistory();