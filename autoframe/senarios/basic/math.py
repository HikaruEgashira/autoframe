import os
import autogen
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent

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

# 1. create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant", 
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "seed": 42,
        "config_list": config_list,
    }
)

# 2. create the MathUserProxyAgent instance named "mathproxyagent"
# By default, the human_input_mode is "NEVER", which means the agent will not ask for human input.
mathproxyagent = MathUserProxyAgent(
    name="mathproxyagent", 
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)

# given a math problem, we use the mathproxyagent to generate a prompt to be sent to the assistant as the initial message.
# the assistant receives the message and generates a response. The response will be sent back to the mathproxyagent for processing.
# The conversation continues until the termination condition is met, in MathChat, the termination condition is the detect of "\boxed{}" in the response.
math_problem = "Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval notation."
mathproxyagent.initiate_chat(assistant, problem=math_problem)

# math_problem = "For what negative value of $k$ is there exactly one solution to the system of equations \\begin{align*}\ny &= 2x^2 + kx + 6 \\\\\ny &= -x + 4?\n\\end{align*}"
# mathproxyagent.initiate_chat(assistant, problem=math_problem)

# math_problem = "Find all positive integer values of $c$ such that the equation $x^2-7x+c=0$ only has roots that are real and rational. Express them in decreasing order, separated by commas."
# mathproxyagent.initiate_chat(assistant, problem=math_problem)

# # we set the prompt_type to "python", which is a simplied version of the default prompt.
# math_problem = "Problem: If $725x + 727y = 1500$ and $729x+ 731y = 1508$, what is the value of $x - y$ ?"
# mathproxyagent.initiate_chat(assistant, problem=math_problem, prompt_type="python")

# # The wolfram alpha app id is required for this example (the assistant may choose to query Wolfram Alpha).
# import os
# if "WOLFRAM_ALPHA_APPID" not in os.environ:
#     os.environ["WOLFRAM_ALPHA_APPID"] = open("wolfram.txt").read().strip()

# # we set the prompt_type to "two_tools", which allows the assistant to select wolfram alpha when necessary.
# math_problem = "Find all numbers $a$ for which the graph of $y=x^2+a$ and the graph of $y=ax$ intersect. Express your answer in interval notation."
# mathproxyagent.initiate_chat(assistant, problem=math_problem, prompt_type="two_tools")