"""
chainlit run autoframe/express/main.py -w
"""
import logging

import chainlit as cl

from autoframe.express.agent import ChainlitAssistantAgent, ChainlitUserProxyAgent
from autoframe.express.config import is_termination_msg, llm_config
from autoframe.express.tools.ask_programmer import ask_programmer, ask_programmer_doc
from autoframe.express.tools.search import search, search_doc

logging.basicConfig(level=logging.INFO)

assistant = ChainlitAssistantAgent(
    "assistant",
    system_message="",
    llm_config={
        **llm_config,
        "functions": [
            ask_programmer_doc,
            search_doc,
        ],
    },
)
user_proxy = ChainlitUserProxyAgent(
    "user_proxy",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
    function_map={"ask_programmer": ask_programmer, "search": search},
)


@cl.on_message
async def main(message: cl.Message):
    await cl.make_async(user_proxy.initiate_chat)(
        assistant,
        message=message.content,
    )
