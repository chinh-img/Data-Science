import json
import re

# Read json file
with open("chat_history.json", "r", encoding="utf-8") as file:
    chat_data = json.load(file)
    
# Sentences count
total_messages = len(chat_data)
user_messages = [message for message in chat_data if message["role"] == "user"]
ai_messages = [message for message in chat_data if message["role"] == "assistant"]

print(f"Tổng số lượt chat: {total_messages}")
print(f"Bạn nói: {len(user_messages)} câu")
print(f"AI phản hồi: {len(ai_messages)} câu")

# Symbol count
user_chars = sum(len(m["content"]) for m in user_messages)
ai_chars = sum(len(m["content"]) for m in ai_messages)

print(f"\nTổng kí tự bạn đã gõ: {user_chars}")
print(f"Tổng kí tự AI đã trả lời: {ai_chars}")

# AI longest sentence
longest_ai = max(ai_messages, key=lambda m: m["content"])
print(f"\nCâu AI nói dài nhất ({len(longest_ai['content'])} ký tự):")
print(longest_ai["content"][:200] + "...")

# How many times AI used actions (*...*)
action_count = 0
for m in ai_messages:
    matches = re.findall(r"\*.*?\*", m["content"], flags=re.DOTALL)
    action_count += len(matches)
    
print(f"\nAI đã dùng ký hiệu hành động * * tổng cộng {action_count} lần.")