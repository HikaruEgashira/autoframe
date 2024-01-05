import os

from autoframe.express.agent import ChainlitUserProxyAgent

openai_apikey = os.getenv("OPENAI_API_KEY")
config_list = [
    {
        "model": "gpt-3.5-turbo-1106",
        "api_key": openai_apikey,
    },
    # {
    #     "model": "gpt-4-1106-preview",
    #     "api_key": openai_apikey,
    # },
]
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 1,
}


def is_termination_msg(x):
    return x.get("content", "") and ("TERMINATE" in x.get("content", ""))


def create_user_proxy(name="user_proxy"):
    user_proxy = ChainlitUserProxyAgent(
        name=name,
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": f"../_workspace/{name}",  # prevent reloading
            "use_docker": False,
        },
        is_termination_msg=is_termination_msg,
    )
    return user_proxy
