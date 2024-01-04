import logging
from typing import Dict, Optional, Union

import chainlit as cl
from autogen import Agent, AssistantAgent, UserProxyAgent

logging.basicConfig(level=logging.INFO)


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
        logging.info(f"message: {message}")
        if isinstance(message, str):
            cl.run_sync(
                cl.Message(
                    content=f"@{recipient.name}\n{message}",
                    author=self.name,
                ).send()
            )
        elif "content" in message and message["content"] is not None:
            cl.run_sync(
                cl.Message(
                    content=f'@{recipient.name}\n{message["content"]}',
                    author=self.name,
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
        last_message = messages[-1].get("content", "")
        logging.info(f"last_message: {last_message}")
        if last_message is None or "```" in last_message or "function_call" in last_message:
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
        return reply["content"].strip()

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        if isinstance(message, str):
            cl.run_sync(
                cl.Message(
                    content=f"@{recipient.name}\n{message}",
                    author=self.name,
                ).send()
            )
        elif "content" in message and message["content"] is not None:
            cl.run_sync(
                cl.Message(
                    content=f'@{recipient.name}\n{message["content"]}',
                    author=self.name,
                ).send()
            )
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )
