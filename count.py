import json
from datetime import datetime

def count_user_questions(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    question_count = 0
    timestamps = []

    for conversation in data:
        mapping = conversation.get("mapping", {})
        for node_id, node in mapping.items():
            message = node.get("message")
            if message:
                author = message.get("author", {})
                if author.get("role") == "user":
                    content_parts = message.get("content", {}).get("parts", [])
                    if isinstance(content_parts, list):
                        for part in content_parts:
                            if isinstance(part, str) and part.strip():
                                question_count += 1
                                create_time = message.get("create_time")
                                if isinstance(create_time, (int, float)):
                                    timestamps.append(create_time)
                                break

    if timestamps:
        start_time = datetime.fromtimestamp(min(timestamps))
        end_time = datetime.fromtimestamp(max(timestamps))
        duration_days = (end_time - start_time).days + 1  # 端数を含めて+1日

        print(f"✅ ChatGPTでの質問数: {question_count} 件")
        print(f"🕰️ 質問期間: {start_time.strftime('%Y-%m-%d %H:%M:%S')} ～ {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 全体の期間: {duration_days} 日間")
    else:
        print("ユーザーの質問が見つかりませんでした。")

# 実行
count_user_questions("conversations.json")
