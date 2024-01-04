from autoframe.express.chainlit import ChainlitAssistantAgent
from autoframe.express.config import create_user_proxy, llm_config

lian = ChainlitAssistantAgent(
    name="coding_assistant",
    llm_config=llm_config,
    max_consecutive_auto_reply=10,
)


ask_assistant_doc = {
    "name": "ask_assistant",
    "description": """
Pythonを用いて要件を実装し、実行結果を出力するアシスタントです。
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


def ask_assistant(message):
    user_proxy = create_user_proxy("coding_assistant_user_proxy")
    user_proxy.initiate_chat(lian, message=message)
    last_message = user_proxy.last_message()
    return last_message["content"] if last_message is not None else ""
