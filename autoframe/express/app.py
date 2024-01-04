"""
chainlit run autoframe/senarios/express/main.py -w
"""


import logging

import chainlit as cl

from autoframe.express.agents import assistant, user_proxy

logging.basicConfig(level=logging.INFO)


@cl.on_message
async def main(message: cl.Message):
    await cl.make_async(user_proxy.initiate_chat)(
        assistant,
        message=message.content,
    )
