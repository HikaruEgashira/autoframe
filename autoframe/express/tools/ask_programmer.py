from autoframe.express.agent import ChainlitAssistantAgent
from autoframe.express.config import create_user_proxy, llm_config

programmer_agent = ChainlitAssistantAgent(
    name="programmer",
    llm_config=llm_config,
    max_consecutive_auto_reply=10,
)


ask_programmer_doc = {
    "name": "ask_programmer",
    "description": """
Pythonを用いて要件を実装し、実行結果を応答するアシスタントです。
""",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": """
達成したいタスクをDesign Docのフォーマットで記述します。""",
            },
        },
        "required": ["message"],
    },
}


def ask_programmer(message):
    user_proxy = create_user_proxy("ask_programmer_user_proxy")
    user_proxy.initiate_chat(programmer_agent, message=message)
    last_message = user_proxy.last_message()
    return last_message["content"] if last_message is not None else ""
