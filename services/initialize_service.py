import os
import re
import json

import gradio as gr


# Set OpenAI API key
openai_api_key = ""
if os.path.exists("openai_api_key.txt") and os.path.getsize("openai_api_key.txt"):
    with open("openai_api_key.txt", "r") as f:
        openai_api_key = f.read().strip()
elif 'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY'] != '':
    openai_api_key = os.environ['OPENAI_API_KEY']

if openai_api_key != "":
    api_key_regex = r'^sk-[0-9a-zA-Z]{48}$'
    if not re.match(api_key_regex, openai_api_key):
        raise Exception("Please enter a correct OpenAI API key.")

# Set configs
with open("configs.json", "r", encoding="utf-8") as f:
    default_configs = json.load(f)

# Set default tools
default_role_options = default_configs['ai_roles']['Useful']

# Set tokens calculate settings
tokens_calculate = default_configs['tokens_calculate']

# Set description
description = "<div align='center' style='margin:16px 0'>\n\n" + \
    default_configs['description'] + "\n</div>"

# Set CSS style
with open("assets/style.css", "r", encoding="utf-8") as f:
    style = f.read()

# Set Theme
theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#02C160",
        c100="rgba(2, 193, 96, 0.2)",
        c200="#02C160",
        c300="rgba(2, 193, 96, 0.32)",
        c400="rgba(2, 193, 96, 0.32)",
        c500="rgba(2, 193, 96, 1.0)",
        c600="rgba(2, 193, 96, 1.0)",
        c700="rgba(2, 193, 96, 0.32)",
        c800="rgba(2, 193, 96, 0.32)",
        c900="#02C160",
        c950="#02C160",
    ),
    secondary_hue=gr.themes.Color(
        c50="#576b95",
        c100="#576b95",
        c200="#576b95",
        c300="#576b95",
        c400="#576b95",
        c500="#576b95",
        c600="#576b95",
        c700="#576b95",
        c800="#576b95",
        c900="#576b95",
        c950="#576b95",
    ),
    neutral_hue=gr.themes.Color(
        name="gray",
        c50="#f9fafb",
        c100="#f3f4f6",
        c200="#e5e7eb",
        c300="#d1d5db",
        c400="#B2B2B2",
        c500="#808080",
        c600="#636363",
        c700="#515151",
        c800="#393939",
        c900="#272727",
        c950="#171717",
    ),
    radius_size=gr.themes.sizes.radius_sm,
).set(
    button_primary_background_fill="#06AE56",
    button_primary_background_fill_dark="#06AE56",
    button_primary_background_fill_hover="#07C863",
    button_primary_border_color="#06AE56",
    button_primary_border_color_dark="#06AE56",
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
    button_secondary_background_fill="#F2F2F2",
    button_secondary_background_fill_dark="#2B2B2B",
    button_secondary_text_color="#393939",
    button_secondary_text_color_dark="#FFFFFF",
    # background_fill_primary="#F7F7F7",
    # background_fill_primary_dark="#1F1F1F",
    block_title_text_color="*primary_500",
    block_title_background_fill="*primary_100",
    input_background_fill="#F6F6F6",
)
