"""
# Agile AIエージェント

## 概要

- SM, PO, DevのAIエージェントを作成する。
- SMには、スプリントの進捗管理、POには、バックログの管理、Devには、タスクの管理を担わせる。
- ユースケースとして、簡単なタスク管理アプリを作成する。

## 背景

- 役割が明確でシンプルなスクラムを参考に練習したい。

## やること

- SM, PO, DevのAIエージェントを作成する。
- スプリントDBを作成する。
- バックログDBを作成する。
- タスクDBを作成する。
"""

import logging
import os
from time import time

import autogen

logging.basicConfig(level=logging.WARN)

openai_apikey = os.getenv("OPENAI_API_KEY")
config_list = [
    {
        "model": "gpt-3.5-turbo-1106",
        "api_key": openai_apikey,
    }
]
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "timeout": 120,
}


def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


class CommonConversableAgent(autogen.ConversableAgent):
    """A CommonConversableAgent class."""

    def __init__(self, name: str, additional_system_message: str, functions=[]) -> None:
        """Create a CommonConversableAgent instance."""
        super().__init__(
            name=name,
            llm_config={**llm_config, "functions": functions} if len(functions) > 0 else llm_config,
            system_message=f"""
Your role is {name}.
{additional_system_message}
""",
            human_input_mode="NEVER",
            default_auto_reply=None,
            is_termination_msg=termination_msg,
            max_consecutive_auto_reply=10,
            code_execution_config=False,
        )


timer = 0


def start_timer(s: int) -> str:
    """Start a timer."""
    global timer
    timer = time() + (s / 10)
    return f"タイマーを{s}秒に設定しました。"


start_timer_doc = {
    "name": "start_timer",
    "description": "タイマーを開始する",
    "parameters": {
        "type": "object",
        "properties": {"s": {"type": "integer", "description": "タイマーの秒数"}},
        "required": ["s"],
    },
}


def get_time_left() -> str:
    """Get the time left."""
    global timer
    left = timer - time()
    if left < 0:
        return "タイマーは終了しています。"
    return f"残り時間は{left*10}秒です。"


get_time_left_doc = {
    "name": "get_time_left",
    "description": """タイマーの残り時間を取得する。""",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

agent_sm = CommonConversableAgent(
    name="ScrumMaster",
    additional_system_message="""
スクラムフレームワークにのっとって、開発を行います。
不要な会話を排除するために、タイムキーパーの役割を果たしなさい。
トピックの初めにstart_timerを呼び出すことで、タイマーを開始できる。
プログラムが提供された場合、絶対にタイマーをスタートさせてはならない。
get_time_leftを呼び出すことで、残り時間を確認できる。
タイマーが終了したら、次のTopicに移りなさい。
必ずAdminのタスクを遂行すること。
""",
    functions=[start_timer_doc, get_time_left_doc],
)

agent_po = CommonConversableAgent(
    name="ProductOwner",
    additional_system_message="""
Developerにタスクを指示しなさい。
タスクはその場で消化させること。
命令口調で話すこと。
""",
)

agent_dev = CommonConversableAgent(
    name="Developer",
    additional_system_message="""Pythonでプログラムを作成しなさい。""",
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    is_termination_msg=termination_msg,
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "_paper",
        "use_docker": False,
    },
)

reviewer = CommonConversableAgent(
    name="Code_Reviewer",
    additional_system_message="You are a code reviewer. Reply `TERMINATE` in the end when everything is done.",
)

for agent in [agent_sm, agent_po, agent_dev, executor]:
    # register functions for all agents.
    agent.register_function(
        function_map={
            "start_timer": start_timer,
            "get_time_left": get_time_left,
        }
    )

# Create a GroupChat instance
groupchat = autogen.GroupChat(
    agents=[agent_sm, agent_po, agent_dev, reviewer, executor],
    messages=[],
    max_round=50,
)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)
user_proxy.initiate_chat(
    manager,
    message="""ghとfzfを用いたcli extensionを作成しなさい。
コマンドライン引数なしの場合、仮引数でサンプルを実行できるようにしなさい。""",
)
