import requests
import logging
import gradio as gr
import tiktoken
from services.initialize_service import tokens_calculate


def get_token_usage_value(user_api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_api_key}",
    }

    timeout = 100

    try:
        response = requests.get(
            "https://api.openai.com/dashboard/billing/credit_grants",
            headers=headers,
            timeout=timeout,
        )
        # logging.info(response.json())

        total_granted = response.json()['total_granted']
        total_used = response.json()['total_used']

        return total_granted, total_used
    except:
        logging.info("Failed to get token usage")
        return 18.00, 0.00


def get_token_usage(user_api_key):
    total_granted, total_used = get_token_usage_value(user_api_key)
    return gr.Slider.update(maximum=total_granted, value=total_used)


def calculate_tokens_messages(messages, model):
    encoding = tiktoken.encoding_for_model(model)
    tokens_num = 0
    for message in messages:
        tokens_num += tokens_calculate[model]['tokens_per_message']
        for key, value in message.items():
            tokens_num += len(encoding.encode(value))
            if key == "name":
                tokens_num += tokens_calculate[model]['tokens_per_name']
    tokens_num += 2
    return tokens_num
