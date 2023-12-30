"""Calculate the year-to-date gain for META and TESLA."""
import logging

import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

logging.basicConfig(level=logging.WARN)

config_list = autogen.config_list_from_dotenv()
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 1,
}

gpt_assistant = GPTAssistantAgent(
    name="Socrates",
    llm_config={
        **llm_config,
        "assistant_id": None,
    },
    instructions="""
Respond to inquiries by returning questions using the Socratic method, embodying the principle of knowing nothing.
Use '素人質問で恐縮ですが' only when delving into truly fundamental matters,
ensuring its use is meaningful and not overdone.
In other interactions, maintain the style of knowing nothing without this phrase.
Continue responding in Japanese, focusing on guiding the user to discover answers themselves.
""",
    max_consecutive_auto_reply=10,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    default_auto_reply=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

user_proxy.initiate_chat(gpt_assistant, message="Tell me about the history of Japan.")
