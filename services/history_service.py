import os
import gradio as gr
import tempfile
import json
import datetime


def save_history(history, history_file):
    if history is None or history == []:
        status_display = "No history to save."
        return history_file, gr.Button().update(), gr.Button().update(), status_display
    current_time = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    saved_file_name = "history-" + current_time + ".json"
    saved_path = tempfile.gettempdir().replace(
        "T", saved_file_name)
    with open(saved_path, "w", encoding="utf-8") as f:
        json.dump(history, f)

    history_file = gr.File.update(value=saved_path)
    status_display = "History saved."
    save_history_btn = gr.Button().update(visible=False)
    load_history_btn = gr.Button().update(visible=True)

    return history_file, save_history_btn, load_history_btn, status_display


def load_history(history_file, chatbot, history):
    if history_file is None:
        status_display = "No history file to load."
        return chatbot, history, status_display

    path = history_file.name
    with open(path, "r", encoding="utf-8") as f:
        load_history = json.load(f)

    if type(load_history) != list:
        status_display = "Please select input list json file for history."
        return chatbot, history, status_display
    if len(load_history) <= 1:
        status_display = "Wrong history file."
        return chatbot, history, status_display

    chatbot = []
    for message in load_history:
        if message["role"] == "user":
            user_message = message["content"]
            if "Current date: " in user_message and "Query: " in user_message:
                user_message = user_message.split("Query: ")[1]
            elif "Answer the question: " in user_message:
                user_message = user_message.split("Answer the question: ")[1]

            chatbot.append([user_message, ""])
        elif message["role"] == "assistant":
            chatbot[-1][1] = message["content"]

    history = load_history[:]
    status_display = "History loaded."
    return chatbot, history, status_display


def load_history_file(history_file):
    if history_file is None:
        status_display = "Clear history."
        save_history_btn = gr.Button().update(visible=True)
        load_history_btn = gr.Button().update(visible=False)
        return save_history_btn, load_history_btn, status_display

    path = history_file.name

    if os.path.splitext(path)[1] != ".json":
        status_display = "Please select input json file for history."
        return "", status_display, ""

    save_history_btn = gr.Button().update(visible=False)
    load_history_btn = gr.Button().update(visible=True)

    return save_history_btn, load_history_btn, "History files loaded."
