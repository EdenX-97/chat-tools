import gradio as gr
import openai
import json
import datetime
import logging
import services.shared_service as shared
from services.embedded_service import *
from services.token_service import *
from duckduckgo_search import ddg


WEBSEARCH_PTOMPT_TEMPLATE = """\
Web search results:

{web_results}
Current date: {current_date}

Instructions: Answer the query based on your own thoughts and knowledge, and feel free to supplement with relevant web search results. Make sure to cite results using [[number](URL)] notation after the reference. If there are multiple subjects with the same name in the search results, provide separate answers for each. Use prior knowledge only if the given context didn't provide enough information. And use clear language to write your answer.
Query: {query}
"""

PROMPT_TEMPLATE = """\
Context information is below.
---------------------
{context_str}
---------------------
Current date: {current_date}.
Using the provided context information, write a comprehensive reply to the given query.
Make sure to cite results using [[number](URL)] notation after the reference.
If the provided context information refer to multiple subjects with the same name, write separate answers for each subject.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
"""


def start_responsing(inputs):
    logging.info("Start responsing")
    reset_textbox = gr.update(value="")
    set_send_btn_invisible = gr.Button.update(visible=False)
    set_cancel_btn_visible = gr.Button.update(visible=True)
    return inputs, reset_textbox, set_send_btn_invisible, set_cancel_btn_visible


def end_oresponsing():
    logging.info("Stop responsing")
    set_send_btn_visible = gr.Button.update(visible=True)
    set_cancel_btn_invisible = gr.Button.update(visible=False)
    status_display = "Responsing finished"
    return set_send_btn_visible, set_cancel_btn_invisible, status_display


def cancel_responsing():
    logging.info("Cancel responsing")
    shared.state.interrupt()


def online_search(user_question):
    logging.info("Online search")
    search_results = ddg(user_question, max_results=3)
    fomatted_search_results = []
    for idx, result in enumerate(search_results):
        fomatted_search_results.append(
            f'[{idx+1}]"{result["body"]}"\nURL: {result["href"]}')
        logging.info(len(fomatted_search_results[idx]))
    user_question = WEBSEARCH_PTOMPT_TEMPLATE.format(
        web_results="\n".join(fomatted_search_results),
        current_date=datetime.datetime.today().strftime("%Y-%m-%d"),
        query=user_question,
    )

    return user_question


def chat(
    user_api_key,
    selected_ai_role,
    history,
    user_question,
    temperatrue,
    chatbot,
    selected_model="gpt-3.5-turbo",
    if_online_search=False,
    index_file=None
):
    if user_question == "":
        status_display = 'Cannot input empty messages'
        logging.info("Cannot input empty messages")
        yield chatbot, history, status_display
        return

    if if_online_search and index_file is not None:
        status_display = 'Cannot enable online search and documents search at the same time'
        yield chatbot, history, status_display
        return

    # There is a index file, load the index, and search the documents to answer
    if index_file is not None:
        status_display = "Searching documents and answering..."
        question = user_question[:]
        response = query(user_api_key, index_file, question)
        chatbot.append([user_question, response])
        history.append({'role': 'user', 'content': question})
        history.append({'role': 'assistant', 'content': response})
        logging.info("Search documents and answer finished")
        yield chatbot, history, status_display
        return

    if not if_online_search:
        question = user_question[:]
    else:
        question = online_search(user_question)

    openai.api_key = user_api_key

    # Set prompts
    logging.info("Set prompts")
    with open("prompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)

    if len(history) == 0:
        history = prompts[selected_ai_role][:]
    else:
        history.append(prompts[selected_ai_role][0])

    if chatbot == None:
        chatbot = []

    # Check if token num over the limit
    predict_tokens = calculate_tokens_messages(history, selected_model)
    print(predict_tokens)
    if predict_tokens > 3800:
        # Need to optimize the token num
        logging.info("Optimize the token num")
        status_display = 'Optimizing the token num...'
        yield chatbot, history, status_display

        # Get the summary of previous mesaages
        logging.info("Get the summary of previous mesaages")
        history.append(
            {'role': 'user', 'content': 'Please summarize our previous conversation.'})
        response = openai.ChatCompletion.create(
            model=selected_model, messages=history, temperature=temperatrue, stream=False)
        summary = response['choices'][0]['message']['content']
        history = [
            history[0],  # System prompt
            {'role': 'assistant', 'content': summary},
        ]
        chatbot = [
            ['Auto summarized', summary]
        ]

    chatbot.append([user_question, ''])
    history.append({'role': 'user', 'content': question})

    new_messages = history[:]

    logging.info("Getting chat result from openai api")
    try:
        response = openai.ChatCompletion.create(
            model=selected_model, messages=new_messages, temperature=temperatrue, stream=True)
    except:
        status_display = 'AI respond failed, maybe the API key is invalid'
        logging.info("AI respond failed, maybe the API key is invalid")
        history.pop()
        chatbot[-1] = [chatbot[-1][0], status_display]
        yield chatbot, history, status_display
        return

    status_display = 'AI is responding...'
    logging.info("AI is responding...")

    # Iterate to get the response
    full_response_content = ""
    for chunk in response:
        message = chunk['choices'][0]['delta']
        if hasattr(message, 'content'):
            if shared.state.interrupted:
                shared.state.recover()
                yield chatbot, history, status_display
                return
            full_response_content += message['content']
            chatbot[-1] = [chatbot[-1][0], full_response_content]
            yield chatbot, history, status_display
    history.append({'role': 'assistant', 'content': full_response_content})
    yield chatbot, history, status_display
