"""
chainlit run autoframe/senarios/express/main.py -w
"""


import logging
import os
from typing import Dict, Optional, Union

import chainlit as cl
from autogen import Agent, AssistantAgent, UserProxyAgent

logging.basicConfig(level=logging.INFO)


def is_termination_msg(x):
    return x.get("content", "") and (
        x.get("content", "").rstrip().endswith("TERMINATE") or x.get("content", "").rstrip().endswith("TERMINATE.")
    )


async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res


class ChainlitAssistantAgent(AssistantAgent):
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        cl.run_sync(
            cl.Message(
                content=f'*Sending message to "{recipient.name}":*\n\n{message}',
                author="AssistantAgent",
            ).send()
        )
        super(ChainlitAssistantAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


class ChainlitUserProxyAgent(UserProxyAgent):
    def get_human_input(self, prompt: str) -> str:
        # プログラムの場合、ユーザーの入力を待たずに実行する
        messages = [m for ms in self.chat_messages.values() for m in ms]
        if "```" in messages[-1].get("content", ""):
            return ""
        if prompt.startswith("Provide feedback to assistant. Press enter to skip and use auto-reply"):
            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="Continue or provide feedback?",
                    actions=[
                        cl.Action(name="continue", value="continue", label="✅ Continue"),
                        cl.Action(
                            name="feedback",
                            value="feedback",
                            label="💬 Provide feedback",
                        ),
                        cl.Action(name="exit", value="exit", label="🔚 Exit Conversation"),
                    ],
                )
            )
            if res.get("value") == "continue":
                return ""
            if res.get("value") == "exit":
                return "exit"

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))
        logging.info(f"User reply: {reply}")
        return reply["content"].strip()

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


openai_apikey = os.getenv("OPENAI_API_KEY")
config_list = [
    {
        "model": "gpt-3.5-turbo-1106",
        "api_key": openai_apikey,
    }
]
assistant = ChainlitAssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = ChainlitUserProxyAgent(
    "user_proxy",
    code_execution_config={
        "work_dir": "../_workspace",  # prevent reloading
        "use_docker": False,
    },
    is_termination_msg=is_termination_msg,
)


@cl.on_message
async def main(message: cl.Message):
    await cl.make_async(user_proxy.initiate_chat)(
        assistant,
        message=message.content,
    )
