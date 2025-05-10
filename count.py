import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import matplotlib.colors as mcolors

def count_user_questions(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    question_count = 0
    timestamps = []
    month_list = []

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
                                    month_str = datetime.fromtimestamp(create_time).strftime('%Y-%m')
                                    month_list.append(month_str)
                                break

    if timestamps:
        start_time = datetime.fromtimestamp(min(timestamps))
        end_time = datetime.fromtimestamp(max(timestamps))
        duration_days = (end_time - start_time).days + 1  # +1 day to include both ends

        print(f"Total questions: {question_count}")
        print(f"Period: {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total days: {duration_days}")

        # Count questions per month
        month_counter = Counter(month_list)
        sorted_months = sorted(month_counter.keys())
        counts = [month_counter[month] for month in sorted_months]

        # Plot
        plt.figure(figsize=(10, 5))
        plt.bar(sorted_months, counts, color='skyblue')
        plt.xlabel('Month')
        plt.ylabel('Number of Questions')
        plt.title('Number of ChatGPT Questions per Month')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('questions_per_month.png')
        print('Saved monthly question count graph as questions_per_month.png')
    else:
        print("No user questions found.")

    # 会話ごとのターン数を集計
    turn_counts = []
    for conversation in data:
        mapping = conversation.get("mapping", {})
        turn_count = 0
        for node_id, node in mapping.items():
            message = node.get("message")
            if message:
                author = message.get("author", {})
                if author.get("role") in ("user", "assistant"):
                    content_parts = message.get("content", {}).get("parts", [])
                    if isinstance(content_parts, list):
                        for part in content_parts:
                            if isinstance(part, str) and part.strip():
                                turn_count += 1
                                break
        if turn_count > 0:
            turn_counts.append(turn_count)

    # ヒストグラム用にターン数を調整（奇数なら-1して偶数に）
    adjusted_turn_counts = []
    for count in turn_counts:
        if count % 2 == 1:
            adjusted_turn_counts.append(count - 1)
        else:
            adjusted_turn_counts.append(count)

    # ヒストグラムを描画
    if adjusted_turn_counts:
        plt.figure(figsize=(8, 5))
        plt.hist(adjusted_turn_counts, bins=range(0, max(adjusted_turn_counts)+2, 2), color='orange', edgecolor='black', align='left')
        plt.xlabel('Number of Turns per Conversation (even)')
        plt.ylabel('Number of Conversations')
        plt.title('Histogram of Conversation Turns (even bins)')
        plt.tight_layout()
        plt.savefig('conversation_turns_histogram.png')
        print('Saved histogram of conversation turns as conversation_turns_histogram.png')

    # 質問と回答の文字数ペアを収集
    qa_lengths = []
    def get_create_time(node):
        msg = node.get('message') if node else None
        t = msg.get('create_time', 0) if isinstance(msg, dict) else 0
        return t if isinstance(t, (int, float)) and t is not None else 0

    for conversation in data:
        mapping = conversation.get("mapping", {})
        # ノードIDで昇順ソート（時系列順）
        sorted_nodes = sorted(
            ((k, v) for k, v in mapping.items() if v is not None),
            key=lambda x: get_create_time(x[1])
        )
        prev_question_len = None
        for node_id, node in sorted_nodes:
            message = node.get("message")
            if not message:
                continue
            author = message.get("author", {})
            content_parts = message.get("content", {}).get("parts", [])
            if not (isinstance(content_parts, list) and content_parts):
                continue
            text = str(content_parts[0]).strip()
            if not text:
                continue
            if author.get("role") == "user":
                prev_question_len = len(text)
            elif author.get("role") == "assistant" and prev_question_len is not None:
                answer_len = len(text)
                qa_lengths.append((prev_question_len, answer_len))
                prev_question_len = None

    # ヒートマップ描画
    if qa_lengths:
        q_lens, a_lens = zip(*qa_lengths)
        # question lengthは90パーセンタイル、answer lengthは95パーセンタイルで最大値を決定
        q_max = int(np.percentile(q_lens, 90))
        a_max = int(np.percentile(a_lens, 95))
        q_bins = np.arange(0, q_max + 25, 25)
        a_bins = np.arange(0, a_max + 50, 50)
        heatmap, xedges, yedges = np.histogram2d(
            np.clip(q_lens, 0, q_max),
            np.clip(a_lens, 0, a_max),
            bins=[q_bins, a_bins]
        )
        plt.figure(figsize=(8, 6))
        plt.imshow(
            heatmap.T, origin='lower', aspect='auto',
            extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
            cmap='YlOrRd', norm=mcolors.LogNorm(vmin=1, vmax=heatmap.max())
        )
        plt.colorbar(label='Count (log scale)')
        plt.xlabel('Question Length (chars)')
        plt.ylabel('Answer Length (chars)')
        plt.title('Heatmap of Question vs. Answer Length')
        plt.tight_layout()
        plt.savefig('qa_length_heatmap.png')
        print('Saved heatmap of question vs. answer length as qa_length_heatmap.png')

# Run
count_user_questions("conversations.json")
