import gradio as gr
import sqlite3
import os
import requests

DB_PATH = os.path.join(os.path.dirname(__file__), "quotes.db")

# =========================
# GET QUOTES
# =========================
def get_quotes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text, author FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    result = ""
    for r in rows[:10]:
        result += f"{r[0]} - {r[1]}\n\n"

    return result


# =========================
# WORD COUNT
# =========================
def word_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    words = []
    for r in rows:
        words.extend(r[0].split())

    return f"Total words: {len(words)}"

# =========================
# TRANSLATE TO KOREAN
# =========================
def translate_korean():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text, author FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    result = ""

    for r in rows[:10]:
        text = r[0]
        author = r[1]

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "ko",  # 👈 ini Korean
            "dt": "t",
            "q": text
        }

        response = requests.get(url, params=params)
        translated = response.json()[0][0][0]

        result += f"{translated} - {author}\n\n"

    return result

    
# =========================
# TRANSLATE TO INDONESIAN
# =========================
def translate_quotes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text, author FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    result = ""

    for r in rows[:10]:
        text = r[0]
        author = r[1]

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "id",
            "dt": "t",
            "q": text
        }

        response = requests.get(url, params=params)
        translated = response.json()[0][0][0]

        result += f"{translated} - {author}\n\n"

    return result
    

# =========================
# UI
# =========================
with gr.Blocks() as app:
    gr.Markdown("# Quotes Data Analysis System")
    gr.Markdown("An integrated system for quote data analysis, visualization, and translation.")
    
    with gr.Tab("View Quotes"):
        output = gr.Textbox(lines=15)

        btn = gr.Button("Load Quotes")
        btn.click(get_quotes, outputs=output)

        btn_translate_kr = gr.Button("Translate to Korean 🇰🇷")
        btn_translate_kr.click(translate_korean, outputs=output)

        btn_translate = gr.Button("Translate to Indonesian 🇮🇩")
        btn_translate.click(translate_quotes, outputs=output)

    with gr.Tab("Analysis"):
        output2 = gr.Textbox()

        btn2 = gr.Button("Word Count")
        btn2.click(word_count, outputs=output2)

app.launch()
