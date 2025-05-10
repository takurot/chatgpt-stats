# ChatGPT Question Counter Script

This script analyzes your `conversations.json` file—exported from OpenAI ChatGPT—to count the total number of **user questions** and determine the **time span** of your usage.

---

## 📁 File Structure

```

.
├── conversations.json      ← Exported from ChatGPT's data export feature
├── count\_questions.py      ← Python script for question analysis
└── README.md               ← This documentation

````

---

## 🚀 How to Use

### 1. Export ChatGPT Conversation Data

1. In ChatGPT, go to **Settings → Data Controls → Export Data**
2. You'll receive an email with a ZIP download link
3. Extract the ZIP and locate `conversations.json`
4. Place `conversations.json` in the same directory as the script

### 2. Run the Script

```bash
python count_questions.py
```

---

## 🖥️ Example Output

```
✅ Total number of questions you asked ChatGPT: 532
🕰️ Time span: 2023-08-10 14:35:21 to 2025-05-09 21:55:02
📅 Total duration: 639 days
```

---

## 📦 Requirements

* Python 3.6 or higher
* No external libraries required (only standard Python libraries)

---

## 🧠 Script Overview

* Parses the `mapping` section of each conversation in `conversations.json`
* Extracts messages where `author.role == "user"`
* If `content.parts` contains any non-empty string, it's counted as a question
* Uses `create_time` to determine the first and last question timestamps

---

## 🔥 Key Features

- Visualize the number of questions per month as a bar graph (`questions_per_month.png`)
- Histogram of the number of turns per conversation (user + assistant) (`conversation_turns_histogram.png`)
- Heatmap showing the correlation between question and answer length (`qa_length_heatmap.png`)
- All graphs are automatically saved as PNG files
- These visualizations require the `matplotlib` and `numpy` libraries

---

## 💡 Extensions (Optional)

You can extend the script to:

* Visualize monthly question counts as a bar graph
* Show the distribution of conversation turns as a histogram
* Analyze the correlation between question and answer length (heatmap)
* Export question data to CSV
* Calculate average questions per day
* Visualize trends using graphs (e.g., with `matplotlib`)

---

## 📝 License

MIT License
