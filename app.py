import gradio as gr
import sqlite3

def get_quotes():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT text, author FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    result = ""
    for r in rows[:10]:
        result += f"{r[0]} - {r[1]}\n\n"

    return result


def word_count():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    words = []
    for r in rows:
        words.extend(r[0].split())

    return f"Total words: {len(words)}"


with gr.Blocks() as app:
    gr.Markdown("# 📊 Quotes App")

    with gr.Tab("View Quotes"):
        output = gr.Textbox(lines=15)
        btn = gr.Button("Load Quotes")
        btn.click(get_quotes, outputs=output)

    with gr.Tab("Analysis"):
        output2 = gr.Textbox()
        btn2 = gr.Button("Word Count")
        btn2.click(word_count, outputs=output2)

app.launch()
