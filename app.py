# -*- coding:utf-8 -*-
import sys
import os
import re
import logging

from services.initialize_service import *
from services.chat_service import *
from services.token_service import *
from services.mode_service import *
from services.overwrite_service import *
from services.professional_mode_service import *
from services.embedded_service import *
from services.history_service import *
from services.role_service import *

import gradio as gr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
)

gr.Chatbot.postprocess = postprocess

with gr.Blocks(css=style, theme=theme) as app:
    # Set app states
    history = gr.State([])
    user_api_key = gr.State(openai_api_key)
    user_question = gr.State("")
    configs = gr.State(default_configs)

    # Content
    with gr.Row():
        # Sidebar
        with gr.Column(scale=2, elem_id="sidebar"):
            with gr.Column(min_width=50):
                with gr.Tab("Enhanced Features"):
                    if_online_search = gr.Checkbox(
                        label="Enable online search", value=False)
                    if_documents_search = gr.Checkbox(
                        label="Enable documents search", value=False)
                    if_professional_mode = gr.Checkbox(
                        label="Enable professional mode", value=False)

                with gr.Tab("Tools Switch"):
                    with gr.Row():
                        normarl_btn = gr.Button(
                            "Useful Tools", variant="secondary")
                        academic_btn = gr.Button(
                            "Academic Tools", variant="secondary")
                        develop_btn = gr.Button(
                            "Develop Tools", variant="secondary")
                        fun_btn = gr.Button(
                            "Fun Tools", variant="secondary")

                with gr.Row():
                    selected_ai_role = gr.Dropdown(
                        label="AI Role", choices=default_role_options, multiselect=False, value=default_role_options[0], elem_id="selected_ai_role")

                with gr.Box(elem_id="box"):
                    with gr.Column():
                        history_file = gr.File(
                            label="Upload or download history here", type="file", file_types=[".json"])
                        save_history_btn = gr.Button(
                            "Save History", variant="secondary")
                        load_history_btn = gr.Button(
                            "Load History", variant="secondary", visible=False)

                documents_search_row = gr.Row(
                    visible=if_documents_search.value)
                with documents_search_row:
                    with gr.Tab('Documents'):
                        documents = gr.Files(
                            label="Upload documents", type="file", file_types=[".json", ".txt", ".pdf", ".docx"])
                    with gr.Tab('Index'):
                        index_file = gr.File(
                            label="Upload index", type="file", file_types=[".json"])

                professional_mode_column = gr.Column(
                    visible=if_professional_mode.value)
                with professional_mode_column:
                    with gr.Box(elem_id="box"):
                        api_key_input = gr.Textbox(
                            label="OpenAI API Key",
                            value=openai_api_key,
                            placeholder="Input your OpenAI API Key",
                            type="password",
                            interactive=True,
                        )

                        models = configs.value['models']
                        selected_model = gr.Dropdown(
                            label="Model", choices=models, multiselect=False, value=models[0])

                        total_granted, total_used = get_token_usage_value(
                            openai_api_key)
                        token_usage = gr.Slider(
                            minimum=0.00, maximum=total_granted, value=total_used, interactive=False, label="Token Usage")

                        temperatrue = gr.Slider(
                            minimum=0.0, maximum=2.0, value=0.4, step=0.1, label="Temperature")

            # Chatbox
        with gr.Column(scale=4):
            with gr.Column():
                with gr.Row():
                    status_display = gr.Markdown(
                        "Welcome to chat tools", elem_id="status_display")
                with gr.Row():
                    chatbot = gr.Chatbot(
                        label="Messages", elem_id="chatbot").style(height="100%")
                with gr.Row():
                    with gr.Column(scale=12):
                        user_input = gr.Textbox(
                            show_label=False, placeholder="Enter your question here..."
                        ).style(container=False)
                    with gr.Column(min_width=70, scale=1):
                        submit_btn = gr.Button("Send", variant="primary")
                        cancel_btn = gr.Button(
                            "Cancel", variant="secondary", visible=False)

    gr.Markdown(description)

    start_responsing_args = dict(
        fn=start_responsing,
        inputs=[user_input],
        outputs=[user_question, user_input, submit_btn, cancel_btn],
        show_progress=True
    )

    chat_args = dict(
        fn=chat,
        inputs=[
            user_api_key,
            selected_ai_role,
            history,
            user_question,
            temperatrue,
            chatbot,
            selected_model,
            if_online_search,
            index_file
        ],
        outputs=[chatbot, history, status_display],
        show_progress=True,
    )

    end_responsing_args = dict(
        fn=end_oresponsing, inputs=[], outputs=[submit_btn, cancel_btn, status_display]
    )

    token_usage_args = dict(
        fn=get_token_usage, inputs=[user_api_key], outputs=[
            token_usage], show_progress=False
    )

    normal_mode_args = dict(
        fn=normal_mode, inputs=configs, outputs=selected_ai_role
    )

    academic_mode_args = dict(
        fn=academic_mode, inputs=configs, outputs=selected_ai_role
    )

    develop_mode_args = dict(
        fn=develop_mode, inputs=configs, outputs=selected_ai_role
    )

    fun_mode_args = dict(
        fn=fun_mode, inputs=configs, outputs=selected_ai_role
    )

    selected_ai_role.change(update_ai_role, inputs=[], outputs=[
                            chatbot, history, status_display])

    user_input.submit(**start_responsing_args).then(**
                                                    chat_args).then(**end_responsing_args)
    user_input.submit(**token_usage_args)

    submit_btn.click(**start_responsing_args).then(**
                                                   chat_args).then(**end_responsing_args)
    submit_btn.click(**token_usage_args)

    cancel_btn.click(cancel_responsing, [], [])

    api_key_input.change(
        update_api_key, inputs=api_key_input, outputs=[user_api_key, status_display])

    normarl_btn.click(**normal_mode_args)
    academic_btn.click(**academic_mode_args)
    develop_btn.click(**develop_mode_args)
    fun_btn.click(**fun_mode_args)

    if_professional_mode.change(show_hide_professional_components,
                                inputs=if_professional_mode, outputs=professional_mode_column)

    if_documents_search.change(click_documents_search_checkbox,
                               inputs=if_documents_search, outputs=documents_search_row)

    documents.upload(create_index, inputs=[
                     user_api_key, documents], outputs=index_file)

    history_file.change(load_history_file, inputs=history_file,
                        outputs=[save_history_btn, load_history_btn, status_display])

    save_history_btn.click(save_history, inputs=[history, history_file], outputs=[
        history_file, save_history_btn, load_history_btn, status_display])

    load_history_btn.click(load_history, inputs=[history_file, chatbot, history], outputs=[
                           chatbot, history, status_display])

app.title = configs.value['title']

if __name__ == "__main__":
    app.queue(
        concurrency_count=configs.value['user_limit']
    ).launch(
        share=False,
        favicon_path="assets/favicon.ico",
        inbrowser=True,
    )
