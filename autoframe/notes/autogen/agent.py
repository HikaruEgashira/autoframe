"""Calculate the year-to-date gain for META and TESLA."""
import logging
import os

import autogen

logging.basicConfig(level=logging.INFO)

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
    "temperature": 1,
}

# create an ConversableAgent named "agent"
agent = autogen.ConversableAgent(
    name="agent",
    llm_config=llm_config,
    system_message="""
You are a helpful assistant that can use available functions when needed to solve problems.
At each point, do your best to determine if the user's request has been addressed.
IF THE REQUEST HAS NOT BEEN ADDRESSED, RESPOND WITH CODE TO ADDRESS IT.
IF A FAILURE OCCURRED (e.g., due to a missing library)
AND SOME ADDITIONAL CODE WAS WRITTEN (e.g. code to install the library).
ENSURE THAT THE ORIGINAL CODE TO ADDRESS THE TASK STILL GETS EXECUTED.
If the request HAS been addressed, respond with a summary of the result.
The summary must be written as a coherent helpful response to the user request.
e.g. 'Sure, here is result to your request ' or 'The tallest mountain in Africa is ..' etc.
Always respond in Japanese.
""",
    is_termination_msg=lambda x: x.get("content", "") == "",  # user_proxy response empty string
    max_consecutive_auto_reply=10,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),  # agent response "TERMINATE"
    code_execution_config={
        "work_dir": "_coding",
        "use_docker": False,
    },
)

# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    agent,
    message="""
Calculate the year-to-date gain for META and TESLA.
""",
)
