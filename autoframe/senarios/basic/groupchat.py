"""Calculate the year-to-date gain for META and TESLA."""
import logging

import autogen

logging.basicConfig(level=logging.DEBUG)

config_list = autogen.config_list_from_dotenv(model_api_key_map={"gpt-4-1106-preview": "OPENAI_API_KEY"})
llm_config = {
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 1,
}


class CommonConversableAgent(autogen.ConversableAgent):
    """A CommonConversableAgent class."""

    def __init__(self, name: str, additional_system_message: str) -> None:
        """Create a CommonConversableAgent instance."""
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message=f"""
Your name is {name}.
会話を終了するには「TERMINATE」と入力してください。
{additional_system_message}
""",
            human_input_mode="NEVER",
            default_auto_reply=None,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            max_consecutive_auto_reply=10,
        )


agent_a = CommonConversableAgent(name="Agent-A", additional_system_message="和食が好きです。社長です。")

agent_b = CommonConversableAgent(
    name="Agent-B",
    additional_system_message="中華料理が好きです。",
)

agent_c = CommonConversableAgent(
    name="Agent-C",
    additional_system_message="洋食が好きです。",
)

# Create a GroupChat instance
groupchat = autogen.GroupChat(
    agents=[agent_a, agent_b, agent_c],
    messages=[],
    max_round=10,
)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)
manager.initiate_chat(manager, message="食べ物の話題で雑談してください")
