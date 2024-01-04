from autoframe.express.chainlit import ChainlitAssistantAgent, ChainlitUserProxyAgent
from autoframe.express.config import is_termination_msg, llm_config
from autoframe.express.tools.ask_assistant import ask_assistant, ask_assistant_doc

assistant = ChainlitAssistantAgent(
    "assistant",
    llm_config={
        **llm_config,
        "functions": [
            ask_assistant_doc,
        ],
    },
)
user_proxy = ChainlitUserProxyAgent(
    "user_proxy",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
    function_map={"ask_assistant": ask_assistant},
)
