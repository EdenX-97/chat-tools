import re
import gradio as gr


def show_hide_professional_components(if_professional_mode):
    professional_mode_column = gr.Column().update(visible=if_professional_mode)
    return professional_mode_column


def update_api_key(api_key_input):
    user_api_key = api_key_input
    api_key_regex = r'^sk-[0-9a-zA-Z]{48}$'
    if not re.match(api_key_regex, user_api_key):
        status_display = "Please enter a correct OpenAI API key."
        user_api_key = ""
    else:
        status_display = "API key updated"
    return user_api_key, status_display
