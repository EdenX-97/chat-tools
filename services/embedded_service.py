import os
import logging
import datetime
import gradio as gr
from llama_index import (
    GPTVectorStoreIndex,
    LLMPredictor,
    SimpleDirectoryReader,
    PromptHelper,
    QuestionAnswerPrompt,
    ServiceContext
)
from langchain.llms import OpenAIChat


PROMPT_TEMPLATE = """\
Context information is below.
---------------------
{context_str}
---------------------
Current date: {current_date}.
Using the provided context information, write a comprehensive reply to the given query.
Make sure to cite results using [number] notation after the reference.
If the provided context information refer to multiple subjects with the same name, write separate answers for each subject.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
"""


def click_documents_search_checkbox(if_documents_search):
    documents_box = gr.Box().update(visible=if_documents_search)
    return documents_box


def create_index(user_api_key,
                 documents,
                 max_input_size=4096,
                 num_outputs=1,
                 max_chunk_overlap=20,
                 chunk_size_limit=600,
                 embedding_limit=None,
                 separator=" "):
    os.environ["OPENAI_API_KEY"] = user_api_key

    prompt_helper = PromptHelper(
        max_input_size,
        num_outputs,
        max_chunk_overlap,
        embedding_limit,
        chunk_size_limit,
        separator=separator,
    )

    service_context = ServiceContext.from_defaults(prompt_helper=prompt_helper)

    try:
        documents_url = []
        path_prefix = ""
        for document in documents:
            if path_prefix == "":
                path_prefix = os.path.split(document.name)[0]
            documents_url.append(document.name)

        documents_loaded = SimpleDirectoryReader(
            input_files=documents_url).load_data()

        index = GPTVectorStoreIndex.from_documents(
            documents=documents_loaded, service_context=service_context)

        os.environ["OPENAI_API_KEY"] = ""

        index_file_name = path_prefix + "/index.json"
        index.save_to_disk(index_file_name)

        return gr.File().update(index_file_name)
    except Exception as e:
        logging.error(e)
        logging.info("Create index failed")
        os.environ["OPENAI_API_KEY"] = ""
        return None


def query(user_api_key,
          index_file,
          query,
          prefix_messages=[],
          temprature=0.4):
    os.environ["OPENAI_API_KEY"] = user_api_key

    llm_predictor = LLMPredictor(
        llm=OpenAIChat(
            temperature=temprature,
            model_name="gpt-3.5-turbo",
            prefix_messages=prefix_messages
        )
    )

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    question_answer_prompt = QuestionAnswerPrompt(PROMPT_TEMPLATE.replace(
        "{current_date}", datetime.datetime.today().strftime("%Y-%m-%d")))

    index = GPTVectorStoreIndex.load_from_disk(
        index_file.name, service_context=service_context)

    response = index.query(query, similarity_top_k=1,
                           text_qa_template=question_answer_prompt, response_mode="compact")

    os.environ["OPENAI_API_KEY"] = ""

    logging.info("Finished query")
    return response.response
