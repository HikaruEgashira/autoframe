import logging

import autogen

logging.basicConfig(level=logging.WARN)

config_list = autogen.config_list_from_dotenv(model_api_key_map={"gpt-4-1106-preview": "OPENAI_API_KEY"})
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 1,
}

# Construct Agents
constructor = autogen.AssistantAgent(
    name="constructor",
    llm_config={"config_list": config_list},
    system_message="""
    Generate math expression. Operation only supports addition.
    DO NOT USE OTHER OPERATOR.
    bad: 3 * 4
    good: 3 + 3 + 3 + 3
    DO NOT EVALUATE THE EXPRESSION. JUST GENERATE THE EXPRESSION.
    """,
)
constructor_user = autogen.UserProxyAgent(
    name="constructor_user",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    human_input_mode="NEVER",
)


def ask_constructor(message):
    constructor_user.initiate_chat(constructor, message=message)
    last_message = constructor_user.last_message()
    return last_message["content"] if last_message is not None else ""


def calc_sum(numbers):
    return sum(numbers)


# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="""
if user ask math problems.
1. ask constructor to generate math expression.
2. ask user to calculate the sum of numbers in the expression.
3. return the result.
""",
    is_termination_msg=lambda x: x.get("content", "") == "",  # user_proxy response empty string
    llm_config={
        "temperature": 0,
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
        "functions": [
            {
                "name": "ask_constructor",
                "description": """数式を生成する""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": """コンストラクターに尋ねる質問。
                                コードと実行結果など、十分な文脈を含めるようにしてください。
                                ユーザーとの会話をコンストラクターと共有しない限り、コンストラクターは会話を知りません。""",
                        },
                    },
                    "required": ["message"],
                },
            },
            {
                "name": "calc_sum",
                "description": """Calculate the sum of list[int]""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": """数値のリスト""",
                        },
                    },
                    "required": ["numbers"],
                },
            },
        ],
    },
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "content" in x
    and x["content"] is not None
    and x["content"].rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "_planning"},
    function_map={"calc_sum": calc_sum, "ask_constructor": ask_constructor},
)

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""
        6人のユーザーが3つのりんごを購入しました。
        3人のユーザーが2つのりんごを購入しました。
        2人のユーザーが1つのりんごを購入しました。
        1人のユーザーが0個のりんごを購入しました。
        10人のユーザーは何個のりんごを購入しましたか？
        """,
)
