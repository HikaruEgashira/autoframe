"""Calculate the year-to-date gain for META and TESLA."""
import logging

import autogen

logging.basicConfig(level=logging.WARN)

config_list = autogen.config_list_from_dotenv(model_api_key_map={"gpt-4-1106-preview": "OPENAI_API_KEY"})
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 1,
}

# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    default_auto_reply=None,
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "_coding",
        "use_docker": False,
    },
)

# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA. Use pip library.""",
)
